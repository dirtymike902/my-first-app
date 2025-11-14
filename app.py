import streamlit as st

# Import Google Fonts for cool sticker font
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f4f8 !important;
        color: #333333 !important;
    }
    body {
        color: #333333 !important;
    }
    .main-title {
        color: #8B4513 !important;
        font-family: 'Arial', sans-serif;
        text-align: center;
        font-size: 2.5em;
    }
    .crooked-clock {
        display: inline-block;
        transform: rotate(-15deg);
        margin-right: 5px;
    }
    .money-bag {
        display: inline-block;
        transform: rotate(5deg);
        margin-left: 10px;
        font-size: 1.2em;
    }
    .subtitle {
        color: #8B4513 !important;
        text-align: center;
        font-size: 1.2em;
        margin-top: -10px;
    }
    .logo {
        font-family: 'Permanent Marker', cursive;
        font-size: 1.5em;
        background-color: #FFD700;
        color: #8B4513 !important;
        border-radius: 15px;
        padding: 8px 12px;
        display: inline-block;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        transform: rotate(-2deg); /* Slight tilt for sticker vibe */
    }
    .section-header {
        color: #34495e !important;
        font-weight: bold;
    }
    .metric-label {
        font-size
