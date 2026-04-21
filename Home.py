import streamlit as st
import time 

# 1. PAGE CONFIG
st.set_page_config(page_title="Texopedia", layout="wide", initial_sidebar_state="collapsed")

# --- 2. INITIALIZE PERMANENT MEMORY ---
if "saved_r" not in st.session_state:
    st.session_state["saved_r"] = 0
if "saved_g" not in st.session_state:
    st.session_state["saved_g"] = 0
if "saved_b" not in st.session_state:
    st.session_state["saved_b"] = 1

# --- 3. EXTREME LAYOUT COMPRESSION ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    [data-testid="stVerticalBlock"] { gap: 0rem !important; }
    .stApp { overflow: hidden !important; }
    </style>
    """, unsafe_allow_html=True)

# LOGO SECTION (Big Size, Zero Gap)
col_logo_l, col_logo_m, col_logo_r = st.columns([0.4, 3, 0.4])
with col_logo_m:
    # Pulls the logo up to the top edge
    st.markdown("<div style='margin-top: -90px;'></div>", unsafe_allow_html=True)
    st.image("logo.png", use_container_width=True)
    
    # THE KEY FIX: This negative margin-top pulls the word "Welcome" 
    # almost halfway into the logo's bottom padding to kill the gap.
    st.markdown("<h2 style='text-align: center; margin-top: -100px; padding:0; font-weight: bold;'>Welcome</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-top: -10px; padding:0; font-size: 1.1rem;'>Before initializing... Mix for your own vision!</p>", unsafe_allow_html=True)

# --- 4. SLIDERS (Yanked Up) ---
# This pulls the sliders even higher toward the text
st.markdown("<div style='margin-top: -30px;'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    r = st.slider("Red", 0, 255, value=st.session_state["saved_r"])
with col2:
    g = st.slider("Green", 0, 255, value=st.session_state["saved_g"])
with col3:
    b = st.slider("Blue", 0, 255, value=st.session_state["saved_b"])

st.session_state["saved_r"] = r
st.session_state["saved_g"] = g
st.session_state["saved_b"] = b

# --- 5. COLOR LOGIC ---
bg_color = f"rgb({r}, {g}, {b})"
brightness = (r + g + b) / 3
text_color = "black" if brightness > 128 else "white"
button_bg = "#222222" if brightness > 128 else "#eeeeee"
button_txt = "#ffffff" if brightness > 128 else "#000000"

st.session_state["bg_color"] = bg_color
st.session_state["text_color"] = text_color
st.session_state["button_bg"] = button_bg
st.session_state["button_txt"] = button_txt

# --- 6. CSS STYLE ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    .stApp *, h1, label, .stMarkdown, .stToggle {{ color: {text_color} !important; }}
    div[data-baseweb="input"] {{ border: 2px solid {text_color} !important; }}
    [data-testid="stSidebar"] {{display: none;}}
    .stAppHeader {{display: none;}}
    </style>
""", unsafe_allow_html=True)

# --- 7. THE SWITCH ---
# A small buffer to keep the action button visible at the bottom
st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
col_space, col_switch = st.columns([6, 2.5])

with col_switch:
    st.write("**Power**")
    on = st.toggle("Initialize System")

    if on:
        st.write("⚡ System Online...")
        time.sleep(0.5) 
        st.switch_page("pages/Selection.py")
