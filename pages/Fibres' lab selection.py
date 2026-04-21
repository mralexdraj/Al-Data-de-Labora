import streamlit as st

# 1. PAGE CONFIG
st.set_page_config(page_title="Fibre Lab", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE RECEIVER ---
bg = st.session_state.get("bg_color", "rgb(20, 20, 20)")
txt = st.session_state.get("text_color", "white")
b_bg = st.session_state.get("box_bg", st.session_state.get("button_bg", "white"))
b_txt = st.session_state.get("box_txt", st.session_state.get("button_txt", "black"))

# --- 3. THE RE-SYNCHRONIZED LOCKDOWN ---
st.markdown(f"""
    <style>
    /* 1. Main Background */
    .stApp {{ background-color: {bg} !important; }}
    
    /* 2. Global Text Color */
    .stApp *, h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown {{
        color: {txt} !important;
    }}
    
    /* 3. High Contrast Buttons (REVERTED FONT) */
    .stButton > button {{
        background-color: {b_bg} !important;
        color: {b_txt} !important;
        border: 2px solid {txt} !important;
        width: 100% !important; 
        transition: 0.3s;
        /* Removed bold and display:block to restore original font look */
    }}
    .stButton > button * {{ color: {b_txt} !important; }}
    
    /* 4. Input Boxes & Reference Boxes */
    div[data-baseweb="input"], [data-testid="stExpander"], .streamlit-expanderHeader {{
        background-color: {b_bg} !important;
        border: 2px solid {txt} !important;
    }}
    div[data-baseweb="input"] input, [data-testid="stExpander"] * {{
        color: {b_txt} !important;
    }}
    
    /* 5. SIDEBAR LOCKDOWN */
    header, [data-testid="stSidebar"], [data-testid="stSidebarNav"], 
    .stAppHeader, button[kind="header"], [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
    }}

    /* 6. CONTAINER LOCKDOWN */
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
st.title("Fibre Lab 🌿")
st.write("Select a test parameter:")
st.markdown("---")

# 4. THE SECTIONS (Grid Layout)

# --- Row 1 ---
col1, col2 = st.columns(2)
with col1:
    if st.button("Fibre diameter", use_container_width=True):
        st.switch_page("pages/Fibre Diameter.py")
with col2:
    if st.button("Fibre fineness", use_container_width=True):
        st.switch_page("pages/Fibre Fineness.py")

# --- Row 2 ---
col3, col4 = st.columns(2)
with col3:
    if st.button("Fibre Maturity", use_container_width=True):
        st.switch_page("pages/Fibre Maturity.py")
with col4:
    if st.button("Fibre Crimp", use_container_width=True):
        st.switch_page("pages/Fibre Crimp.py")

# --- Row 3 ---
col5, col6 = st.columns(2)
with col5:
    if st.button("Fibre Moisture", use_container_width=True):
        st.switch_page("pages/Fibre Moisture.py")
with col6:
    if st.button("Fibre Length", use_container_width=True):
        st.switch_page("pages/Fibre Length.py")

# --- Row 4 ---
col7, col8 = st.columns(2)
with col7:
    if st.button("Fibre Quality index", use_container_width=True):
        st.switch_page("pages/Fibre Quality Index.py")
with col8:
    if st.button("Spinning consistency Index", use_container_width=True):
        st.switch_page("pages/Spinning Consistency Index.py")

# --- Row 5 ---
col9, col10 = st.columns(2)
with col9:
    if st.button("Trash content", use_container_width=True):
        st.switch_page("pages/Trash content.py")
with col10:
    if st.button("Fibre Bundle Strength", use_container_width=True):
        st.switch_page("pages/Fibre Bundle Strength.py")
