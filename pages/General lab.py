import streamlit as st

# 1. PAGE CONFIG (Enforce Wide Layout)
st.set_page_config(page_title="General Lab", layout="wide", initial_sidebar_state="collapsed")

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
    
    /* 3. High Contrast Buttons (Restored Font Style) */
    .stButton > button {{
        background-color: {b_bg} !important;
        color: {b_txt} !important;
        border: 2px solid {txt} !important;
        width: 100% !important; 
        transition: 0.3s;
    }}
    .stButton > button * {{ color: {b_txt} !important; }}
    
    /* 4. Input Boxes & Reference Boxes (Inversion) */
    div[data-baseweb="input"], [data-testid="stExpander"], .streamlit-expanderHeader {{
        background-color: {b_bg} !important;
        border: 2px solid {txt} !important;
    }}
    div[data-baseweb="input"] input, [data-testid="stExpander"] * {{
        color: {b_txt} !important;
    }}
    
    /* 5. SIDEBAR & HEADER LOCKDOWN (Aggressive Refresh-Proof) */
    header, [data-testid="stSidebar"], [data-testid="stSidebarNav"], 
    .stAppHeader, button[kind="header"], [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
    }}

    /* 6. CONTAINER LOCKDOWN (Ensures Wide Layout across all resolutions) */
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
st.title("General Lab")
st.write("Select a test parameter:")
st.markdown("---")

# 4. THE 4 SECTIONS (Grid Layout)
# We make a 2x2 grid (Two rows, Two columns)

# --- Row 1 ---
col1, col2 = st.columns(2)

with col1:
    if st.button("Average(Mean)", use_container_width=True):
        st.switch_page("pages/Average(Mean).py")

with col2:
    if st.button("Standard Deviation", use_container_width=True):
        st.switch_page("pages/Standard Deviation.py")

# --- Row 2 ---
col3, col4 = st.columns(2)

with col3:
    if st.button("Coefficient of Variation(CV)", use_container_width=True):
        st.switch_page("pages/Coefficient of Variation(CV).py")
with col4:
    if st.button("Median", use_container_width=True):
        st.switch_page("pages/Median.py")

# --- Row 3 ---
col3, col4 = st.columns(2)

with col3:
    if st.button("Mode", use_container_width=True):
        st.switch_page("pages/Mode.py")
with col4:
    if st.button("Percentage Converter", use_container_width=True):
        st.switch_page("pages/Percentage Converter.py")

# --- Row 4 ---
col3, col4 = st.columns(2)

