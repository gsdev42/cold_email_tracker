import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection context manager
class DatabaseConnection:
    def __init__(self, db_path='email_tracker.db'):
        self.db_path = db_path
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            logger.error(f"Database error: {exc_val}")
            self.conn.rollback()
        self.conn.close()

# Initialize database
def init_database():
     with DatabaseConnection() as cursor:
        # Create contacts table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            job_title TEXT,
            linkedin_url TEXT,
            company_name TEXT,
            company_website TEXT,
            company_linkedin TEXT,
            company_social TEXT,
            company_twitter TEXT,
            location TEXT,
            company_niche TEXT,
            applied_date DATE,
            followup_interval INTEGER DEFAULT 72,
            last_followup_date DATE,
            next_followup_date DATE,
            status TEXT DEFAULT 'Not Applied',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Verify status column exists
        cursor.execute("PRAGMA table_info(contacts)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'status' not in columns:
            cursor.execute("ALTER TABLE contacts ADD COLUMN status TEXT DEFAULT 'Not Applied'")
        
        # Create templates table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

# Contact operations
def insert_contact(contact_data):
    with DatabaseConnection() as cursor:
        cursor.execute('''
        INSERT INTO contacts (
            name, job_title, linkedin_url, company_name, company_website,
            company_linkedin, company_social, company_twitter, location, company_niche,
            applied_date, followup_interval, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', contact_data)
        return cursor.lastrowid


def get_all_contacts():
    with DatabaseConnection() as cursor:
        cursor.execute('SELECT * FROM contacts ORDER BY created_at DESC')
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        data = [dict(row) for row in rows]
        
        # Create DataFrame from list of dictionaries
        return pd.DataFrame(data)

def update_contact_status(contact_id, status, notes=""):
    with DatabaseConnection() as cursor:
        cursor.execute('''
        UPDATE contacts 
        SET status = ?, notes = ?, last_followup_date = ?
        WHERE id = ?
        ''', (status, notes, datetime.now().strftime('%Y-%m-%d'), contact_id))

def mark_followup_sent(contact_id, followup_interval=72):
    now = datetime.now()
    next_followup = now + timedelta(hours=followup_interval)
    
    with DatabaseConnection() as cursor:
        cursor.execute('''
        UPDATE contacts 
        SET last_followup_date = ?, next_followup_date = ?, status = ?
        WHERE id = ?
        ''', (now.strftime('%Y-%m-%d'), next_followup.strftime('%Y-%m-%d'), 'Follow-Up Sent', contact_id))

def get_due_followups():
    with DatabaseConnection() as cursor:
        cursor.execute('''
        SELECT * FROM contacts 
        WHERE next_followup_date <= date('now') 
        AND status IN ('Applied', 'Follow-Up Sent')
        ORDER BY next_followup_date ASC
        ''')
        return pd.DataFrame(cursor.fetchall())

def delete_contact(contact_id):
    with DatabaseConnection() as cursor:
        cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))

def delete_all_contacts():
    with DatabaseConnection() as cursor:
        cursor.execute('SELECT COUNT(*) FROM contacts')
        count_before = cursor.fetchone()[0]
        
        cursor.execute('DELETE FROM contacts')
        
        cursor.execute('SELECT COUNT(*) FROM contacts')
        count_after = cursor.fetchone()[0]
        
        return count_before - count_after  # Return number of deleted contacts

def reset_database():
    """Completely reset the database by dropping all tables and re-initializing"""
    try:
        # Connect to the database without context manager for full control
        conn = sqlite3.connect('email_tracker.db')
        cursor = conn.cursor()
        
        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        
        # Disable foreign keys to allow dropping tables
        cursor.execute("PRAGMA foreign_keys = OFF;")
        
        # Drop all tables
        for table in tables:
            if table != "sqlite_sequence":  # Skip the sequence table
                cursor.execute(f"DROP TABLE IF EXISTS {table};")
                logger.info(f"Dropped table: {table}")
        
        # Re-enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        # Re-initialize the database structure
        init_database()
        
        logger.info("Database completely reset to initial state")
        return True
        
    except Exception as e:
        logger.error(f"Error resetting database: {str(e)}")
        return False
    
def remove_duplicate_contacts():
    with DatabaseConnection() as cursor:
        cursor.execute('''
        DELETE FROM contacts 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM contacts 
            GROUP BY LOWER(name), LOWER(company_name)
        )  -- Added missing parenthesis
        ''')
        return cursor.rowcount

def get_contact_stats():
    with DatabaseConnection() as cursor:
        cursor.execute('SELECT COUNT(*) FROM contacts')
        total_contacts = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM templates')
        total_templates = cursor.fetchone()[0]
        
        cursor.execute('''
        SELECT name, company_name, COUNT(*) as count 
        FROM contacts 
        GROUP BY LOWER(name), LOWER(company_name) 
        HAVING count > 1
        ORDER BY count DESC
        ''')
        duplicates = cursor.fetchall()
        
        # Convert to serializable format
        serializable_duplicates = []
        for row in duplicates:
            # Convert sqlite3.Row to tuple first, then to dict
            row_tuple = tuple(row)
            serializable_duplicates.append({
                'name': row_tuple[0],
                'company': row_tuple[1],
                'count': row_tuple[2]
            })
        
        return {
            'total_contacts': total_contacts,
            'total_templates': total_templates,
            'duplicate_groups': len(duplicates),
            'duplicates': serializable_duplicates
        }

def insert_bulk_contacts(df):
    contacts_data = []
    for _, row in df.iterrows():
        contact = (
            row.get('Name', ''),
            row.get('Job Title', ''),
            row.get('Linkedin URL', ''),
            row.get('Company Name', ''),
            row.get('Company Website', ''),
            row.get('Company Linkedin', ''),
            row.get('Company Social', ''),
            row.get('Company Twitter', ''),
            row.get('Location', ''),
            row.get('Company Niche', ''),
            None,  # applied_date
            72,    # followup_interval (default 3 days)
            'Not Applied'  # status
        )
        contacts_data.append(contact)
    
    with DatabaseConnection() as cursor:
        cursor.executemany('''
        INSERT INTO contacts (
            name, job_title, linkedin_url, company_name, company_website,
            company_linkedin, company_social, company_twitter, location, company_niche,
            applied_date, followup_interval, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', contacts_data)
        return len(contacts_data)

# Template operations
def add_template(title, body):
    with DatabaseConnection() as cursor:
        cursor.execute('INSERT INTO templates (title, body) VALUES (?, ?)', (title, body))
        return cursor.lastrowid

def get_all_templates():
    with DatabaseConnection() as cursor:
        cursor.execute('SELECT * FROM templates ORDER BY created_at DESC')
        return pd.DataFrame(cursor.fetchall())

def delete_template(template_id):
    with DatabaseConnection() as cursor:
        cursor.execute('DELETE FROM templates WHERE id = ?', (template_id,))