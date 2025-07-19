import streamlit as st
from services.contact_service import load_stats

def show_db_info():
    st.title("🗂️ Database Information")
    
    stats = load_stats()
    
    # Database stats
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Total Contacts", stats['total_contacts'])
    with col2: st.metric("Total Templates", stats['total_templates'])
    with col3: st.metric("Duplicate Groups", stats['duplicate_groups'])
    
    # Show duplicates if any
    if stats['duplicates']:
        st.subheader("🔍 Found Duplicates")
        st.markdown("**These contacts appear to be duplicates (same name + company):**")
        
        for name, company, count in stats['duplicates'][:10]:
            st.markdown(f"- **{name}** at **{company}** ({count} entries)")
        
        if len(stats['duplicates']) > 10:
            st.markdown(f"... and {len(stats['duplicates']) - 10} more duplicate groups")
        
        st.info("💡 Use 'Remove Duplicates' in the sidebar to clean up your data!")
    else:
        st.success("✅ No duplicates found!")