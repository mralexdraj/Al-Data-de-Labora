import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Fabric Strength Lab", layout="wide", initial_sidebar_state="collapsed")

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
        st.switch_page("pages/Fabric's lab selection.py")

st.title("Fabric Strength & Tenacity Lab 🔬")

# 3. DEFINITIONS
st.subheader("What is Fabric Strength?")
st.markdown("""
<div style="text-align: justify;">
<b>Tensile Strength (Breaking Strength):</b> This is the maximum force a specific width of fabric can withstand before it ruptures. It is the industry standard for commercial trade and quality control (ISO 13934-1). It does not account for fabric weight, focusing only on the total breaking point for a specific strip width.
<br><br>
<b>Tenacity (Specific Strength):</b> A research-oriented metric used to compare fabrics of different weights. By involving the GSM, this value "normalizes" the result, representing how strong the fibers and weave are intrinsically, regardless of whether the fabric is heavy or light.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. CALCULATORS

# --- SECTION 1: TENSILE STRENGTH (INDUSTRY STANDARD) ---
st.subheader("1. Tensile Strength (Breaking Strength)")
st.latex(r"S = \frac{F}{W}")

# Reverse Algebra Selector
target_s = st.radio("Solve for (Tensile Section):", ["Tensile Strength (N/cm)", "Breaking Force (N)", "Width (cm)"], horizontal=True, key="solve_s")

col_s1, col_s2 = st.columns([3, 1])
# Initialize gatekeepers
f_s, w_s, s_v = 0.0, 0.0, 0.0

with col_s1:
    if target_s == "Tensile Strength (N/cm)":
        f_s = st.number_input("Breaking Force [N]", value=0.0, key="fs1")
        w_s = st.number_input("Fabric Strip Width [cm]", value=0.0, key="ws1")
        res_s = f_s / w_s if w_s > 0 else 0.0
    elif target_s == "Breaking Force (N)":
        s_v = st.number_input("Known Tensile Strength [N/cm]", value=0.0, key="sv2")
        w_s = st.number_input("Fabric Strip Width [cm]", value=0.0, key="ws2")
        res_s = s_v * w_s
    else: # Width
        f_s = st.number_input("Breaking Force [N]", value=0.0, key="fs3")
        s_v = st.number_input("Known Tensile Strength [N/cm]", value=0.0, key="sv3")
        res_s = f_s / s_v if s_v > 0 else 0.0

with col_s2:
    if (f_s > 0 or w_s > 0 or s_v > 0):
        u = " N/cm" if "Strength" in target_s else (" N" if "Force" in target_s else " cm")
        st.metric(f"Result: {target_s}", f"{res_s:.2f}{u}")

st.info("**Formula Note:** $F$ is Breaking Force in Newtons (N) and $W$ is the Width of the strip in Centimeters (cm).")

st.markdown("---")

# --- SECTION 2: TENACITY (RESEARCH STANDARD) ---
st.subheader("2. Tenacity (Specific Strength)")
st.latex(r"T = \frac{F \times 100}{GSM \times W}")

# Reverse Algebra Selector
target_t = st.radio("Solve for (Tenacity Section):", ["Tenacity (cN/tex)", "Breaking Force (cN)", "Fabric GSM", "Width (m)"], horizontal=True, key="solve_t")

col_t1, col_t2 = st.columns([3, 1])
# Initialize gatekeepers
f_t, gsm_t, w_t, t_v = 0.0, 0.0, 0.0, 0.0

with col_t1:
    if target_t == "Tenacity (cN/tex)":
        f_t = st.number_input("Breaking Force [cN]", value=0.0, key="ft1")
        gsm_t = st.number_input("Fabric GSM [g/m²]", value=0.0, key="gt1")
        w_t = st.number_input("Sample Width [m]", value=0.0, key="wt1")
        res_t = (f_t * 100) / (gsm_t * w_t) if (gsm_t > 0 and w_t > 0) else 0.0
    elif target_t == "Breaking Force (cN)":
        t_v = st.number_input("Known Tenacity [cN/tex]", value=0.0, key="tv2")
        gsm_t = st.number_input("Fabric GSM [g/m²]", value=0.0, key="gt2")
        w_t = st.number_input("Sample Width [m]", value=0.0, key="wt2")
        res_t = (t_v * gsm_t * w_t) / 100
    elif target_t == "Fabric GSM":
        t_v = st.number_input("Known Tenacity [cN/tex]", value=0.0, key="tv3")
        f_t = st.number_input("Breaking Force [cN]", value=0.0, key="ft3")
        w_t = st.number_input("Sample Width [m]", value=0.0, key="wt3")
        res_t = (f_t * 100) / (t_v * w_t) if (t_v > 0 and w_t > 0) else 0.0
    else: # Width
        t_v = st.number_input("Known Tenacity [cN/tex]", value=0.0, key="tv4")
        f_t = st.number_input("Breaking Force [cN]", value=0.0, key="ft4")
        gsm_t = st.number_input("Fabric GSM [g/m²]", value=0.0, key="gt4")
        res_t = (f_t * 100) / (t_v * gsm_t) if (t_v > 0 and gsm_t > 0) else 0.0

with col_t2:
    if (f_t > 0 or gsm_t > 0 or w_t > 0 or t_v > 0):
        u = " cN/tex" if "Tenacity" in target_t else (" cN" if "Force" in target_t else (" g/m²" if "GSM" in target_t else " m"))
        st.metric(f"Result: {target_t}", f"{res_t:.2f}{u}")

st.info("**Unit Constants:** $F$ is in cN, $W$ in meters. The **100** is a conversion factor to balance the units for Tex calculation ($GSM \times W \times 1000$ represents linear density).")

# 5. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **Breaking Force:** The peak tension recorded by the load cell during rupture.
* **GSM:** Grams per Square Meter; represents the fabric's mass per unit area.
* **Tex (Linear Density):** In fabric testing, the equivalent linear density of the test strip is $GSM \times Width$.
* **N vs cN:** Industry uses Newtons (N), while R&D often uses centiNewtons (cN) for finer precision equivalent to 1 gram-force.
""")