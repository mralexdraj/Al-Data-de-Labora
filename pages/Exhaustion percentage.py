import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Exhaustion Calculator", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Dye Exhaustion Analysis 🧪")

# 3. DEFINITIONS
st.markdown("### **What is Dye Exhaustion?**")
st.markdown("""
<div style="text-align: justify;">
Dye Exhaustion (E) is a critical parameter in textile processing that quantifies the efficiency of the dyeing process. It represents the proportion of dye that has successfully migrated from the dye bath and fixed onto the textile fiber. Expressed as a percentage, exhaustion is determined by comparing the initial mass of dye in the liquor to the residual dye remaining after the dyeing cycle is complete. High exhaustion rates indicate superior dye uptake, improved color depth, and a more environmentally sustainable process with less chemical waste in the effluent.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Exhaustion Percentage")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Prepare the dye bath with a precisely measured initial concentration of dye (C₀) in grams per liter.</li>
<li>Introduce the textile material into the bath and perform the dyeing process under specified conditions of temperature, time, and pH.</li>
<li>After completion, remove the material and collect a sample of the residual dye liquor (dye-bath effluent).</li>
<li>Analyze the residual liquor using a spectrophotometer to determine the final dye concentration (C₁).</li>
<li>Calculate the percentage of dye exhausted by identifying the relative loss of dye from the bath.</li>
</ol>
</div>
""", unsafe_allow_html=True)



st.latex(r"E\% = \left( \frac{C_0 - C_1}{C_0} \right) \times 100")

# 5. CALCULATOR SECTION
st.subheader("2. Dye Exhaustion Analytical Calculator")

# MCP: Radio buttons placed outside and above columns
target_mode = st.radio(
    "Solve for:",
    ["Exhaustion Percentage (E) [%]", "Initial Concentration (C₀) [g/L]", "Final Concentration (C₁) [g/L]"],
    horizontal=True,
    key="solver_dye_exhaust"
)

# MCP: 3:1 Column Ratio
col_main1, col_main2 = st.columns([3, 1])

res_val = 0.0
c0_in, c1_in, e_in = 0.0, 0.0, 0.0

with col_main1:
    if "Exhaustion" in target_mode:
        c0_in = st.number_input("Initial Dye Concentration (C₀) [g/L]", value=0.0, format="%.3f", key="c0_1")
        c1_in = st.number_input("Final Dye Concentration (C₁) [g/L]", value=0.0, format="%.3f", key="c1_1")
        if c0_in > 0:
            res_val = ((c0_in - c1_in) / c0_in) * 100
            
    elif "Initial" in target_mode:
        e_in = st.number_input("Exhaustion Percentage (E) [%]", value=0.0, key="e_2")
        c1_in = st.number_input("Final Dye Concentration (C₁) [g/L]", value=0.0, format="%.3f", key="c1_2")
        if e_in < 100:
            res_val = c1_in / (1 - (e_in / 100))
            
    else: # Final Concentration
        c0_in = st.number_input("Initial Dye Concentration (C₀) [g/L]", value=0.0, format="%.3f", key="c0_3")
        e_in = st.number_input("Exhaustion Percentage (E) [%]", value=0.0, key="e_3")
        res_val = c0_in * (1 - (e_in / 100))

with col_main2:
    st.write("")
    st.write("")
    if res_val > 0:
        unit = " %" if "Exhaustion" in target_mode else " g/L"
        st.metric(f"Result: {target_mode.split(' (')[0]}", f"{res_val:.3f}{unit}")

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Justification:**
* **E (Exhaustion):** The percentage of dye transferred from the liquor to the fiber. High E values signify process efficiency.
* **C₀ (Initial Concentration):** The mass of dye per unit volume ($g/L$) present in the bath at the start of the dyeing cycle.
* **C₁ (Final Concentration):** The residual dye concentration remaining in the bath after dyeing.
* **Relationship:** The formula follows the fundamental 'Mass Balance' principle ($Mass_{Initial} - Mass_{Final}$), where the difference represents the mass fixed onto the fiber.
* **Spectrophotometry:** In lab practice, $C_1$ is typically derived using the Beer-Lambert Law by measuring the absorbance of the residual liquor.
""")