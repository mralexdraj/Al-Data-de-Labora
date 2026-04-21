import streamlit as st
import time

# 1. PAGE CONFIG
st.set_page_config(page_title="Texopedia", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE CACHE-BUSTER CSS ---
st.markdown("""
    <style>
    /* Force container to the very top */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -80px !important;
    }
    /* Absolute scroll lock */
    .stApp { overflow: hidden !important; height: 100vh !important; }
    
    /* Remove all internal padding */
    [data-testid="stVerticalBlock"] { gap: 0rem !important; }
    
    /* Target sliders specifically to move them up */
    [data-testid="stSlider"] { margin-top: -20px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGO SECTION ---
col_l, col_m, col_r = st.columns([1, 2.2, 1])
with col_m:
    st.image("logo.png", use_container_width=True)

# --- 4. WORDINGS (YANKED TO LOGO) ---
st.markdown("<div style='margin-top: -130px; position: relative; z-index: 10;'>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-weight: bold; margin:0;'>Welcome</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-top: -10px; font-size: 1.1rem;'>Before initializing... Mix for your own vision!</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- 5. SLIDERS (YANKED TO TEXT) ---
st.markdown("<div style='margin-top: -90px;'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    r = st.slider("Red", 0, 255, value=st.session_state.get("saved_r", 100))
with col2:
    g = st.slider("Green", 0, 255, value=st.session_state.get("saved_g", 100))
with col3:
    b = st.slider("Blue", 0, 255, value=st.session_state.get("saved_b", 100))
st.markdown("</div>", unsafe_allow_html=True)

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

# --- 7. CSS STYLE ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    .stApp *, label, .stMarkdown, .stToggle {{ color: {text_color} !important; }}
    div[data-baseweb="input"] {{ border: 2px solid {text_color} !important; }}
    [data-testid="stSidebar"] {{display: none;}}
    .stAppHeader {{display: none;}}
    </style>
""", unsafe_allow_html=True)

# --- 8. THE SWITCH (YANKED TO SLIDERS) ---
st.markdown("<div style='margin-top: -60px;'>", unsafe_allow_html=True)
col_space, col_switch = st.columns([6, 2.5])
with col_switch:
    st.write("**Power**")
    on = st.toggle("Initialize System")
    if on:
        st.write("⚡ System Online...")
        time.sleep(0.5)
        st.switch_page("pages/Selection.py")
st.markdown("</div>", unsafe_allow_html=True)
