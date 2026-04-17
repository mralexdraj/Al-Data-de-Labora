import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Percentage Converter", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Percentage Scaling Converter 🔄")

# 3. DEFINITIONS
st.markdown("### **What is Percentage Scaling?**")
st.markdown("""
<div style="text-align: justify;">
Percentage Scaling is the process of converting a raw score or total value into a standardized base of 100. It answers the question: <i>"If the total possible value was 100, what would my current value be?"</i> This is the standard method for calculating academic grades, efficiency ratios in production, and yield percentages in chemical processing. It provides a universal way to compare results from tests or batches that have different total sizes.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Scaled Percentage")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Identify the 'Obtained Value' (the part)—this is the actual score or amount you have measured.</li>
<li>Identify the 'Maximum Value' (the whole)—this is the highest possible value or the total capacity.</li>
<li>Divide the obtained value by the maximum value to find the decimal fraction.</li>
<li>Multiply the resulting decimal by 100 to find the final percentage (%).</li>
<li>To perform reverse calculation, multiply the target percentage by the maximum value and divide by 100.</li>
</ol>
</div>
""", unsafe_allow_html=True)



# 5. CALCULATOR SECTION
st.subheader("2. Scaling Analytical Calculator")

st.latex(r"\% = \left( \frac{\text{Obtained}}{\text{Maximum}} \right) \times 100")

# MCP: Radio buttons placed outside and above columns
target_mode = st.radio(
    "Solve for:",
    ["Percentage (%)", "Obtained Value", "Maximum Possible Value"],
    horizontal=True,
    key="solver_scaling"
)

# MCP: 3:1 Column Ratio
col_main1, col_main2 = st.columns([3, 1])

res_val = 0.0
obt_in, max_in, pct_in = 0.0, 0.0, 0.0

with col_main1:
    if "Percentage" in target_mode:
        obt_in = st.number_input("Obtained Value (e.g., 544 marks)", value=0.0, key="obt_1")
        max_in = st.number_input("Maximum Possible Value (e.g., 600 total)", value=0.0, key="max_1")
        if max_in > 0:
            res_val = (obt_in / max_in) * 100
            
    elif "Obtained" in target_mode:
        pct_in = st.number_input("Target Percentage (%)", value=0.0, key="pct_2")
        max_in = st.number_input("Maximum Possible Value", value=0.0, key="max_2")
        res_val = (pct_in * max_in) / 100
        
    else: # Maximum Value
        obt_in = st.number_input("Obtained Value", value=0.0, key="obt_3")
        pct_in = st.number_input("Percentage (%)", value=0.0, key="pct_3")
        if pct_in > 0:
            res_val = (obt_in * 100) / pct_in

with col_main2:
    st.write("")
    st.write("")
    if res_val > 0:
        u = " %" if "Percentage" in target_mode else ""
        st.metric(f"Result: {target_mode.split(' (')[0]}", f"{res_val:.2f}{u}")

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Justification:**
* **Obtained Value:** The measured component or raw score.
* **Maximum Value:** The baseline representing 100% capacity or the total pool.
* **Ratio Analysis:** By dividing the part by the whole, we derive the 'efficiency' or 'proportion' of the result.
* **Standardization:** Converting to a percentage allows for an apples-to-apples comparison between different datasets (e.g., comparing a score of 18/20 and 45/50).
""")

st.info("""
**💡 Fun Fact:** The "pass mark" in many professional certifications is often scaled to 70% or 75%. This doesn't necessarily mean you got 75% of the questions right, but that your raw total, when converted through this scaling formula, met the required performance threshold!
""")