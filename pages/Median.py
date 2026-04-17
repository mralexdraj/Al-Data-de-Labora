import streamlit as st
import numpy as np
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Median Analysis", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Median (Middle Value) 🎯")

# 3. DEFINITIONS
st.markdown("### **What is the Median?**")
st.markdown("""
<div style="text-align: justify;">
The Median is a measure of central tendency that represents the exact middle value in a data set when the observations are arranged in order of magnitude. Unlike the arithmetic mean, the median is a "robust" statistic, meaning it is not significantly influenced by extreme outliers or skewed data. In textile testing, the median is particularly useful when analyzing parameters like yarn breakage or localized defects, where a single mechanical failure might produce an extreme reading that would otherwise distort the average and misrepresent the typical performance of the batch.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of the Median Position")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Collect all numerical readings from the textile test specimens.</li>
<li>Arrange the data points in ascending order (from lowest to highest value).</li>
<li>Count the total number of observations (n) in the data set.</li>
<li>If the total count (n) is an odd number, the median is the value located at the exact center position: $(n+1)/2$.</li>
<li>If the total count (n) is an even number, identify the two central values and calculate their average to find the median.</li>
</ol>
</div>
""", unsafe_allow_html=True)



# 5. CALCULATOR SECTION
st.subheader("2. Median Analytical Calculator")

# Displaying Formula
st.latex(r"\text{Position (L)} = \frac{n + 1}{2}")

# MCP: Radio buttons placed outside and above columns
target_mode = st.radio(
    "Calculation Mode:",
    ["Calculate from Raw Data", "Find Required Center Values"],
    horizontal=True,
    key="solver_median"
)

# MCP: 3:1 Column Ratio
col_main1, col_main2 = st.columns([3, 1])

res_val = 0.0
sorted_data = []

with col_main1:
    if "Raw Data" in target_mode:
        st.markdown("**Enter Lab Readings**")
        # Step 1: User selects number of samples
        num_readings = st.number_input("Number of samples?", min_value=1, max_value=100, value=3, key="n_med")
        
        # Step 2: Create and display the table (data_editor)
        input_df = pd.DataFrame({"Readings": [0.0] * num_readings})
        input_df.index = range(1, len(input_df) + 1)
        edited_df = st.data_editor(input_df, use_container_width=True, hide_index=False, key="med_table")
        
        # Step 3: Calculation logic
        data = edited_df["Readings"].tolist()
        if any(v > 0 for v in data):
            sorted_data = sorted(data)
            res_val = np.median(sorted_data)
            st.write("**Sorted Sequence:**")
            st.info(f"{sorted_data}")
                
    else: # Reverse Algebra Logic
        st.markdown("**Determine Middle Values for Target Median**")
        target_med = st.number_input("Desired Median Value", value=0.0, key="t_med")
        val_lower = st.number_input("Lower Neighboring Value (for even n)", value=0.0, key="v_low")
        if target_med > 0 and val_lower > 0:
            # Logic: Target = (Lower + Upper) / 2 -> Upper = (2 * Target) - Lower
            res_val = (2 * target_med) - val_lower
            st.write(f"To achieve a median of **{target_med}**, the upper neighboring value must be:")

with col_main2:
    st.write("")
    st.write("")
    if res_val > 0:
        label = "Median Value" if "Raw Data" in target_mode else "Required Upper Value"
        st.metric(f"Result: {label}", f"{res_val:.2f}")

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Justification:**
* **n (Sample Size):** Determines the mathematical approach (Odd vs. Even count).
* **Sorted Order:** Essential for identifying position; the magnitude of values on either side of the median does not affect its value, only their count.
* **Robustness:** The median remains the "center" even if the largest value in the set is doubled, making it ideal for data with high variability.
* **Reverse Logic:** To shift the median, data points must be added or modified specifically around the central index of the ordered set.
""")

st.info("""
**💡 Fun Fact:** The median is used in the textile industry's "Standardized Fiber Length" reports. Because fiber length distributions are often skewed by short fibers, the median (or 50% Span Length) gives a more realistic view of the fiber "staple" than the simple arithmetic average.
""")