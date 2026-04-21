import streamlit as st
import time

# 1. PAGE CONFIG
st.set_page_config(page_title="Texopedia", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS OVERRIDE (THE "NO-SCROLL" LOCK) ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -65px !important;
    }
    .stApp { overflow: hidden !important; }
    [data-testid="stVerticalBlock"] { gap: 0rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGO SECTION ---
col_l, col_m, col_r = st.columns([1, 2.2, 1])
with col_m:
    st.image("logo.png", use_container_width=True)

# --- 4. WORDINGS (EXTREME LIFT) ---
st.markdown("<div style='margin-top: -115px;'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-weight: bold; margin:0;'>Welcome</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-top: -10px; font-size: 1.1rem;'>Before initializing... Mix for your own vision!</p>", unsafe_allow_html=True)

# --- 5. SLIDERS (RAISED EVEN MORE) ---
# Increased lift from -55px to -70px
st.markdown("<div style='margin-top: -70px;'></div>", unsafe_allow_html=True)
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

# --- 6. COLOR LOGIC ---
bg_color = f"rgb({r}, {g}, {b})"
brightness = (r + g + b) / 3
text_color = "black" if brightness > 128 else "white"
button_bg = "#222222" if brightness > 128 else "#eeeeee"
button_txt = "#ffffff" if brightness > 128 else "#000000"

st.session_state["bg_color"] = bg_color
st.session_state["text_color"] = text_color
st.session_state["button_bg"] = button_bg
st.session_state["button_txt"] = button_txt

# --- 7. CSS STYLE (YOUR DESIGN) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    .stApp *, label, .stMarkdown, .stToggle {{ color: {text_color} !important; }}
    div[data-baseweb="input"] {{ border: 2px solid {text_color} !important; }}
    [data-testid="stSidebar"] {{display: none;}}
    .stAppHeader {{display: none;}}
    </style>
""", unsafe_allow_html=True)

# --- 8. THE SWITCH (FINAL RAISED POSITION) ---
# Increased lift from -10px to -35px
st.markdown("<div style='margin-top: -35px;'></div>", unsafe_allow_html=True)
col_space, col_switch = st.columns([6, 2.5])

with col_switch:
    st.write("**Power**")
    on = st.toggle("Initialize System")
    if on:
        st.write("⚡ System Online...")
        time.sleep(0.5)
        st.switch_page("pages/Selection.py")
