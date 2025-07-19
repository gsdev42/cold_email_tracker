import streamlit as st
import pandas as pd
from database import (
    get_all_contacts, 
    update_contact_status,
    delete_contact,
    insert_bulk_contacts,  # Add this import
    remove_duplicate_contacts,
    delete_all_contacts,
    get_contact_stats
)

@st.cache_data(ttl=30)
def load_contacts():
    df = get_all_contacts()
    
    # Ensure all required columns exist
    required_columns = [
        'id', 'name', 'job_title', 'linkedin_url', 'company_name',
        'company_website', 'company_linkedin', 'company_social', 
        'company_twitter', 'status'
    ]
    
    for col in required_columns:
        if col not in df.columns:
            df[col] = None
    
    # Set default status
    if 'status' not in df.columns or df['status'].isnull().all():
        df['status'] = 'Not Applied'
    
    return df

@st.cache_data(ttl=30)
def load_stats():
    stats = get_contact_stats()
    
    # Ensure stats is serializable
    if 'duplicates' in stats:
        if isinstance(stats['duplicates'], list):
            stats['duplicates'] = [dict(d) for d in stats['duplicates']]
    
    return stats

# Add these functions to make them available through the service
def insert_bulk_contacts_wrapper(df):
    return insert_bulk_contacts(df)



# Add this at the bottom
def delete_all_contacts_wrapper():
    return delete_all_contacts()

def remove_duplicates_wrapper():
    return remove_duplicate_contacts()