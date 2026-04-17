import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Mode Analysis", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Mode (Frequency Analysis) 🔁")

# 3. DEFINITIONS
st.markdown("### **What is the Mode?**")
st.markdown("""
<div style="text-align: justify;">
The Mode is a measure of central tendency that identifies the value or category that appears most frequently within a given data set. Unlike the mean or median, the mode can be applied to both numerical and categorical data, making it a versatile tool for identifying dominant trends. In textile laboratory analysis, the mode is essential for fault detection—such as identifying the most common type of fabric defect—and for verifying batch consistency. For example, a bimodal distribution (two modes) may indicate that two different fiber lots were accidentally mixed during production.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of the Modal Value")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Assemble the complete set of test readings or observations from the textile sample batch.</li>
<li>Count the number of times each unique value or category appears in the set (Frequency).</li>
<li>Identify the value that possesses the highest frequency count.</li>
<li>If one value dominates, the distribution is "Unimodal"; if two or more values share the highest frequency, the distribution is "Bimodal" or "Multimodal."</li>
<li>For grouped data, identify the 'Modal Class'—the interval with the highest frequency density.</li>
</ol>
</div>
""", unsafe_allow_html=True)



# 5. CALCULATOR SECTION
st.subheader("2. Frequency Lab Calculator")

# Displaying Formula
st.latex(r"\text{Mode} = L + \left( \frac{f_1 - f_0}{(f_1 - f_0) + (f_1 - f_2)} \right) \times h")

# MCP: Radio buttons placed outside and above columns
target_mode = st.radio(
    "Calculation Mode:",
    ["Input Raw Data", "Find Required Frequency for a Mode"],
    horizontal=True,
    key="solver_mode"
)

# MCP: 3:1 Column Ratio
col_main1, col_main2 = st.columns([3, 1])

res_val = 0.0
freq_count = 0

with col_main1:
    if "Raw Data" in target_mode:
        st.markdown("**Enter Lab Readings**")
        num_readings = st.number_input("Number of samples?", min_value=1, max_value=100, value=1, key="n_mode")
        
        # Data editor with 1-based indexing and 0.0 default values
        input_df = pd.DataFrame({"Readings": [0.0] * num_readings})
        input_df.index = range(1, len(input_df) + 1)
        edited_df = st.data_editor(input_df, use_container_width=True, hide_index=False)
        data = edited_df["Readings"].tolist()
        
        # Logic: Filter valid (non-zero) entries
        valid_data = [x for x in data if x != 0]
        if valid_data:
            counts = pd.Series(valid_data).value_counts()
            freq_count = counts.max()
            res_val = counts[counts == freq_count].index.tolist()[0]
            
            st.write("**Frequency Distribution Table:**")
            st.table(counts.rename_index("Value").rename("Frequency"))
            
    else: # Reverse Algebra Logic
        st.markdown("**Required Data Profile Calculation**")
        target_v = st.number_input("Target Modal Value", value=0.0, key="t_mode")
        current_max = st.number_input("Highest Current Frequency of other values", value=0.0, key="c_max")
        if target_v > 0:
            res_val = current_max + 1
            st.write(f"To ensure **{target_v}** becomes the unique Mode, it must appear at least:")

with col_main2:
    st.write("")
    st.write("")
    if res_val > 0:
        label = "Primary Mode" if "Raw Data" in target_mode else "Required Frequency"
        u = "" if "Raw Data" in target_mode else " Times"
        st.metric(f"Result: {label}", f"{res_val:.2f}{u}")

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Justification:**
* **Mode:** The value that occurs with the highest frequency ($f_1$).
* **Unimodal/Bimodal:** A diagnostic tool; bimodal results often point to inconsistent raw materials or machine setting changes mid-batch.
* **Categorical Capability:** Unlike mean/median, the mode is the only measure of central tendency for nominal data (e.g., "Fabric Color: Blue").
* **Reverse Logic:** To change the mode of a set, you must either increase the frequency of the target value or decrease the frequency of the current modal value.
""")

st.info("""
**💡 Fun Fact:** In fashion retail and inventory management, the "Mode" is the most important statistic. Buyers don't look for the "average" size; they look for the modal size—the one most customers actually buy—to decide which garments to stock in the highest quantities.
""")