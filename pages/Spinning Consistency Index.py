import streamlit as st
import pandas as pd
import math

# 1. PAGE SETUP
st.set_page_config(page_title="Fiber Lab - SCI", layout="wide", initial_sidebar_state="collapsed")

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
        st.switch_page("pages/Fibres' lab selection.py")

st.title("Spinning Consistency Index (SCI) 🧵")
st.markdown("### **What is SCI?**")
st.markdown("""
<div style="text-align: justify;">
The Spinning Consistency Index (SCI) is a comprehensive quality rating for cotton. Instead of evaluating properties like length or strength in isolation, the SCI uses a multiple regression equation to blend all key fiber properties into a single value. This index is highly effective in predicting the overall spinnability and performance of the cotton during manufacturing.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 3. METHODOLOGY
st.subheader("1. SCI Regression Analysis")
st.markdown("""
**Procedure:**
1. Measure fiber properties using HVI (High Volume Instrument) testing.
2. Identify the six key parameters: Strength, Length (UHML), Uniformity, Micronaire, Reflectance, and Yellowness.
3. Apply the regression equation to determine the single index value.
""")

st.latex(r"SCI = -414.67 + 2.9S + 49.17L + 4.74UI - 9.32Mic + 0.65Rd + 0.36(+b)")

# 4. CALCULATOR SECTION
st.subheader("2. SCI Analytical Calculator")

target_sci = st.radio(
    "Solve for:",
    ["SCI Value", "Strength (S)", "Length (L)", "Uniformity (UI)", "Micronaire (Mic)"],
    horizontal=True,
    key="solve_sci_master"
)

col_main1, col_main2 = st.columns([3, 1])

# Constants for Calculation
C = -414.67

# INITIALIZE GATEKEEPERS TO PREVENT NAMEERROR
s, l, sci = 0.0, 0.0, 0.0

with col_main1:
    if target_sci == "SCI Value":
        s = st.number_input("Strength (S) [g/tex]", value=0.0, key="s_v")
        l = st.number_input("Length (UHML) [mm]", value=0.0, key="l_v")
        ui = st.number_input("Uniformity (UI) [%]", value=0.0, key="ui_v")
        mic = st.number_input("Micronaire (Mic) [µg/inch]", value=0.0, key="mic_v")
        rd = st.number_input("Reflectance (Rd)", value=0.0, key="rd_v")
        b = st.number_input("Yellowness (+b)", value=0.0, key="b_v")
        res_sci = C + (2.9*s) + (49.17*l) + (4.74*ui) - (9.32*mic) + (0.65*rd) + (0.36*b)
        
    elif target_sci == "Strength (S)":
        sci = st.number_input("Target SCI Value", value=0.0, key="sci_s")
        l = st.number_input("Length (UHML) [mm]", value=0.0, key="l_s")
        ui = st.number_input("Uniformity (UI) [%]", value=0.0, key="ui_s")
        mic = st.number_input("Micronaire (Mic) [µg/inch]", value=0.0, key="mic_s")
        rd = st.number_input("Reflectance (Rd)", value=0.0, key="rd_s")
        b = st.number_input("Yellowness (+b)", value=0.0, key="b_s")
        res_sci = (sci - C - (49.17*l) - (4.74*ui) + (9.32*mic) - (0.65*rd) - (0.36*b)) / 2.9

    elif target_sci == "Length (L)":
        sci = st.number_input("Target SCI Value", value=0.0, key="sci_l")
        s = st.number_input("Strength (S) [g/tex]", value=0.0, key="s_l")
        ui = st.number_input("Uniformity (UI) [%]", value=0.0, key="ui_l")
        mic = st.number_input("Micronaire (Mic) [µg/inch]", value=0.0, key="mic_l")
        rd = st.number_input("Reflectance (Rd)", value=0.0, key="rd_l")
        b = st.number_input("Yellowness (+b)", value=0.0, key="b_l")
        res_sci = (sci - C - (2.9*s) - (4.74*ui) + (9.32*mic) - (0.65*rd) - (0.36*b)) / 49.17

    elif target_sci == "Uniformity (UI)":
        sci = st.number_input("Target SCI Value", value=0.0, key="sci_ui")
        s = st.number_input("Strength (S) [g/tex]", value=0.0, key="s_ui")
        l = st.number_input("Length (UHML) [mm]", value=0.0, key="l_ui")
        mic = st.number_input("Micronaire (Mic) [µg/inch]", value=0.0, key="mic_ui")
        rd = st.number_input("Reflectance (Rd)", value=0.0, key="rd_ui")
        b = st.number_input("Yellowness (+b)", value=0.0, key="b_ui")
        res_sci = (sci - C - (2.9*s) - (49.17*l) + (9.32*mic) - (0.65*rd) - (0.36*b)) / 4.74

    else: # Micronaire (Mic)
        sci = st.number_input("Target SCI Value", value=0.0, key="sci_mic")
        s = st.number_input("Strength (S) [g/tex]", value=0.0, key="s_mic")
        l = st.number_input("Length (UHML) [mm]", value=0.0, key="l_mic")
        ui = st.number_input("Uniformity (UI) [%]", value=0.0, key="ui_mic")
        rd = st.number_input("Reflectance (Rd)", value=0.0, key="rd_mic")
        b = st.number_input("Yellowness (+b)", value=0.0, key="b_mic")
        res_sci = (sci - C - (2.9*s) - (49.17*l) - (4.74*ui) - (0.65*rd) - (0.36*b)) / -9.32

with col_main2:
    # This check now has initialized variables, so it won't crash.
    # It also prevents showing the -414.67 value on load.
    if (s > 0 or l > 0 or sci > 0):
        st.metric(f"Result: {target_sci}", f"{res_sci:.2f}")

# 5. REFERENCE DATA
st.markdown("---")
with st.expander("📖 View SCI Quality Reference Table"):
    data_sci = {
        "SCI Range": ["< 120", "120 - 130", "130 - 145", "145 <"],
        "Quality Category": ["Low Quality", "Average", "Good", "Premium / Excellent"],
        "Spinning Performance": ["Difficult to spin; High waste", "Standard performance", "Smooth spinning; Strong yarn", "Superior yarn quality"]
    }
    df_sci = pd.DataFrame(data_sci)
    df_sci.index = range(1, len(df_sci) + 1)
    st.table(df_sci)

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **S (Strength):** Fiber tenacity measured in grams per tex (g/tex).
* **L (Length):** Upper Half Mean Length (UHML) in millimeters.
* **UI (Uniformity Index):** The ratio of mean length to upper half mean length.
* **Mic (Micronaire):** Fiber fineness and maturity (µg/inch).
* **Rd (Reflectance):** The degree of brightness or grayness of the fiber.
* **+b (Yellowness):** The degree of cotton pigmentation.
* **SCI:** A regression-based index where higher values indicate superior spinnability.
""")