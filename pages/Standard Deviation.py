import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE SETUP
st.set_page_config(page_title="Standard Deviation Analysis", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Standard Deviation (σ) 📏")

# 3. DEFINITIONS
st.markdown("### **What is Standard Deviation?**")
st.markdown("""
<div style="text-align: justify;">
Standard Deviation (σ) is a statistical measure that quantifies the amount of variation or dispersion within a set of data values. In textile quality control, it represents the level of consistency in production; a low standard deviation indicates that the data points tend to be very close to the mean, signifying high uniformity in properties like yarn strength or fabric weight. Conversely, a high standard deviation indicates that the data points are spread out over a wider range, which often alerts lab technicians to potential machine errors, raw material blending issues, or process instability.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Statistical Variation")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Perform a series of independent tests on a specified number of textile samples (n).</li>
<li>Record each individual test reading ($x_i$) into the data table.</li>
<li>Calculate the Arithmetic Mean ($\bar{x}$) of the collected data set.</li>
<li>Subtract the mean from each individual reading to determine the 'Deviation' for each data point.</li>
<li>Square each deviation to eliminate negative values and calculate the sum of these squared deviations.</li>
<li>Divide the total sum of squares by the degrees of freedom (n - 1) and calculate the square root to derive the Standard Deviation.</li>
</ol>
</div>
""", unsafe_allow_html=True)



# 5. CALCULATOR SECTION
st.subheader("2. Standard Deviation Analytical Calculator")

st.latex(r"s = \sqrt{\frac{\sum (x_i - \bar{x})^2}{n - 1}}")

# MCP: Radio buttons placed outside and above columns
target_mode = st.radio(
    "Calculation Mode:",
    ["Input Raw Data", "Find Required Sum of Squares (SS)"],
    horizontal=True,
    key="solver_sd"
)

# MCP: 3:1 Column Ratio
col_main1, col_main2 = st.columns([3, 1])

res_sd = 0.0
res_mean = 0.0

with col_main1:
    if target_mode == "Input Raw Data":
        st.markdown("**Enter Lab Readings**")
        num_readings = st.number_input("Number of samples?", min_value=2, max_value=50, value=2)
        
        # Data editor with corrected 1-based indexing
        input_df = pd.DataFrame({"Readings": [0.0] * num_readings})
        input_df.index = range(1, len(input_df) + 1)
        edited_df = st.data_editor(input_df, use_container_width=True, hide_index=False)
        data = edited_df["Readings"].tolist()
        
        if any(v > 0 for v in data):
            res_mean = np.mean(data)
            res_sd = np.std(data, ddof=1)
            
    else: # Reverse Algebra Mode
        st.markdown("**Required Profile Calculation**")
        n_val = st.number_input("Sample Count (n)", value=0.0, key="n_rev")
        target_v = st.number_input("Target Standard Deviation (σ)", value=0.0, key="sd_rev")
        if n_val > 1:
            res_sd = (target_v**2) * (n_val - 1)

with col_main2:
    st.write("")
    st.write("")
    if res_sd > 0:
        if target_mode == "Input Raw Data":
            st.metric("Mean (x̄)", f"{res_mean:.3f}")
            st.metric("SD (σ)", f"{res_sd:.4f}")
        else:
            st.metric("Required SS", f"{res_sd:.2f}")

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Justification:**
* **s (Sample SD):** Used when the test group is a subset of the total production (incorporates Bessel's Correction).
* **x̄ (Mean):** The central reference point from which all deviations are measured.
* **n - 1:** The 'Degrees of Freedom'; dividing by $n-1$ instead of $n$ provides a less biased estimate for small sample sizes.
* **Sum of Squares (SS):** Represents the total aggregate of all squared deviations; it is the raw measure of total variability before normalization.
""")
st.info("""
 **💡Fun Fact:** The concept of Standard Deviation was first introduced by Karl Pearson in 1894, although the Greek letter sigma ($\sigma$) was already being used by astronomers to describe errors in observation long before, it became a staple of modern statistics.
""")