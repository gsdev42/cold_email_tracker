import streamlit as st
from services.template_service import load_templates, add_template, delete_template

def show_templates():
    st.title("📝 Email Templates")
    
    with st.expander("➕ Add New Template"):
        title = st.text_input("Title:")
        body = st.text_area("Body:", height=150)
        
        if st.button("💾 Save"):
            if title and body:
                add_template(title, body)
                st.cache_data.clear()
                st.success("Saved!")
                st.rerun()
    
    templates_df = load_templates()
    
    for _, template in templates_df.iterrows():
        with st.expander(f"📄 {template['title']}"):
            st.code(template['body'])
            if st.button("🗑️ Delete", key=f"del_{template['id']}"):
                delete_template(template['id'])
                st.cache_data.clear()
                st.rerun()