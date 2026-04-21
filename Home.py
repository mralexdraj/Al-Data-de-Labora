import streamlit as st
import time 

# 1. PAGE CONFIG
st.set_page_config(page_title="Texopedia", layout="wide", initial_sidebar_state="collapsed")

# --- 2. INITIALIZE PERMANENT MEMORY ---
if "saved_r" not in st.session_state:
    st.session_state["saved_r"] = 100
if "saved_g" not in st.session_state:
    st.session_state["saved_g"] = 100
if "saved_b" not in st.session_state:
    st.session_state["saved_b"] = 100

# --- 3. LAYOUT & GAP COMPRESSION ---
st.markdown("""
    <style>
    /* 1. Removes the massive gap at the very top of the page */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    /* 2. Tightens the gap between all Streamlit elements */
    [data-testid="stVerticalBlock"] { gap: 0.2rem !important; }
    
    /* 3. Prevents the page from scrolling */
    .stApp { overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# LOGO SECTION
col_logo_l, col_logo_m, col_logo_r = st.columns([1, 1.5, 1])
with col_logo_m:
    # Adding a negative margin here to pull the logo even higher
    st.markdown("<div style='margin-top: -30px;'></div>", unsafe_allow_html=True)
    st.image("logo.png", use_container_width=True)
    st.markdown("<h3 style='text-align: center; margin-top: -25px;'>Welcome</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-top: -15px;'>Before initializing... Mix for your own vision!</p>", unsafe_allow_html=True)

# --- 4. SLIDERS ---
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

if brightness > 128:
    text_color = "black"
    button_bg = "#222222"
    button_txt = "#ffffff"
else:
    text_color = "white"
    button_bg = "#eeeeee"
    button_txt = "#000000"

st.session_state["bg_color"] = bg_color
st.session_state["text_color"] = text_color
st.session_state["button_bg"] = button_bg
st.session_state["button_txt"] = button_txt

# --- 6. CSS STYLE (YOUR DESIGN) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    .stApp *, h1, label, .stMarkdown, .stToggle {{ color: {text_color} !important; }}
    div[data-baseweb="input"] {{ border: 2px solid {text_color} !important; }}
    .stButton > button {{
        background-color: {button_bg} !important;
        color: {button_txt} !important;
        border: 1px solid {text_color} !important;
        transition: 0.3s;
    }}
    .stButton > button * {{ color: {button_txt} !important; }}
    [data-testid="stSidebar"] {{display: none;}}
    .stAppHeader {{display: none;}}
    </style>
""", unsafe_allow_html=True)

# --- 7. THE SWITCH (BOTTOM RIGHT) ---
# Small margin here to give the "little gap" you wanted between sliders and button
st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
col_space, col_switch = st.columns([6, 2])

with col_switch:
    st.write("**Power**")
    on = st.toggle("Initialize System")

    if on:
        st.write("⚡ System Online...")
        time.sleep(0.5) 
        st.switch_page("pages/Selection.py")
