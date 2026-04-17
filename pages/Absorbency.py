import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE SETUP
st.set_page_config(page_title="Beer-Lambert Lab", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Beer-Lambert Law Analysis 🧪")

# 3. DEFINITIONS
st.markdown("### **What is the Beer-Lambert Law?**")
st.markdown("""
<div style="text-align: justify;">
The Beer-Lambert Law is the fundamental principle governing quantitative spectrometry in textile processing. It states that the Absorbance (A) of a solution is directly proportional to its Concentration (c) and the Path Length (l) of the light traveling through it. In the dye house, this law allows for the precise measurement of dye concentrations in liquors, the determination of dye exhaustion rates, and the assessment of effluent quality. It provides the mathematical link between the physical "darkness" of a liquid and the actual mass of chemical solids dissolved within it.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Optical Density")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Switch on the spectrophotometer and allow the lamp to stabilize for at least 15 minutes.</li>
<li>Fill a clean glass or quartz cuvette with the "blank" solution (distilled water or solvent used) and set the instrument to zero absorbance.</li>
<li>Fill a second cuvette with the dye solution. If the solution is too dark, perform a precise dilution (e.g., 1:10) to bring the absorbance into the linear range.</li>
<li>Insert the sample cuvette and record the absorbance (A) at the wavelength of maximum absorption (λmax).</li>
<li>Calculate the concentration or molar absorptivity using the verified path length and dilution factor.</li>
</ol>
</div>
""", unsafe_allow_html=True)



# 5. CALCULATORS

# --- SECTION I: SPECTROMETRY LAB ---
st.subheader("2. Interactive Spectrometry Calculator")
st.latex(r"A = \varepsilon \cdot c \cdot l")

target_beer = st.radio(
    "Solve for (Spectrometry Section):",
    ["Concentration (c) [g/L]", "Absorbance (A) [Abs]", "Molar Absorptivity (ε) [L/(g·cm)]"],
    horizontal=True,
    key="solver_beer_zero"
)

col1_in, col1_res = st.columns([3, 1])
res_val = 0.0

with col1_in:
    if "Concentration" in target_beer:
        abs_in = st.number_input("Measured Absorbance (A) [Abs]", value=0.0, format="%.3f", key="a_z1")
        eps_in = st.number_input("Molar Absorptivity (ε) [L/(g·cm)]", value=0.0, key="e_z1")
        path_l = st.number_input("Cuvette Path Length (l) [cm]", value=0.0, key="l_z1")
        dil_z = st.number_input("Dilution Factor", value=1.0, key="df_z1") # DF 1.0 is the logical base
        if eps_in > 0 and path_l > 0:
            res_val = (abs_in / (eps_in * path_l)) * dil_z
            
    elif "Absorbance" in target_beer:
        conc_in = st.number_input("Dye Concentration (c) [g/L]", value=0.0, key="c_z2")
        eps_in = st.number_input("Molar Absorptivity (ε) [L/(g·cm)]", value=0.0, key="e_z2")
        path_l = st.number_input("Cuvette Path Length (l) [cm]", value=0.0, key="l_z2")
        res_val = eps_in * conc_in * path_l
        
    else: # Molar Absorptivity
        abs_in = st.number_input("Measured Absorbance (A) [Abs]", value=0.0, format="%.3f", key="a_z3")
        conc_in = st.number_input("Known Concentration (c) [g/L]", value=0.0, key="c_z3")
        path_l = st.number_input("Cuvette Path Length (l) [cm]", value=0.0, key="l_z3")
        if conc_in > 0 and path_l > 0:
            res_val = abs_in / (conc_in * path_l)

with col1_res:
    st.write("")
    st.write("")
    if res_val > 0:
        u = " g/L" if "Concentration" in target_beer else (" Abs" if "Absorbance" in target_beer else " L/(g·cm)")
        st.metric(f"Result: {target_beer.split(' (')[0]}", f"{res_val:.4f}{u}")

st.markdown("---")

# --- SECTION II: TRANSMITTANCE CONVERTER ---
st.subheader("3. Transmittance (T%) to Absorbance (A) Converter")
st.latex(r"A = 2 - \log_{10}(T\%)")

target_t = st.radio(
    "Solve for (Transmittance Section):",
    ["Absorbance (A) [From T%]", "Transmittance (T%) [From A]"],
    horizontal=True,
    key="solver_trans_zero"
)

col2_in, col2_res = st.columns([3, 1])
res_t = 0.0

with col2_in:
    if "Absorbance" in target_t:
        t_val = st.slider("Transmittance Percentage (T%) [%]", 0.0, 100.0, 10.0,key="t_z_slide")
        # Logic: Only calculate if slider moved from 100% (or user intent)
        res_t = 2 - np.log10(t_val)
    else:
        a_val = st.number_input("Known Absorbance (A) [AU]", value=0.0, format="%.4f", key="a_z_t")
        if a_val > 0:
            res_t = 10**(2 - a_val)

with col2_res:
    st.write("")
    st.write("")
    # Standard Guard: only show if the result is meaningful/calculated
    if (res_t > 0 and "Transmittance" in target_t) or ("Absorbance" in target_t and t_val < 100.0):
        u_t = " AU" if "Absorbance" in target_t else " %" 
        st.metric(f"Result: {target_t.split(' (')[0]}", f"{res_t:.4f}{u_t}")

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Justification:**
* **A (Absorbance):** A dimensionless unit representing the logarithmic ratio of incident to transmitted light.
* **ε (Epsilon):** The Molar Absorptivity; a constant that defines how strongly a specific dye absorbs light at a specific wavelength.
* **c (Concentration):** The amount of dye molecules in the solution. Linear proportionality is usually lost if $A > 1.5$.
* **l (Path Length):** The distance light travels through the solution. Standard lab cuvettes are exactly 1 cm.
* **Transmittance (T%):** The percentage of light that successfully passes through the sample ($T = 100 \\times 10^{-A}$).
* **Linearity:** The law is only valid for dilute solutions. At high concentrations, molecular interactions cause the relationship to become non-linear.
""")