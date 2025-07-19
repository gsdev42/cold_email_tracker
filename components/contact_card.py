import streamlit as st
import pandas as pd

def contact_card(row):

    name = row.get('name', 'Unknown')
    job_title = row.get('job_title', 'N/A')
    company_name = row.get('company_name', 'N/A')
    status = row.get('status', 'Not Applied')
    
    # Generate status class for CSS
    status_class = f"status-{status.lower().replace(' ', '-').replace('/', '-')}"
    
    # Build contact links
    contact_links = []
    linkedin_url = row.get('linkedin_url', '')
    if pd.notna(linkedin_url) and linkedin_url and linkedin_url != 'None':
        contact_links.append(f'<a href="{linkedin_url}" target="_blank" class="link-button">LinkedIn</a>')
    
    # Build company links
    company_links = []
    link_types = {
        'website': row.get('company_website', ''),
        'linkedin': row.get('company_linkedin', ''),
        'social': row.get('company_social', ''),
        'twitter': row.get('company_twitter', '')
    }
    
    for link_type, link in link_types.items():
        if pd.notna(link) and link and link != 'None':
            company_links.append(
                f'<a href="{link}" target="_blank" class="link-button">{link_type.capitalize()}</a>'
            )
    
    # Render the card
    st.markdown(f"""
    <div class="contact-row">
        <div style="display: grid; grid-template-columns: 2fr 1.5fr 2fr 1fr 1fr; gap: 1rem; align-items: center;">
            <div>
                <div class="contact-name">{name}</div>
                <div class="contact-details">{job_title}</div>
            </div>
            <div>
                <div style="margin-bottom: 0.5rem;">
                    {''.join(contact_links) if contact_links else 'No contact info'}
                </div>
            </div>
            <div>
                <div class="contact-company">{company_name}</div>
                <div style="margin-top: 0.5rem;">
                    {''.join(company_links) if company_links else 'No links'}
                </div>
            </div>
            <div>
                <span class="status-badge {status_class}">{status}</span>
            </div>
            <div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)