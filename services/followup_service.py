import streamlit as st
from database import get_due_followups, mark_followup_sent

@st.cache_data(ttl=30)
def load_due_followups():
    return get_due_followups()

def mark_followup_sent_wrapper(contact_id):
    """Wrapper function for mark_followup_sent from database"""
    return mark_followup_sent(contact_id)