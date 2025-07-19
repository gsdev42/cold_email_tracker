import streamlit as st
from database import get_all_templates, add_template, delete_template

@st.cache_data(ttl=60)
def load_templates():
    return get_all_templates()