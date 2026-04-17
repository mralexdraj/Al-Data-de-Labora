import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Chemical Add-on Analysis", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Chemical Add-on (%) Analysis 🧪")

# 3. DEFINITIONS
st.markdown("### **What is Chemical Add-on?**")
st.markdown("""
<div style="text-align: justify;">
Chemical Add-on (A%) represents the actual mass of solid finishing agents (such as resins, softeners, or flame retardants) that remains permanently on the fabric after the drying and curing process. While Wet Pick-up measures the total liquid retained (water + chemicals), the Add-on focuses specifically on the active solids. Precise control of the add-on is vital to achieving the desired functional properties of the fabric without compromising its strength, handle, or appearance.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Chemical Add-on")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Determine the precise solid concentration (Conc. %) of the chemical bath being used in the padding mangle.</li>
<li>Determine the Wet Pick-up (P%) of the fabric for the specific mangle settings and fabric type.</li>
<li>Pass the fabric through the padding mangle to apply the chemical liquor.</li>
<li>Dry the fabric in a stenter or oven to evaporate the water, leaving only the chemical solids fixed to the fiber.</li>
<li>Calculate the final add-on percentage based on the relationship between bath concentration and liquid retention.</li>
</ol>
</div>
""", unsafe_allow_html=True)



# 5. CALCULATOR SECTION
st.subheader("2. Chemical Add-on Analytical Calculator")

st.latex(r"A\% = \frac{C\% \times P\%}{100}")

# MCP: Radio buttons placed outside and above columns
target_mode = st.radio(
    "Solve for:",
    ["Chemical Add-on (A) [%]", "Bath Concentration (C) [%]", "Wet Pick-up (P) [%]"],
    horizontal=True,
    key="solver_addon"
)

# MCP: 3:1 Column Ratio
col_main1, col_main2 = st.columns([3, 1])

res_val = 0.0
a_in, c_in, p_in = 0.0, 0.0, 0.0

with col_main1:
    if "Add-on" in target_mode:
        c_in = st.number_input("Chemical Concentration in Bath (C) [%]", value=0.0, key="c_1")
        p_in = st.number_input("Wet Pick-up (P) [%]", value=0.0, key="p_1")
        res_val = (c_in * p_in) / 100
        
    elif "Concentration" in target_mode:
        a_in = st.number_input("Desired Chemical Add-on (A) [%]", value=0.0, key="a_2")
        p_in = st.number_input("Wet Pick-up (P) [%]", value=0.0, key="p_2")
        if p_in > 0:
            res_val = (a_in * 100) / p_in
            
    else: # Wet Pick-up
        a_in = st.number_input("Desired Chemical Add-on (A) [%]", value=0.0, key="a_3")
        c_in = st.number_input("Chemical Concentration in Bath (C) [%]", value=0.0, key="c_3")
        if c_in > 0:
            res_val = (a_in * 100) / c_in

with col_main2:
    st.write("")
    st.write("")
    if res_val > 0:
        st.metric(f"Result: {target_mode.split(' (')[0]}", f"{res_val:.2f}%")

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Justification:**
* **A (Chemical Add-on):** The weight of dry chemical solids added per unit weight of the dry fabric.
* **C (Concentration):** The percentage of active solid ingredients present in the aqueous padding liquor.
* **P (Wet Pick-up):** The amount of liquor retained by the fabric before drying, which acts as the carrier for the solids.
* **Solids Content:** Finishing chemicals are often supplied as dispersions; the "active solids" value must be used for accurate calculation.
* **Process Balance:** If the add-on is too low, functional finishes (like water repellency) will fail. If too high, it may cause shade yellowing or "dusting" of the chemical.
""")