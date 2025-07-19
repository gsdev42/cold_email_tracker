import streamlit as st
import pandas as pd
from services.contact_service import insert_bulk_contacts_wrapper as insert_bulk_contacts

def show_import_data():
    st.title("⬆️ Import Excel Data")
    
    st.markdown("""
    ### 📋 Expected Excel Columns:
    `Name | Job Title | Linkedin URL | Company Name | Company Website | Company Linkedin | Company Social | Company Twitter | Location | Company Niche`
    """)
    
    uploaded_file = st.file_uploader(
        "Choose Excel file (.xlsx or .xls)",
        type=['xlsx', 'xls']
    )
    
    if uploaded_file is not None:
        try:
            with st.spinner("Loading Excel file..."):
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ File loaded! Found {len(df)} contacts")
            
            with st.expander("📋 Preview Data (first 5 rows)"):
                st.dataframe(df.head(), use_container_width=True)
            
            if st.button("📥 Import All Contacts", type="primary"):
                try:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("Importing contacts...")
                    progress_bar.progress(50)
                    
                    count = insert_bulk_contacts(df)
                    
                    progress_bar.progress(100)
                    status_text.text("Import complete!")
                    
                    st.cache_data.clear()
                    st.success(f"🎉 Successfully imported {count} contacts!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Import failed: {str(e)}")
                    
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")