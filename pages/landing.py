import streamlit as st
from streamlit_card import card

def show_landing():
    # Custom CSS styling for landing page
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Open+Sans&display=swap');
        
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            background-attachment: fixed;
            padding: 3rem;
        }
        
        .main-header {
            font-family: 'Montserrat', sans-serif;
            font-size: 3.5rem !important;
            text-align: center;
            color: #ffffff;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .sub-header {
            font-family: 'Open Sans', sans-serif;
            font-size: 1.5rem;
            text-align: center;
            color: #e0f7fa;
            font-style: italic;
            margin-bottom: 2rem;
        }
        
        .feature-text {
            max-width: 800px;
            margin: 2rem auto;
            font-family: 'Open Sans', sans-serif;
            font-size: 1.1rem;
            line-height: 1.8;
            text-align: center;
            color: #f5f5f5;
        }
        
        .feature-list {
            text-align: left;
            display: inline-block;
            margin: 1rem 0;
        }
        
        div.stButton > button {
            background-color: #4fc3f7;
            color: #000000;
            border: none;
            padding: 0.7em 1.5em;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        div.stButton > button:hover {
            background-color: #0288d1;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }
        </style>
    """, unsafe_allow_html=True)

    # Header section
    st.markdown("<h1 class='main-header'>Cold Email Tracker Pro 📧</h1>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Your Outreach, Optimized.</div>", unsafe_allow_html=True)

    # Feature highlights
    st.markdown("""
    <div class="feature-text">
        Transform your cold outreach with <strong>data-driven precision</strong> — no more guessing what works.  
        <br><br>
        Our tracker helps you:
        <ul class="feature-list">
            <li>🚀 <strong>Boost response rates</strong> – Track what actually gets replies</li>
            <li>⏱️ <strong>Save time</strong> – Never miss a follow-up again</li>
            <li>📈 <strong>Grow smarter</strong> – Data-backed outreach strategies</li>
            <li>🔍 <strong>Stay organized</strong> – All your prospects in one place</li>
        </ul>
        <em>"Your Outreach, Optimized."</em>
    </div>
    """, unsafe_allow_html=True)

    # CTA button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Go to Dashboard"):
            st.query_params["nav"] = "📊 Dashboard"
            st.rerun()
    
    st.markdown("---")