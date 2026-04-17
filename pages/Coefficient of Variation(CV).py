import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="CV% Analysis", layout="wide", initial_sidebar_state="collapsed")

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
        st.switch_page("pages/General lab.py")

st.title("Coefficient of Variation (CV%) 📈")

# 3. DEFINITIONS
st.markdown("### **What is the Coefficient of Variation?**")
st.markdown("""
<div style="text-align: justify;">
The Coefficient of Variation (CV%) is a relative measure of dispersion that expresses the Standard Deviation as a percentage of the Mean. While Standard Deviation provides the absolute spread of data in its original units, CV% provides a dimensionless ratio that allows for the direct comparison of variability between different data sets, even if they have significantly different means or units of measurement. In the textile industry, CV% is the gold standard for defining quality levels, as it reveals the "uniformity" of properties like yarn count, mass, and strength across varying specifications.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Relative Variability")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Collect a comprehensive set of lab readings for the specific textile property being tested.</li>
<li>Calculate the Arithmetic Mean ($\bar{x}$) for the data set to establish the central reference point.</li>
<li>Calculate the Standard Deviation ($\sigma$) to determine the absolute dispersion of the readings.</li>
<li>Divide the Standard Deviation by the Mean to obtain the fractional variation.</li>
<li>Multiply the resulting fraction by 100 to convert it into the final CV% value.</li>
</ol>
</div>
""", unsafe_allow_html=True)



# 5. CALCULATOR SECTION
st.subheader("2. CV% Analytical Calculator")

st.latex(r"CV\% = \left( \frac{\sigma}{\bar{x}} \right) \times 100")

# MCP: Radio buttons placed outside and above columns
target_mode = st.radio(
    "Solve for:",
    ["Coefficient of Variation (CV%) [%]", "Standard Deviation (σ)", "Arithmetic Mean (x̄)"],
    horizontal=True,
    key="solver_cv"
)

# MCP: 3:1 Column Ratio
col_main1, col_main2 = st.columns([3, 1])

res_val = 0.0
sd_in, mean_in, cv_in = 0.0, 0.0, 0.0

with col_main1:
    if "CV%" in target_mode:
        sd_in = st.number_input("Standard Deviation (σ)", value=0.0, format="%.4f", key="sd_1")
        mean_in = st.number_input("Arithmetic Mean (x̄)", value=0.0, format="%.4f", key="mean_1")
        if mean_in > 0:
            res_val = (sd_in / mean_in) * 100
            
    elif "Standard Deviation" in target_mode:
        cv_in = st.number_input("Target CV% [%]", value=0.0, key="cv_2")
        mean_in = st.number_input("Arithmetic Mean (x̄)", value=0.0, format="%.4f", key="mean_2")
        res_val = (cv_in * mean_in) / 100
        
    else: # Arithmetic Mean
        cv_in = st.number_input("Target CV% [%]", value=0.0, key="cv_3")
        sd_in = st.number_input("Standard Deviation (σ)", value=0.0, format="%.4f", key="sd_3")
        if cv_in > 0:
            res_val = (sd_in / cv_in) * 100

with col_main2:
    st.write("")
    st.write("")
    if res_val > 0:
        u = " %" if "CV%" in target_mode else ""
        st.metric(f"Result: {target_mode.split(' (')[0]}", f"{res_val:.3f}{u}")

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Justification:**
* **CV% (Coefficient of Variation):** A standardized measure of dispersion. It allows for a "fair" comparison of consistency between coarse and fine yarns (e.g., comparing 20s Ne and 80s Ne).
* **σ (Standard Deviation):** The absolute measure of spread.
* **x̄ (Mean):** The average value; used as the denominator to normalize the deviation.
* **Dimensionless Property:** Because the units in the numerator and denominator cancel out, CV% is a pure percentage, making it independent of the scale of measurement.
""")

st.info("""
**💡 Fun Fact:** In the world of high-speed yarn spinning (Uster testing), CV% is often called the "Unevenness" parameter. If the CV% of a yarn exceeds certain "Uster Statistics" thresholds, it is classified as "irregular," which can lead to visible streaks (barré) in the final knitted or woven fabric.
""")