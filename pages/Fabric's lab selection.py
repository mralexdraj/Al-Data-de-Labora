import streamlit as st

# 1. PAGE CONFIG (Enforce Wide Layout)
st.set_page_config(page_title="Fabric Lab", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE RECEIVER (SAFE PULL) ---
bg = st.session_state.get("bg_color", "rgb(20, 20, 20)")
txt = st.session_state.get("text_color", "white")
b_bg = st.session_state.get("box_bg", st.session_state.get("button_bg", "white"))
b_txt = st.session_state.get("box_txt", st.session_state.get("button_txt", "black"))

# --- 3. THE SYNCHRONIZED LOCKDOWN ---
st.markdown(f"""
    <style>
    /* 1. Main Background */
    .stApp {{ background-color: {bg} !important; }}
    
    /* 2. Global Text Color */
    .stApp *, h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown {{
        color: {txt} !important;
    }}
    
    /* 3. High Contrast Buttons (Matching Selection Page Font) */
    .stButton > button {{
        background-color: {b_bg} !important;
        color: {b_txt} !important;
        border: 2px solid {txt} !important;
        width: 100% !important; 
        transition: 0.3s;
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
    
    /* 5. SIDEBAR & HEADER LOCKDOWN (No more refresh leaks) */
    header, [data-testid="stSidebar"], [data-testid="stSidebarNav"], 
    .stAppHeader, button[kind="header"], [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
    }}

    /* 6. CONTAINER LOCKDOWN (Fixes the Shrinkage) */
    .stAppViewContainer {{ padding: 0 !important; max-width: 100vw !important; width: 100vw !important; }}
    [data-testid="stMainBlockContainer"] {{ 
        max-width: 100% !important; 
        width: 100% !important; 
        padding: 1rem 2rem !important; 
    }}

    /* Verdict Box readable override */
    .verdict-box {{ color: black !important; }}
    </style>
""", unsafe_allow_html=True)

# 2. BACK BUTTON (Returns to Selection Page)
col_back, col_empty = st.columns([1, 8])
with col_back:
    if st.button("⬅ Back"):
        st.switch_page("pages/Selection.py")

# 3. PAGE TITLE
st.title("Fabric Lab 🌿")
st.write("Select a test parameter:")
st.markdown("---")

# 4. THE 4 SECTIONS (Grid Layout)
# We make a 2x2 grid (Two rows, Two columns)

# --- Row 1 ---
col1, col2 = st.columns(2)

with col1:
    if st.button("1. Fabric GSM", use_container_width=True):
        st.switch_page("pages/Fabric GSM.py")

with col2:
    if st.button("2. Fabric Strength", use_container_width=True):
        st.switch_page("pages/Fabric Strength.py")

# --- Row 2 ---
col3, col4 = st.columns(2)

with col3:
    if st.button("Fabric Stiffness", use_container_width=True):
        st.switch_page("pages/Fabric Stiffness.py")
with col4:
    if st.button("Fabric Drape", use_container_width=True):
        st.switch_page("pages/Fabric Drape.py")

# --- Row 3 ---
col3, col4 = st.columns(2)

with col3:
    if st.button("Air permeability", use_container_width=True):
        st.switch_page("pages/Air permeability.py")
with col4:
    if st.button("Fabric Cover Factor", use_container_width=True):
        st.switch_page("pages/Fabric Cover Factor.py")

# --- Row 4 ---
col3, col4 = st.columns(2)

with col3:
    if st.button("Fabric Crease Recovery", use_container_width=True):
        st.switch_page("pages/Fabric Crease Recovery.py")
with col4:
    if st.button("Fabric Abrasion Resistance", use_container_width=True):
        st.switch_page("pages/Fabric Abrasion Resistance.py")