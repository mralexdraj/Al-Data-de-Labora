import streamlit as st
import math

# 1. PAGE SETUP
st.set_page_config(page_title="Fiber Crimp Lab", layout="wide", initial_sidebar_state="collapsed")

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
    
    /* 3. High Contrast Buttons */
    .stButton > button {{
        background-color: {b_bg} !important;
        color: {b_txt} !important;
        border: 2px solid {txt} !important;
        width: 100% !important; 
        transition: 0.3s;
    }}
    .stButton > button * {{ color: {b_txt} !important; }}

    /* 4. THE INPUT BOX FIX (Fixes the dark-on-dark numbers/icons) */
    div[data-testid="stNumberInput"] input {{
        color: white !important;
        -webkit-text-fill-color: white !important;
    }}
    div[data-testid="stNumberInput"] button svg {{
        fill: white !important;
    }}
    div[data-testid="stNumberInput"] [data-baseweb="input"] {{
        background-color: #262730 !important;
        border: 1px solid {txt} !important;
        border-radius: 8px !important;
    }}

    /* 5. THE EXPANDER (Reference Box Fix) */
    [data-testid="stExpander"] {{
        border: 1px solid {txt} !important; 
        background-color: transparent !important;
        border-radius: 8px !important;
    }}

    .streamlit-expanderHeader, 
    div[data-testid="stExpander"] > details > summary {{
        background-color: transparent !important;
        color: {txt} !important;
    }}

    .streamlit-expanderHeader p, 
    .streamlit-expanderHeader svg, 
    .streamlit-expanderHeader span {{
        color: {txt} !important;
        fill: {txt} !important;
    }}

    /* 6. THE TABLE GRID (Drawing the Lines) */
    [data-testid="stTable"] td, 
    [data-testid="stTable"] th,
    .stDataFrame td, 
    .stDataFrame th {{
        border: 1px solid {txt} !important; 
        color: {txt} !important;           
        background-color: transparent !important;
    }}

    [data-testid="stTable"], .stDataFrame {{
        border: none !important;
        background-color: transparent !important;
    }}

    /* 7. SIDEBAR & HEADER KILL-SWITCH */
    header, [data-testid="stSidebar"], .stAppHeader, [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
    }}

    /* 8. FULL WIDTH LOCKDOWN */
    .stAppViewContainer {{ width: 100vw !important; max-width: 100vw !important; }}
    [data-testid="stMainBlockContainer"] {{ 
        width: 100% !important; 
        max-width: 100% !important; 
        padding: 1rem 2rem !important; 
    }}
    </style>
""", unsafe_allow_html=True)

# 2. NAVIGATION
col_back, _ = st.columns([1, 8])
with col_back:
    if st.button("⬅ Back"):
        st.switch_page("pages/Fibres' lab selection.py")

st.title("Fiber Crimp Lab 〰️")
st.markdown("### **What is Fiber Crimp?**")

st.write("""
Fiber crimp refers to the natural or artificial waviness, curls, or bends along the length of a fiber. 
It is a crucial quality parameter because it determines the cohesion between fibers during spinning, 
influences the bulk and elasticity of the yarn, and affects the overall feel and warmth of the final textile.
""")

st.markdown("---")

# 3. METHOD 1: DIRECT MEASUREMENT
st.subheader("Crimp Percentage Calculation")

st.markdown("""
**Procedure:**
1. Place a single fiber on a measurement board in its natural, wavy state and record the **Relaxed Length (P)**.
2. Apply a small amount of tension to straighten the fiber without stretching it, then record the **Straightened Length (L)**.
3. Use the length difference to calculate the percentage of crimp relative to the relaxed length.
""")

st.latex(r"Crimp \% = \left( \frac{L - P}{P} \right) \times 100")

# 4. CALCULATOR SECTION
col_c1, col_c2 = st.columns([3, 1])

with col_c1:
    target_crimp = st.radio(
        "Solve for:",
        ["Crimp %", "Straight Length (L)", "Relaxed Length (P)"],
        horizontal=True,
        key="solve_crimp_final"
    )
    
    res_val = 0.0

    if target_crimp == "Crimp %":
        l_in = st.number_input("Straightened Length (L) [mm]", value=0.0, key="l_c1")
        p_in = st.number_input("Relaxed Length (P) [mm]", value=0.0, key="p_c1")
        if p_in > 0:
            res_val = ((l_in - p_in) / p_in) * 100

    elif target_crimp == "Straight Length (L)":
        c_in = st.number_input("Target Crimp %", value=0.0, key="c_l2")
        p_in = st.number_input("Relaxed Length (P) [mm]", value=0.0, key="p_l2")
        res_val = p_in * (1 + (c_in / 100))

    else: # Relaxed Length (P)
        c_in = st.number_input("Target Crimp %", value=0.0, key="c_p3")
        l_in = st.number_input("Straightened Length (L) [mm]", value=0.0, key="l_p3")
        if (1 + (c_in / 100)) > 0:
            res_val = l_in / (1 + (c_in / 100))

with col_c2:
    if res_val != 0:
        unit = "%" if target_crimp == "Crimp %" else " mm"
        st.metric(f"Result: {target_crimp}", f"{res_val:.2f}{unit}")

# 5. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **L (Straightened Length):** The length of the fiber when fully extended under tension.
* **P (Relaxed Length):** The length of the fiber in its natural, crimped state.
* **Crimp %:** The degree of waviness expressed as a percentage of the relaxed length.
        
**Note:** Higher crimp percentages are typical for wool fibers, providing excellent bulk and insulation, whereas lower crimp is seen in smooth fibers like silk or synthetic filaments.
""")