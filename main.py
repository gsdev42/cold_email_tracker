
import streamlit as st
from pages import dashboard, import_data, followups, templates, analytics, db_info, landing
from config import CSS_STYLES
from database import init_database

# Page configuration
st.set_page_config(
    page_title="Cold Email Tracker",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_database()

# Inject CSS
st.markdown(CSS_STYLES, unsafe_allow_html=True)

# Get navigation selection from URL
query_params = st.query_params
nav_selection = query_params.get("nav", None)

# Page options
page_options = [
    "Home", 
    "Dashboard", 
    "Import Data", 
    "Follow-Up Reminders", 
    "Email Templates", 
    "Analytics", 
    "Database Info"
]

# Set current page based on URL or default
current_page = "Home"
if nav_selection:
    for option in page_options:
        if nav_selection in option:
            current_page = option
            break

# Always show the landing page when no nav selection
if not nav_selection:
    landing.show_landing()
    st.stop()

# Sidebar Navigation
st.sidebar.title("Cold Email Tracker")
st.sidebar.markdown("---")

# Data Management Section
with st.sidebar.expander("Data Management", expanded=False):
    st.markdown("**DANGER ZONE**")

    if st.button("Remove Duplicates", help="Remove duplicate contacts based on name + company"):
        with st.spinner("Removing duplicates..."):
            from services.contact_service import remove_duplicates_wrapper
            removed_count = remove_duplicates_wrapper()
            st.cache_data.clear()
            st.success(f"Removed {removed_count} duplicate contacts!")

    if st.button("Delete ALL Data", help="Delete all contacts - CANNOT be undone!"):
        if st.checkbox("I understand this will delete ALL contacts"):
            from services.contact_service import delete_all_contacts_wrapper
            deleted_count = delete_all_contacts_wrapper()
            st.cache_data.clear()
            st.success(f"Deleted {deleted_count} contacts!")
            st.rerun()

# Refresh button
if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# Render sidebar selectbox with current selection
page = st.sidebar.selectbox("Navigate to:", page_options, index=page_options.index(current_page))

# Page routing
if page == "Home":
    landing.show_landing()
elif page == "Dashboard":
    dashboard.show_dashboard()
elif page == "Import Data":
    import_data.show_import_data()
elif page == "Follow-Up Reminders":
    followups.show_followups()
elif page == "Email Templates":
    templates.show_templates()
elif page == "Analytics":
    analytics.show_analytics()
elif page == "Database Info":
    db_info.show_db_info()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Cold Email Tracker v2.0**")
