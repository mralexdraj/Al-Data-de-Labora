import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Air Permeability", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Air Permeability & Resistance Lab 🌬️")

# 3. DEFINITIONS
st.markdown("### **Understanding Airflow in Textiles**")
st.markdown("""
<div style="text-align: justify;">
Air Permeability is a measure of how easily air can pass through a fabric, defined as the volume of air that passes vertically through a given area of the fabric under a specified pressure difference over a specific time. Conversely, Air Resistance is the opposition offered by the fabric structure to this flow. These parameters are essential for technical textiles, sportswear, and industrial filters, where breathability or filtration efficiency is a primary performance requirement.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Air Permeability")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Mount the fabric specimen securely over the test orifice of the Air Permeability Tester, ensuring a leak-proof seal at the edges.</li>
<li>Start the vacuum pump or air blower to create a pressure differential across the fabric (standard test pressures are typically 100 Pa or 200 Pa).</li>
<li>The instrument's sensors detect the resistance offered by the fabric structure to the airflow, often displayed as a pressure drop or resistance value (kPa·s/m).</li>
<li>Use the recorded resistance or flow rate to calculate the final permeability value, which represents the volume of air passing through a unit area per unit time.</li>
</ol>
</div>
""", unsafe_allow_html=True)

st.latex(r"V = \frac{124.55}{R \times 1000 \times 10^{-2}}")

# 5. CALCULATOR SECTION
st.subheader("2. Air Permeability Analytical Calculator")

target_mode = st.radio(
    "Solve for:",
    ["Air Permeability (V) [cm³/cm²/s]", "Air Resistance (R) [kPa·s/m]"],
    horizontal=True,
    key="solver_air_perm_exact_match"
)

col_main1, col_main2 = st.columns([3, 1])

res_val = 0.0
numerator = 124.55
full_factor = 1000 * (10**-2)

with col_main1:
    if "Air Permeability" in target_mode:
        r_in = st.number_input("Air Resistance (R) [kPa·s/m]", value=0.0, format="%.4f", key="r_val")
        if r_in > 0:
            res_val = numerator / (r_in * full_factor)
    else:
        v_in = st.number_input("Air Permeability (V) [cm³/cm²/s]", value=0.0, format="%.4f", key="v_val")
        if v_in > 0:
            res_val = numerator / (v_in * full_factor)

with col_main2:
    if res_val > 0:
        unit_label = " cm³/cm²/s" if "Permeability" in target_mode else " kPa·s/m"
        display_label = target_mode.split(' (')[0]
        # HTML output with identical font metrics to standard Streamlit components
        st.markdown(f"""
            <div class="custom-metric-container">
                <div class="custom-metric-label">Result: {display_label}</div>
                <div class="custom-metric-value">{res_val:.4f}{unit_label}</div>
            </div>
        """, unsafe_allow_html=True)

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **V (Air Permeability):** The volume of air passing through a unit area of fabric per second [$cm^3/cm^2/s$].
* **R (Air Resistance):** The opposition offered by the fabric to airflow [$kPa·s/m$].
* **124.55:** A technical constant derived from the fluid dynamics of air passing through porous textile structures.
* **1000:** The conversion factor used to normalize kilopascals [$kPa$] within the specific volume calculation.
* **10⁻²:** The scaling factor required to align the units of area and time between the resistance measurement and the permeability result.
""")