import streamlit as st
import time

# 1. PAGE CONFIG
st.set_page_config(page_title="Texopedia", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE CSS KILL-SWITCH (Removes the top gap completely) ---
st.markdown("""
    <style>
    /* Remove the massive white space at the top of every Streamlit app */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -50px !important;
    }
    /* Stop the page from scrolling */
    .stApp { overflow: hidden !important; }
    /* Tighten space between elements */
    [data-testid="stVerticalBlock"] { gap: 0rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGO & WELCOME ---
# Using native st.image because the HTML version was failing to find the file
col_l, col_m, col_r = st.columns([1, 2.5, 1])
with col_m:
    st.image("logo.png", use_container_width=True)
    st.markdown("<h2 style='text-align: center; margin-top: -60px;'>Welcome</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-top: -10px;'>Before initializing... Mix for your own vision!</p>", unsafe_allow_html=True)

# --- 4. SLIDERS ---
# Resetting the sliders to sit naturally
st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    r = st.slider("Red", 0, 255, value=st.session_state.get("saved_r", 100))
with col2:
    g = st.slider("Green", 0, 255, value=st.session_state.get("saved_g", 100))
with col3:
    b = st.slider("Blue", 0, 255, value=st.session_state.get("saved_b", 100))

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

# --- 6. CSS STYLE (YOUR DESIGN) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    .stApp *, label, .stMarkdown, .stToggle {{ color: {text_color} !important; }}
    div[data-baseweb="input"] {{ border: 2px solid {text_color} !important; }}
    [data-testid="stSidebar"] {{display: none;}}
    .stAppHeader {{display: none;}}
    </style>
""", unsafe_allow_html=True)

# --- 7. THE SWITCH ---
st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
col_space, col_switch = st.columns([6, 2])

with col_switch:
    st.write("**Power**")
    on = st.toggle("Initialize System")
    if on:
        st.write("⚡ System Online...")
        time.sleep(0.5)
        st.switch_page("pages/Selection.py")
