import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE SETUP
st.set_page_config(page_title="Color Strength Lab", layout="wide", initial_sidebar_state="collapsed")

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
        st.switch_page("pages/Processing's lab selection.py")

st.title("Color Strength Analysis (K/S) 🎨")

# 3. DEFINITIONS
st.markdown("### **What is Color Strength?**")
st.markdown("""
<div style="text-align: justify;">
Color strength is a numerical measure of the ability of a dye or pigment to impart color to a substrate. It is fundamentally calculated using the <b>Kubelka-Munk Theory</b>, which establishes a relationship between the light reflectance of a dyed fabric and the concentration of the dye present within the fiber. By calculating the K/S value (where K is absorption and S is scattering), lab technicians can quantify shade depth objectively, allowing for precise shade matching, recipe formulation, and quality control between different dye batches.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Color Strength")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Calibrate the spectrophotometer using standard white and black tiles.</li>
<li>Place the dyed fabric specimen flat against the measurement aperture, ensuring sufficient thickness (folding the fabric) to prevent light transmission through the sample.</li>
<li>Measure the reflectance (R) of the sample at the wavelength of maximum absorption (λmax).</li>
<li>Convert the reflectance percentage into a decimal value to calculate the absolute K/S value.</li>
<li>For relative strength, compare the K/S of the current batch (Sample) against an approved reference (Standard) to determine the percentage deviation.</li>
</ol>
</div>
""", unsafe_allow_html=True)



# 5. CALCULATORS

# --- SECTION I: KUBELKA-MUNK ---
st.subheader("2. Kubelka-Munk Calculation")
st.latex(r"K/S = \frac{(1 - R)^2}{2R}")

# MCP: Radio buttons placed outside and above columns
target_ks = st.radio(
    "Solve for (K/S Section):",
    ["Color Strength (K/S) [Value]", "Reflectance (R) [%]"],
    horizontal=True,
    key="solver_ks"
)

col1_in, col1_res = st.columns([3, 1])
res_ks = 0.0

with col1_in:
    if "K/S" in target_ks:
        r_perc = st.number_input("Reflectance (R) [%]", value=0.0, max_value=100.0, format="%.2f", key="r_in")
        if r_perc > 0:
            r_dec = r_perc / 100
            res_ks = ((1 - r_dec)**2) / (2 * r_dec)
    else:
        ks_in = st.number_input("Color Strength (K/S) [Value]", value=0.0, format="%.4f", key="ks_in")
        if ks_in > 0:
            # Reverse Algebra: R = (K/S + 1) - sqrt((K/S + 1)^2 - 1)
            r_dec = (ks_in + 1) - np.sqrt((ks_in + 1)**2 - 1)
            res_ks = r_dec * 100

with col1_res:
    st.write("")
    st.write("")
    if res_ks > 0:
        u = "" if "K/S" in target_ks else " %"
        st.metric(f"Result: {target_ks.split(' (')[0]}", f"{res_ks:.4f}{u}")

st.markdown("---")

# --- SECTION II: RELATIVE STRENGTH ---
st.subheader("3. Relative Color Strength (%)")
st.latex(r"Strength\% = \left( \frac{(K/S)_{Sample}}{(K/S)_{Standard}} \right) \times 100")

# MCP: Radio buttons placed outside and above columns
target_rel = st.radio(
    "Solve for (Relative Section):",
    ["Relative Strength [%]", "Sample K/S [Value]", "Standard K/S [Value]"],
    horizontal=True,
    key="solver_rel"
)

col2_in, col2_res = st.columns([3, 1])
res_rel = 0.0

with col2_in:
    if "Relative Strength" in target_rel:
        ks_std = st.number_input("Standard Color Strength (K/S_std)", value=0.0, format="%.4f", key="ks_s1")
        ks_sam = st.number_input("Sample Color Strength (K/S_sam)", value=0.0, format="%.4f", key="ks_sam1")
        if ks_std > 0:
            res_rel = (ks_sam / ks_std) * 100
    elif "Sample" in target_rel:
        rel_in = st.number_input("Relative Strength [%]", value=0.0, key="rel_in2")
        ks_std = st.number_input("Standard Color Strength (K/S_std)", value=0.0, format="%.4f", key="ks_s2")
        res_rel = (rel_in / 100) * ks_std
    else:
        rel_in = st.number_input("Relative Strength [%]", value=0.0, key="rel_in3")
        ks_sam = st.number_input("Sample Color Strength (K/S_sam)", value=0.0, format="%.4f", key="ks_sam3")
        if rel_in > 0:
            res_rel = (ks_sam * 100) / rel_in

with col2_res:
    st.write("")
    st.write("")
    if res_rel > 0:
        u = " %" if "Relative Strength" in target_rel else ""
        st.metric(f"Result: {target_rel.split(' [')[0]}", f"{res_rel:.2f}{u}")

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Justification:**
* **K (Absorption Coefficient):** Represents the ability of the dye molecules to absorb light energy.
* **S (Scattering Coefficient):** Represents the ability of the fiber substrate to scatter light.
* **R (Reflectance):** The fraction of incident light reflected by the sample. As dye concentration increases, reflectance decreases.
* **K/S Value:** This value is directly proportional to dye concentration on the fiber, unlike raw reflectance which is non-linear.
* **Wavelength of λmax:** Measurements are taken at the wavelength where the dye absorbs the most light to ensure maximum sensitivity.
* **Tolerance Note:** In industrial dyeing, a batch is generally accepted if the Relative Strength is within 95% to 105% of the standard.
""")