import streamlit as st
import pandas as pd
import math

# 1. PAGE SETUP
st.set_page_config(page_title="Yarn Strength Lab", layout="wide", initial_sidebar_state="collapsed")

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
        st.switch_page("pages/Yarn's lab selection.py")

st.title("Yarn Strength & CSP Lab 🧶")
st.markdown("### **What is CSP?**")
st.markdown("""
<div style="text-align: justify;">
Count Strength Product (CSP), also known as the Lea Product, is the primary measure of yarn quality in the cotton spinning industry. It is calculated by multiplying the yarn count (English Ne) by the breaking strength of a lea (120 yards) in pounds. A higher CSP indicates superior yarn quality and better spinning efficiency.
</div>
""", unsafe_allow_html=True)
st.markdown("### **What is Tenacity?**")
st.markdown("""
<div style="text-align: justify;">
For scientific comparisons across different yarn thicknesses, Tenacity is used. It represents the breaking force relative to the linear density, measured in centi-Newtons per tex (cN/tex). The centi-Newton (cN) is used because it approximately equals the force exerted by a 1-gram mass, making it a practical unit for textile testing.
</div>
""", unsafe_allow_html=True)


st.markdown("---")

# 3. METHODOLOGY
st.subheader("1. Lea Strength Determination")
st.markdown("""
**Procedure:**
1. Prepare a yarn lea (120 yards) using a standard wrap reel.
2. Place the lea on the hooks of a Lea Strength Tester.
3. Apply force until the lea breaks and record the **Breaking Strength in pounds (lbs)**.
4. Calculate the CSP by multiplying this strength value by the **English Count (Ne)** of the yarn.
""")

# 4. CALCULATORS

# --- A. CSP & LEA STRENGTH ---
st.subheader("2. CSP Analytical Calculator")

st.latex(r"CSP = Count \ (Ne) \times Strength \ (lbs)")

target_csp = st.radio(
    "Solve for:",
    ["CSP", "Yarn Strength (lbs)", "Yarn Count (Ne)"],
    horizontal=True,
    key="solve_csp_master"
)

col_s1, col_s2 = st.columns([3, 1])

# Initialize Gatekeepers
ne_g, lbs_g, csp_g = 0.0, 0.0, 0.0

with col_s1:
    if target_csp == "CSP":
        ne_g = st.number_input("Yarn Count (Ne)", value=0.0, key="ne_v1")
        lbs_g = st.number_input("Lea Strength (lbs)", value=0.0, key="lbs_v1")
        res_val = ne_g * lbs_g
        
    elif target_csp == "Yarn Strength (lbs)":
        csp_g = st.number_input("Known CSP", value=0.0, key="csp_v2")
        ne_g = st.number_input("Yarn Count (Ne)", value=0.0, key="ne_v2")
        res_val = csp_g / ne_g if ne_g > 0 else 0.0

    else: # Yarn Count (Ne)
        csp_g = st.number_input("Known CSP", value=0.0, key="csp_v3")
        lbs_g = st.number_input("Lea Strength (lbs)", value=0.0, key="lbs_v3")
        res_val = csp_g / lbs_g if lbs_g > 0 else 0.0

with col_s2:
    if (ne_g > 0 or lbs_g > 0 or csp_g > 0):
        unit = " lbs" if "Strength" in target_csp else (" Ne" if "Count" in target_csp else "")
        st.metric(f"Result: {target_csp}", f"{res_val:.2f}{unit}")

st.markdown("---")

# --- B. YARN TENACITY ---
st.subheader("3. Yarn Tenacity Analysis")
st.latex(r"Tenacity \ (cN/tex) = \frac{Breaking \ Force \ (cN)}{Linear \ Density \ (tex)}")

# Target Selector for Reverse Algebra
target_ten = st.radio(
    "Solve for (Tenacity Section):",
    ["Tenacity (cN/tex)", "Breaking Force (cN)", "Linear Density (tex)"],
    horizontal=True,
    key="solve_ten_reverse"
)

col_t1, col_t2 = st.columns([3, 1])

# Initialize Gatekeepers
cn_g, tex_g, ten_g = 0.0, 0.0, 0.0

with col_t1:
    if target_ten == "Tenacity (cN/tex)":
        cn_g = st.number_input("Breaking Force [cN]", value=0.0, key="cn_v1")
        tex_g = st.number_input("Linear Density [tex]", value=0.0, key="tex_v1")
        res_ten = cn_g / tex_g if tex_g > 0 else 0.0
        
    elif target_ten == "Breaking Force (cN)":
        ten_g = st.number_input("Known Tenacity [cN/tex]", value=0.0, key="ten_v2")
        tex_g = st.number_input("Linear Density [tex]", value=0.0, key="tex_v2")
        res_ten = ten_g * tex_g

    else: # Linear Density (tex)
        cn_g = st.number_input("Breaking Force [cN]", value=0.0, key="cn_v3")
        ten_g = st.number_input("Known Tenacity [cN/tex]", value=0.0, key="ten_v3")
        res_ten = cn_g / ten_g if ten_g > 0 else 0.0

with col_t2:
    # Result Display Guard
    if (cn_g > 0 or tex_g > 0 or ten_g > 0):
        unit_ten = " cN/tex" if "Tenacity" in target_ten else (" cN" if "Force" in target_ten else " tex")
        st.metric(f"Result: {target_ten}", f"{res_ten:.2f}{unit_ten}")

# 5. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **CSP:** Count Strength Product; a dimensionless value used to grade cotton yarn.
* **Lea Strength (lbs):** The total force required to break a 120-yard loop of yarn.
* **Breaking Force (cN):** The tension at which a single yarn strand breaks, measured in centi-Newtons.
* **Tenacity (cN/tex):** The breaking force per unit linear density, allowing comparison between different counts.
* **1 cN:** Approximately equal to the gravitational force on 1.02 grams.
""")