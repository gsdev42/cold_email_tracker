import streamlit as st
from services.followup_service import load_due_followups, mark_followup_sent
from components import metric_card

def show_followups():
    st.title("⏰ Follow-Up Reminders")
    
    due_contacts = load_due_followups()
    
    if len(due_contacts) == 0:
        st.success("🎉 No follow-ups due right now!")
    else:
        st.warning(f"⚠️ {len(due_contacts)} contacts need follow-up!")
        
        for i, (_, contact) in enumerate(due_contacts.iterrows()):
            metric_card(
                title=f"{contact['name']} - {contact['company_name']}",
                content=[
                    f"<strong>Job Title:</strong> {contact['job_title']}",
                    f"<strong>Last Follow-up:</strong> {contact['last_followup_date'] or 'Never'}"
                ],
                urgent=True
            )
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                if st.button("✅ Mark Sent", key=f"mark_{contact['id']}"):
                    mark_followup_sent(contact['id'])
                    st.cache_data.clear()
                    st.rerun()
            with col3:
                if contact['linkedin_url']:
                    st.markdown(f"[🔗 LinkedIn]({contact['linkedin_url']})")