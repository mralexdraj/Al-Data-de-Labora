import streamlit as st
import time # Needed for the delay effect

# 1. PAGE CONFIG
st.set_page_config(page_title="Texopedia", layout="wide", initial_sidebar_state="collapsed")

left_co, cent_co, last_co = st.columns([0.2, 3, 0.2])

with cent_co:
    st.image("logo.png", use_container_width=True)

st.markdown("<h3 style='text-align: center; margin-top: -20px;'>Welcome</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Before initializing... Mix for your own vision!</p>", unsafe_allow_html=True)

st.write("Welcome")
st.write("Before initializing... Mix for your own vision!")

# --- 2. INITIALIZE PERMANENT MEMORY ---
# We use these to store the colors safely away from Streamlit's widget cleanup
if "saved_r" not in st.session_state:
    st.session_state["saved_r"] = 100
if "saved_g" not in st.session_state:
    st.session_state["saved_g"] = 100
if "saved_b" not in st.session_state:
    st.session_state["saved_b"] = 100

# --- 3. SLIDERS ---
# Notice we use `value=` instead of `key=`. This prevents the reset!
col1, col2, col3 = st.columns(3)
with col1:
    r = st.slider("Red", 0, 255, value=st.session_state["saved_r"])
with col2:
    g = st.slider("Green", 0, 255, value=st.session_state["saved_g"])
with col3:
    b = st.slider("Blue", 0, 255, value=st.session_state["saved_b"])

# Immediately update the permanent memory with the current slider positions
st.session_state["saved_r"] = r
st.session_state["saved_g"] = g
st.session_state["saved_b"] = b

# --- 4. COLOR LOGIC ---
bg_color = f"rgb({r}, {g}, {b})"
brightness = (r + g + b) / 3

if brightness > 128:
    text_color = "black"
    button_bg = "#222222"  # Dark gray/black button
    button_txt = "#ffffff" # White text on button
else:
    text_color = "white"
    button_bg = "#eeeeee"  # Light gray/white button
    button_txt = "#000000" # Black text on button

# SAVE ALL COLORS FOR OTHER PAGES (The Receivers)
st.session_state["bg_color"] = bg_color
st.session_state["text_color"] = text_color
st.session_state["button_bg"] = button_bg
st.session_state["button_txt"] = button_txt

# --- 5. CSS STYLE ---
st.markdown(f"""
    <style>
    /* Background & Text */
    .stApp {{
        background-color: {bg_color};
    }}
    .stApp *, h1, label, .stMarkdown, .stToggle {{
        color: {text_color} !important;
    }}
    
    /* Input/Widget Borders */
    div[data-baseweb="input"] {{
        border: 2px solid {text_color} !important;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {button_bg} !important;
        color: {button_txt} !important;
        border: 1px solid {text_color} !important;
        transition: 0.3s;
    }}
    .stButton > button * {{
        color: {button_txt} !important;
    }}
    
    /* Keep Verdict Boxes readable */
    .verdict-box {{
        color: black !important;
    }}
    
    /* HIDE SIDEBAR & HEADER completely */
    [data-testid="stSidebar"] {{display: none;}}
    [data-testid="stSidebarNav"] {{display: none;}}
    .stAppHeader {{display: none;}}
    </style>
""", unsafe_allow_html=True)

# --- 6. THE SWITCH (Bottom Right) ---
st.markdown("<br>" * 3, unsafe_allow_html=True) # Push to bottom

col_space, col_switch = st.columns([6, 2])

with col_switch:
    st.write("**Power**")
    # The Toggle Switch
    on = st.toggle("Initialize System")

    if on:
        st.write("⚡ System Online...")
        time.sleep(1.0) # A 1-second pause for effect
        st.switch_page("pages/Selection.py")
