import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Mean Analysis", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Average (Arithmetic Mean) 🧮")

# 3. DEFINITIONS
st.markdown("### **What is the Arithmetic Mean?**")
st.markdown("""
<div style="text-align: justify;">
The Arithmetic Mean, commonly referred to as the average, is a fundamental measure of central tendency used to identify the "balance point" of a numerical data set. In textile testing and quality control, the mean is utilized to summarize multiple readings—such as yarn strength, fabric GSM, or fiber fineness—into a single representative value for a batch. It provides a quick and effective way to compare test results against industry standards or client specifications, ensuring that the overall production remains within acceptable quality limits.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of the Average Value")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Collect a representative set of samples from the material batch to be tested.</li>
<li>Measure the specific property (e.g., thickness, weight, or count) for each individual sample and record the numerical values accurately.</li>
<li>Calculate the aggregate sum by adding all the individual test readings together ($\sum x$).</li>
<li>Determine the total number of observations or samples tested (n).</li>
<li>Divide the aggregate sum by the number of observations to derive the arithmetic mean.</li>
</ol>
</div>
""", unsafe_allow_html=True)

# 5. CALCULATOR SECTION
st.subheader("2. Mean Analytical Calculator")

st.latex(r"\bar{x} = \frac{\sum x_i}{n}")

# MCP: Radio buttons placed outside and above columns
target_mode = st.radio(
    "Solve for:",
    ["Arithmetic Mean (x̄)", "Total Sum (Σx)", "Number of Samples (n)"],
    horizontal=True,
    key="solver_mean"
)

# MCP: 3:1 Column Ratio
col_main1, col_main2 = st.columns([3, 1])

res_val = 0.0
sum_in, n_in, mean_in = 0.0, 0.0, 0.0

with col_main1:
    if "Arithmetic Mean" in target_mode:
        sum_in = st.number_input("Total Sum of Readings (Σx)", value=0.0, key="sum_1")
        n_in = st.number_input("Number of Samples (n)", value=0.0, key="n_1")
        if n_in > 0:
            res_val = sum_in / n_in
            
    elif "Total Sum" in target_mode:
        mean_in = st.number_input("Target Arithmetic Mean (x̄)", value=0.0, key="mean_2")
        n_in = st.number_input("Number of Samples (n)", value=0.0, key="n_2")
        res_val = mean_in * n_in
        
    else: # Number of Samples
        sum_in = st.number_input("Total Sum of Readings (Σx)", value=0.0, key="sum_3")
        mean_in = st.number_input("Target Arithmetic Mean (x̄)", value=0.0, key="mean_3")
        if mean_in > 0:
            res_val = sum_in / mean_in

with col_main2:
    st.write("")
    st.write("")
    if res_val > 0:
        st.metric(f"Result: {target_mode.split(' (')[0]}", f"{res_val:.3f}")

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Justification:**
* **x̄ (Mean):** The calculated representative value for the data set.
* **Σx (Sigma x):** The sum of all individual data points; represents the total magnitude of the measured property.
* **n (Sample Count):** The total number of independent observations; a higher 'n' generally leads to a more reliable mean.
* **Central Tendency:** The mean is sensitive to every value in the set; however, extreme outliers can significantly pull the "balance point" away from the typical data range.
""")
st.info("""
 **💡Fun Fact:** The word "average" stems from the Old French word *avarie*, which referred to the proportional distribution of financial losses among shippers when cargo was damaged or lost at sea.
""")