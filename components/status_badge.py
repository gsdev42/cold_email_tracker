import streamlit as st

def status_badge(status):

    status_class = f"status-{status.lower().replace(' ', '-').replace('/', '-')}"
    st.markdown(f"""
    <span class="status-badge {status_class}">{status}</span>
    """, unsafe_allow_html=True)