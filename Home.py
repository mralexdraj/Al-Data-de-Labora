import streamlit as st
import time

# 1. PAGE CONFIG
st.set_page_config(page_title="Texopedia", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CLEAN CSS (No more extreme fighting) ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    /* Stop the page from scrolling */
    .stApp { overflow: hidden !important; }
    
    /* Standard tight gaps */
    [data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGO SECTION ---
# Now that it's cropped, we can use a smaller column to keep it centered but manageable
col_l, col_m, col_r = st.columns([1, 1.8, 1])
with col_m:
    st.image("logo.png", use_container_width=True)

# --- 4. WORDINGS (Natural Spacing) ---
# Small -20px nudge just to keep it snug, but no overlapping!
st.markdown("<div style='margin-top: -20px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; margin-top: -5px;'>Need a Double-Check? Not here!</h4>", unsafe_allow_html=True)
st.write("")
st.write("")
st.write("[bold]Before initializing... Mix for your own vision[/bold]")

# --- 5. SLIDERS ---
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

# --- 6. COLOR LOGIC ---
bg_color = f"rgb({r}, {g}, {b})"
brightness = (r + g + b) / 3
text_color = "black" if brightness > 128 else "white"
button_bg = "#222222" if brightness > 128 else "#eeeeee"
button_txt = "#ffffff" if brightness > 128 else "#000000"

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

# --- 8. THE SWITCH ---
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
col_space, col_switch = st.columns([6, 2.5])

with col_switch:
    st.write("**Power**")
    on = st.toggle("Initialize System")
    if on:
        st.write("⚡ System Online...")
        time.sleep(0.5)
        st.switch_page("pages/Selection.py")
