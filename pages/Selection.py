import streamlit as st

# 1. PAGE CONFIG
st.set_page_config(page_title="Textile Calculator", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE RECEIVER (SAFE PULL) ---
# We pull values. If they don't exist (on refresh), we use these hard-coded defaults.
bg = st.session_state.get("bg_color", "rgb(20, 20, 20)")
txt = st.session_state.get("text_color", "white")

# Safety for the high-contrast boxes
# This ensures that even if box_bg is missing, it grabs the button color or defaults to white.
b_bg = st.session_state.get("box_bg", st.session_state.get("button_bg", "white"))
b_txt = st.session_state.get("box_txt", st.session_state.get("button_txt", "black"))

# --- 3. THE 5-POINT LOCKDOWN CSS ---
# This is now OUTSIDE the 'if' check so the sidebar/container lockdown ALWAYS works.
st.markdown(f"""
    <style>
    /* 1. Main Background */
    .stApp {{ background-color: {bg} !important; }}
    
    /* 2. Global Text Color */
    .stApp *, h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown {{
        color: {txt} !important;
    }}
    
    /* 3. High Contrast & Full Width (Fixes Shrinking) */
    .stButton > button {{
        background-color: {b_bg} !important;
        color: {b_txt} !important;
        border: 2px solid {txt} !important;
        width: 100% !important; 
        transition: 0.3s;
        font-weight: bold !important;
    }}
    .stButton > button * {{ color: {b_txt} !important; }}
    
    /* 4. Input Boxes & Reference Boxes (High Contrast Inversion) */
    div[data-baseweb="input"], [data-testid="stExpander"], .streamlit-expanderHeader {{
        background-color: {b_bg} !important;
        border: 2px solid {txt} !important;
    }}
    div[data-baseweb="input"] input, [data-testid="stExpander"] * {{
        color: {b_txt} !important;
    }}
    
    /* 5. SIDEBAR LOCKDOWN (Kills the artifact in your image) */
    header, [data-testid="stSidebar"], [data-testid="stSidebarNav"], 
    .stAppHeader, button[kind="header"], [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
    }}

    /* 6. CONTAINER LOCKDOWN (Ensures wide layout doesn't shrink on refresh) */
    .stAppViewContainer {{ padding: 0 !important; max-width: 100% !important; width: 100% !important; }}
    [data-testid="stMainBlockContainer"] {{ 
        max-width: 100% !important; 
        width: 100% !important; 
        padding: 1rem 2rem !important; 
    }}
    </style>
""", unsafe_allow_html=True)
    
# 2. NAVIGATION BAR
col_back, col_empty = st.columns([1, 8])
with col_back:
    # Ensure Home.py is the name of your main entry file in the root directory
    if st.button("⬅ Home"):
        st.switch_page("Home.py")

# 3. PAGE CONTENT
st.title("Choose Your Material")
st.write("Select a category to begin your calculation in the **Lab**:")

st.markdown("---")

# Using a container for better layout alignment
container = st.container()
col1, col2 = container.columns(2)

with col1:
    # Double check if your file is "Fibres selection.py" or "Fibres Selection.py"
    if st.button("Fibres' lab", use_container_width=True):
        st.switch_page("pages/Fibres' lab selection.py")

with col2:
    if st.button("Yarn's lab", use_container_width=True):
        st.switch_page("pages/Yarn's lab selection.py")

with col1:
    # Check if 'S' is capital in your filename: "Fabric Selection.py"
    if st.button("Fabric's lab", use_container_width=True):
        st.switch_page("pages/Fabric's lab selection.py")

with col2:
    # Check if 'S' is capital in your filename: "Fabric Selection.py"
    if st.button("Chemical's lab", use_container_width=True):
        st.switch_page("pages/Processing's lab selection.py")

with col1:
    # Check if 'S' is capital in your filename: "Fabric Selection.py"
    if st.button("General lab", use_container_width=True):
        st.switch_page("pages/General lab.py")


st.markdown("---")