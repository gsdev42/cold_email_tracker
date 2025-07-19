import streamlit as st
import plotly.express as px
from services.contact_service import load_contacts

def show_analytics():
    st.title("📈 Analytics")
    
    contacts_df = load_contacts()
    
    if len(contacts_df) == 0:
        st.info("No data yet!")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            # Ensure status column exists
            if 'status' in contacts_df.columns:
                status_counts = contacts_df['status'].value_counts()
                fig = px.pie(values=status_counts.values, names=status_counts.index, title="Status Distribution")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Status data not available")
        
        with col2:
            # Ensure company_name column exists
            if 'company_name' in contacts_df.columns:
                # Create a DataFrame for Plotly
                top_companies = contacts_df['company_name'].value_counts().head(10).reset_index()
                top_companies.columns = ['Company', 'Count']
                
                fig = px.bar(
                    top_companies, 
                    x='Count', 
                    y='Company', 
                    orientation='h', 
                    title="Top Companies"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Company data not available")