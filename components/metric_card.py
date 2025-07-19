import streamlit as st

def metric_card(title, content_lines, urgent=False):

    urgent_class = "urgent" if urgent else ""
    
    # Generate content HTML
    content_html = "".join(
        [f'<p style="color: #6c757d !important;"><strong>{line.split(":")[0]}:</strong> {line.split(":")[1].strip()}</p>' 
         for line in content_lines]
    )
    
    st.markdown(f"""
    <div class="metric-card {urgent_class}">
        <h4 style="color: #212529 !important;">{title}</h4>
        {content_html}
    </div>
    """, unsafe_allow_html=True)