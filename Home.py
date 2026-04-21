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

# --- 3. THE "FLEX" LAYOUT (The fix for your image) ---
st.markdown("""
    <style>
    /* 1. Remove all padding and stop scrolling */
    .block-container {
        padding: 0rem !important;
        max-width: 100%;
    }
    .stApp {
        overflow: hidden !important;
        height: 100vh;
    }
    
    /* 2. Center everything and remove the massive top gap */
    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    /* 3. Force Logo size and pull text close */
    .main-header {
        text-align: center;
        margin-top: -20px; /* Pulls it away from the browser top */
    }
    .main-header img {
        width: 400px; /* Big enough for your vision */
        margin-bottom: -40px;
    }
    </style>
""", unsafe_allow_html=True)

# 4. LOGO & TEXT
st.markdown(f"""
    <div class="main-header">
        <img src="app/static/logo.png">
        <h2 style="margin:0; padding:0; font-weight: bold;">Welcome</h2>
        <p style="margin:0; padding:0; font-size: 1.1rem;">Before initializing... Mix for your own vision!</p>
    </div>
""", unsafe_allow_html=True)

# Add a tiny bit of air before the sliders
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# --- 5. SLIDERS ---
# We keep these in 3 columns but wrap them so they don't hit the edges
col_pad1, col1, col2, col3, col_pad2 = st.columns([0.2, 1, 1, 1, 0.2])
with col1:
    r = st.slider("Red", 0, 255, value=st.session_state["saved_r"])
with col2:
    g = st.slider("Green", 0, 255, value=st.session_state["saved_g"])
with col3:
    b = st.slider("Blue", 0, 255, value=st.session_state["saved_b"])

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

# --- 7. CSS STYLE (YOUR ORIGINAL DESIGN) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    .stApp *, label, .stMarkdown, .stToggle {{ color: {text_color} !important; }}
    div[data-baseweb="input"] {{ border: 2px solid {text_color} !important; }}
    [data-testid="stSidebar"] {{display: none;}}
    .stAppHeader {{display: none;}}
    </style>
""", unsafe_allow_html=True)

# --- 8. THE SWITCH (Bottom Right) ---
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
col_space, col_switch = st.columns([6, 2])

with col_switch:
    st.write("**Power**")
    on = st.toggle("Initialize System")

    if on:
        st.write("⚡ System Online...")
        time.sleep(0.5)
        st.switch_page("pages/Selection.py")
