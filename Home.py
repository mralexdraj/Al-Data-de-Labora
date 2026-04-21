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

# --- 3. THE "NO-SCROLL" OVERRIDE ---
st.markdown("""
    <style>
    /* Kill all default padding */
    .block-container { padding: 0rem !important; }
    [data-testid="stVerticalBlock"] { gap: 0rem !important; }
    .stApp { overflow: hidden !important; }

    /* Force the header section to the absolute top */
    .header-container {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        text-align: center;
        z-index: 99;
    }
    .header-container img {
        width: 350px; /* Adjust this to make logo bigger or smaller */
        margin-top: -10px;
    }
    
    /* Position the Power Button at the absolute bottom right */
    .footer-container {
        position: absolute;
        bottom: 20px;
        right: 40px;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# 4. LOGO & TEXT (Pinned to Top)
st.markdown(f"""
    <div class="header-container">
        <img src="app/static/logo.png">
        <div style="margin-top: -40px;">
            <h2 style="margin:0; padding:0;">Welcome</h2>
            <p style="margin:0; padding:0;">Before initializing... Mix for your own vision!</p>
        </div>
    </div>
    <div style="margin-top: 280px;"></div> """, unsafe_allow_html=True)

# --- 5. SLIDERS ---
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

# --- 8. THE SWITCH (Pinned to Bottom) ---
# Wrapping the toggle in the footer-container to pin it
on = False
with st.container():
    st.markdown('<div class="footer-container">', unsafe_allow_html=True)
    st.write("**Power**")
    on = st.toggle("Initialize System")
    st.markdown('</div>', unsafe_allow_html=True)

if on:
    st.write("⚡ System Online...")
    time.sleep(0.5)
    st.switch_page("pages/Selection.py")
