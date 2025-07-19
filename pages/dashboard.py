import streamlit as st
import pandas as pd
from services.followup_service import load_due_followups
from components import contact_card, status_badge, metric_card
from services.contact_service import load_contacts, update_contact_status, delete_contact
from services.followup_service import load_due_followups, mark_followup_sent_wrapper as mark_followup_sent

# Dark theme color mapping with better contrast
def get_company_color(company_name):
    """Assign consistent dark theme color to a company using hash algorithm"""
    if not company_name:
        return "#555555"  # Dark gray for missing company
    
    # Generate hue from hash (0-360)
    hue = hash(company_name) % 360
    
    # Dark theme colors: higher saturation, lower lightness
    return f"hsl({hue}, 65%, 25%)"

def format_social_links(row):
    """Format social links with pipe separators"""
    links = []
    if row.get('website'):
        links.append(f"[Website]({row['website']})")
    if row.get('linkedin'):
        links.append(f"[LinkedIn]({row['linkedin']})")
    if row.get('social'):
        links.append(f"[Social]({row['social']})")
    if row.get('twitter'):
        links.append(f"[Twitter]({row['twitter']})")
    
    return " | ".join(links) if links else "No links available"

def dashboard_contact_card(row):
    """Custom contact card for dashboard with improved link formatting"""
    # Name and title
    st.subheader(row.get('name', 'Unknown'))
    
    # Title and company
    title = row.get('title', '')
    company = row.get('company_name', '')
    if title and company:
        st.write(f"{title} at {company}")
    elif title:
        st.write(title)
    elif company:
        st.write(company)
    
    # Contact info
    email = row.get('email', '')
    phone = row.get('phone', '')
    if email or phone:
        contact_info = []
        if email:
            contact_info.append(f"✉️ {email}")
        if phone:
            contact_info.append(f"📞 {phone}")
        st.write(" | ".join(contact_info))
    
    # Formatted social links with pipe separators
    links_text = format_social_links(row)
    st.markdown(links_text)

def show_dashboard():
    st.title("📊 Dashboard - All Contacts")

    # Get contacts with caching
    contacts_df = load_contacts()

    if len(contacts_df) == 0:
        st.info("No contacts found. Start by importing your Excel file!")
        st.markdown("👆 Use the sidebar to navigate to 'Import Data'")
    else:
        # Quick stats
        total_contacts = len(contacts_df)
        status_counts = contacts_df['status'].value_counts()
        applied_count = status_counts.get('Applied', 0) + status_counts.get('Follow-Up Sent', 0)
        accepted_count = status_counts.get('Accepted', 0)
        followup_due = len(load_due_followups())

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Total Contacts", total_contacts)
        with col2: st.metric("Applied", applied_count)
        with col3: st.metric("Follow-ups Due", followup_due)
        with col4: st.metric("Accepted", accepted_count)

        st.markdown("---")

        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_options = ['All'] + list(contacts_df['status'].unique())
            status_filter = st.selectbox("Filter by Status:", status_options)
        with col2:
            company_options = ['All'] + sorted(contacts_df['company_name'].dropna().unique())
            company_filter = st.selectbox("Filter by Company:", company_options)
        with col3:
            search_term = st.text_input("Search (Name/Company):")

        # Apply filters
        filtered_df = contacts_df.copy()
        if status_filter != 'All':
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        if company_filter != 'All':
            filtered_df = filtered_df[filtered_df['company_name'] == company_filter]
        if search_term:
            mask = (
                filtered_df['name'].str.contains(search_term, case=False, na=False) |
                filtered_df['company_name'].str.contains(search_term, case=False, na=False)
            )
            filtered_df = filtered_df[mask]

        # Pagination
        contacts_per_page = 20
        total_pages = (len(filtered_df) - 1) // contacts_per_page + 1 if len(filtered_df) > 0 else 1

        if total_pages > 1:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                page_num = st.selectbox(
                    f"Page (showing {contacts_per_page} per page):",
                    range(1, total_pages + 1)
                )
        else:
            page_num = 1

        start_idx = (page_num - 1) * contacts_per_page
        end_idx = start_idx + contacts_per_page
        page_data = filtered_df.iloc[start_idx:end_idx]

        st.subheader(f"Contacts ({len(filtered_df)} found, page {page_num} of {total_pages})")

        if len(page_data) > 0:
            st.markdown('<div class="contact-table">', unsafe_allow_html=True)

            for idx, (_, row) in enumerate(page_data.iterrows()):
                # Generate a unique ID for this row using index + contact ID
                row_id = f"{idx}_{row.get('id', 'no_id')}"

                # Company tag with dark theme colors
                company = row.get('company_name', '')
                if company:
                    color = get_company_color(company)
                    st.markdown(
                        f'<div style="background-color: {color}; color: white; padding: 4px 12px; '
                        f'border-radius: 4px; display: inline-block; margin-bottom: 8px; font-weight: 500;">'
                        f'🏢 {company}</div>',
                        unsafe_allow_html=True
                    )

                # Use custom contact card with improved link formatting
                dashboard_contact_card(row)

                # Actions row
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    new_status = st.selectbox(
                        "Status",
                        ['Not Applied', 'Applied', 'Follow-Up Sent', 'Rejected', 'Accepted', 'No Response'],
                        index=['Not Applied', 'Applied', 'Follow-Up Sent', 'Rejected', 'Accepted', 'No Response'].index(
                            row.get('status', 'Not Applied')
                        ),
                        key=f"status_{row_id}"
                    )
                with col2:
                    if st.button("Update", key=f"update_{row_id}", help="Update Status"):
                        if 'id' in row and row['id']:
                            update_contact_status(row['id'], new_status)
                            st.cache_data.clear()
                            st.success("Updated!")
                            st.rerun()
                        else:
                            st.error("Contact ID missing!")
                with col3:
                    if st.button("Mark Follow-up", key=f"followup_{row_id}", help="Mark Follow-up Sent"):
                        if 'id' in row and row['id']:
                            mark_followup_sent(row['id'])
                            st.cache_data.clear()
                            st.success("Follow-up marked!")
                            st.rerun()
                        else:
                            st.error("Contact ID missing!")
                with col4:
                    if st.button("Delete", key=f"delete_{row_id}", help="Delete Contact"):
                        if 'id' in row and row['id']:
                            delete_contact(row['id'])
                            st.cache_data.clear()
                            st.success("Deleted!")
                            st.rerun()
                        else:
                            st.error("Contact ID missing!")

                # Dark theme separator
                st.markdown("<div style='height:1px; background:#444; margin:20px 0;'></div>", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown('</div>', unsafe_allow_html=True)

            # Show unique company names with serial numbers and dark theme colors
            unique_companies = contacts_df['company_name'].dropna().unique()
            st.markdown("### Unique Companies")
            cols = st.columns(3)
            for i, name in enumerate(sorted(unique_companies), start=1):
                color = get_company_color(name)
                with cols[(i-1) % 3]:
                    st.markdown(
                        f'<div style="background-color: {color}; color: white; padding: 8px 12px; '
                        f'border-radius: 4px; margin-bottom: 10px; font-weight: 500;">'
                        f'<b>{i}. {name}</b></div>',
                        unsafe_allow_html=True
                    )