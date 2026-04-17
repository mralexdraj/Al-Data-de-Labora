import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE SETUP
st.set_page_config(page_title="Fabric Lab - Crease Recovery", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Crease Recovery Analysis 📉")

# 3. DEFINITIONS
st.markdown("### **What is Crease Recovery?**")
st.markdown("""
<div style="text-align: justify;">
Crease recovery is the ability of a fabric to return to its original flat state after the removal of a folding or crushing force. When a fabric is creased, the molecular chains within the fibers are displaced; the degree of recovery depends on the fiber's internal elasticity and the stability of its polymer bonds. This property is essential for apparel textiles to maintain a neat appearance during wear and to minimize the need for frequent ironing.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Crease Recovery Angle (CRA)")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Prepare a rectangular fabric specimen (typically 2 inch x 1 inch) and fold it exactly in half.</li>
<li>Place the folded specimen under a <b>2 kg (≈ 19.6 N)</b> load on the Crease Recovery Tester.</li>
<li>Maintain this loading pressure for exactly <b>1 minute</b> to simulate aggressive wrinkling.</li>
<li>Remove the load and transfer the specimen to the measuring dial. Allow the fabric to recover for exactly <b>1 minute</b>.</li>
<li>Rotate the dial to align the recovering edge of the fabric with the vertical pointer and record the Recovery Angle (θ) in degrees.</li>
<li>Repeat the process for both Warp and Weft directions to determine the total cloth performance.</li>
</ol>
</div>
""", unsafe_allow_html=True)



# 5. CALCULATORS

# --- SECTION I: INDIVIDUAL PERCENTAGE ---
st.subheader("2. Recovery Efficiency (%)")
st.latex(r"CR\% = \left( \frac{\theta}{180} \right) \times 100")

target_cr = st.radio(
    "Solve for (Percentage Section):", 
    ["Recovery Percentage (CR%) [%]", "Measured Recovery Angle (θ) [°]"], 
    horizontal=True, key="rcr"
)
col1_in, col1_res = st.columns([3, 1])
res_cr = 0.0
with col1_in:
    if "Percentage" in target_cr:
        theta_in = st.number_input("Measured Recovery Angle (θ) [°]", value=0.0, max_value=180.0, key="th_in")
        if theta_in > 0: res_cr = (theta_in / 180) * 100
    else:
        perc_in = st.number_input("Recovery Percentage (CR%) [%]", value=0.0, max_value=100.0, key="pc_in")
        res_cr = (perc_in / 100) * 180
with col1_res:
    if res_cr > 0:
        unit = " %" if "Percentage" in target_cr else " °"
        st.metric(f"Result: {target_cr.split(' (')[0]}", f"{res_cr:.2f}{unit}")

st.markdown("---")

# --- SECTION II: TOTAL RECOVERY ---
st.subheader("3. Total Crease Recovery (TCR)")
st.latex(r"TCR = \theta_{warp} + \theta_{weft}")

target_tcr = st.radio(
    "Solve for (Total Section):", 
    ["Total Crease Recovery (TCR) [°]", "Required Warp Angle (θw) [°]", "Required Weft Angle (θf) [°]"], 
    horizontal=True, key="rtcr"
)
col2_in, col2_res = st.columns([3, 1])
res_tcr = 0.0
with col2_in:
    if "Total" in target_tcr:
        tw = st.number_input("Warp Recovery Angle (θw) [°]", value=0.0, max_value=180.0, key="tw_in")
        tf = st.number_input("Weft Recovery Angle (θf) [°]", value=0.0, max_value=180.0, key="tf_in")
        res_tcr = tw + tf
    elif "Warp" in target_tcr:
        tcr_v = st.number_input("Target Total Recovery (TCR) [°]", value=0.0, max_value=360.0, key="tcr_in1")
        tf = st.number_input("Known Weft Recovery Angle (θf) [°]", value=0.0, key="tf_in2")
        res_tcr = tcr_v - tf
    else:
        tcr_v = st.number_input("Target Total Recovery (TCR) [°]", value=0.0, max_value=360.0, key="tcr_in2")
        tw = st.number_input("Known Warp Recovery Angle (θw) [°]", value=0.0, key="tw_in2")
        res_tcr = tcr_v - tw

with col2_res:
    if res_tcr > 0:
        st.metric(f"Result: {target_tcr.split(' (')[0]}", f"{res_tcr:.2f}°")

# 6. REFERENCE DATA
st.markdown("---")
with st.expander("📖 View Recovery Quality Grading Table"):
    grade_data = {
        "S/No": [1, 2, 3],
        "TCR (W+F) Range": ["< 150°", "150° – 250°", "250° <"],
        "Recovery Class": ["Poor (High Creasing)", "Fair/Medium", "Excellent (Crease Resistant)"],
        "Typical Fabric": ["Pure Cotton/Linen", "Blends (P/C)", "Synthetics / Resin Treated"]
    }
    st.table(pd.DataFrame(grade_data).set_index("S/No"))

# 7. JUSTIFICATION FOOTER
st.info("""
**Parameters & Justification:**
* **θ (Theta):** The angle measured between the folded limbs of the specimen after recovery time ($0^{\circ}$ is no recovery; $180^{\circ}$ is full recovery).
* **180:** The denominator representing the full $180^{\circ}$ folding arc performed at the start of the test.
* **TCR (Total Crease Recovery):** The cumulative angle of Warp and Weft recovery, providing a holistic view of fabric performance (Max: $360^{\circ}$).
* **2 kg Load:** This "Rapid Lab" weight is higher than the standard 1 kg load to simulate more intense wrinkling conditions for industrial screening.
* **1 Minute Intervals:** The loading and recovery times are synchronized at 60 seconds to ensure repeatable, time-sensitive data collection.
""")