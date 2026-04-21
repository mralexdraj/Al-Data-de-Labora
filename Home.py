import streamlit as st
import time 

# 1. PAGE CONFIG
st.set_page_config(page_title="Texopedia", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE TOTAL GAP KILLER ---
st.markdown("""
    <style>
    /* 1. Force the main container to start at the absolute top of the browser */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -30px !important;
    }
    /* 2. Remove space around the image container */
    [data-testid="stImage"] {
        margin-top: -20px !important;
        margin-bottom: -50px !important;
    }
    /* 3. Tighten text spacing */
    [data-testid="stVerticalBlock"] { gap: 0rem !important; }
    
    /* 4. Disable scroll */
    .stApp { overflow: hidden !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE LOGO SECTION ---
col_l, col_m, col_r = st.columns([0.3, 3, 0.3])
with col_m:
    st.image("logo.png", use_container_width=True)
    st.markdown("<h2 style='text-align: center; margin-top: -60px; font-weight: bold;'>Welcome</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-top: -10px;'>Before initializing... Mix for your own vision!</p>", unsafe_allow_html=True)

# --- 4. THE REST OF YOUR CODE (SLIDERS & COLOR LOGIC) ---
# ... (Keep your slider and logic code here)
