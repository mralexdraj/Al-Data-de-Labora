import streamlit as st
import math
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Fabric Stiffness & Modulus", layout="wide", initial_sidebar_state="collapsed")

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
        st.switch_page("pages/Fabric's lab selection.py")

st.title("Fabric Stiffness Analysis 📐")

# 3. DEFINITIONS
st.subheader("What is Fabric Stiffness?")
st.markdown("""
<div style="text-align: justify;">
<b>Bending Length (C):</b> This is the length of fabric that will bend under its own weight to a specific extent. It provides a measure of the "drapability" and stiffness of the fabric.
<br><br>
<b>Flexural Rigidity (G):</b> A measure of the stiffness of the fabric when bent. It accounts for both the weight of the fabric and its bending length, indicating the resistance of the fabric to bending forces.
<br><br>
<b>Bending Modulus (q):</b> This is the "intrinsic stiffness" of the fabric material. By involving the fabric thickness, it allows for the comparison of stiffness between fabrics of different thicknesses.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. CALCULATORS (Chained Logic)

# --- SECTION 1: FLEXURAL RIGIDITY (Warp & Weft) ---
st.subheader("1. Flexural Rigidity ($G$)")
st.latex(r"G = W \times C^3 \times 10^3")

target_g = st.radio("Solve for (Rigidity Section):", ["Flexural Rigidity (G)", "Bending Length (C)", "Cloth Weight (GSM)"], horizontal=True, key="solve_g_linear")

col_g1, col_g2 = st.columns([3, 1])
# Initializing variables for chained logic
w_gsm, c_len, g_val = 0.0, 0.0, 0.0

with col_g1:
    if target_g == "Flexural Rigidity (G)":
        w_gsm = st.number_input("Cloth Weight (GSM)", value=0.0, key="w1_l")
        c_len = st.number_input("Bending Length (C)[cm]", value=0.0, key="c1_l")
        w_gcm2 = w_gsm / 10000
        res_g = w_gcm2 * (c_len**3) * 1000 if c_len > 0 else 0.0
    elif target_g == "Bending Length (C)":
        g_val = st.number_input("Flexural Rigidity (G)[mg/cm]", value=0.0, key="g2_l")
        w_gsm = st.number_input("Cloth Weight (GSM)", value=0.0, key="w2_l")
        w_gcm2 = w_gsm / 10000
        res_g = (g_val / (w_gcm2 * 1000))**(1/3) if w_gsm > 0 else 0.0
    else: # Weight
        g_val = st.number_input("Flexural Rigidity (G)[mg/cm]", value=0.0, key="g3_l")
        c_len = st.number_input("Bending Length (C)[cm]", value=0.0, key="c3_l")
        res_g = (g_val / (c_len**3 * 1000)) * 10000 if c_len > 0 else 0.0

with col_g2:
    if (w_gsm > 0 or c_len > 0 or g_val > 0):
        u = " mg/cm" if "Rigidity" in target_g else (" cm" if "Length" in target_g else " GSM")
        st.metric(f"Result: {target_g}", f"{res_g:.3f}{u}")

st.info("**Formula Note:** This calculation applies to both Warp ($G_w$) and Weft ($G_f$) directions. $W$ is weight in $g/cm^2$ (GSM/10,000).")

st.markdown("---")

# --- SECTION 2: OVERALL RIGIDITY ---
st.subheader("2. Overall Flexural Rigidity ($G_0$)")
st.latex(r"G_0 = \sqrt{G_{warp} \times G_{weft}}")

target_g0 = st.radio("Solve for (Overall Section):", ["Overall Rigidity (G₀)", "Warp Rigidity (Gw)", "Weft Rigidity (Gf)"], horizontal=True, key="solve_g0")

col_g01, col_g02 = st.columns([3, 1])
gw_in, gf_in, g0_in = 0.0, 0.0, 0.0

with col_g01:
    if target_g0 == "Overall Rigidity (G₀)":
        gw_in = st.number_input("Warp Rigidity (Gw) [mg/cm]", value=res_g, key="gw1")
        gf_in = st.number_input("Weft Rigidity (Gf) [mg/cm]", value=0.0, key="gf1")
        res_g0 = math.sqrt(gw_in * gf_in)
    elif target_g0 == "Warp Rigidity (Gw)":
        g0_in = st.number_input("Overall Rigidity (G₀) [mg/cm]", value=0.0, key="g02")
        gf_in = st.number_input("Weft Rigidity (Gf) [mg/cm]", value=0.0, key="gf2")
        res_g0 = (g0_in**2) / gf_in if gf_in > 0 else 0.0
    else: # Weft
        g0_in = st.number_input("Overall Rigidity (G₀) [mg/cm]", value=0.0, key="g03")
        gw_in = st.number_input("Warp Rigidity (Gw) [mg/cm]", value=res_g, key="gw3")
        res_g0 = (g0_in**2) / gw_in if gw_in > 0 else 0.0

with col_g02:
    if (gw_in > 0 or gf_in > 0 or g0_in > 0):
        st.metric(f"Result: {target_g0}", f"{res_g0:.3f} mg·cm")

st.markdown("---")

# --- SECTION 3: BENDING MODULUS ---
st.subheader("3. Bending Modulus ($q$)")
st.latex(r"q = \frac{12 \times G \times 10^{-6}}{g^3}")

target_q = st.radio("Solve for (Modulus Section):", ["Bending Modulus (q)", "Overall Flexural Rigidity (G)", "Fabric Thickness (mm)"], horizontal=True, key="solve_q_linear")

col_q1, col_q2 = st.columns([3, 1])
g_in_q, th_mm, q_in = 0.0, 0.0, 0.0

with col_q1:
    if target_q == "Bending Modulus (q)":
        g_in_q = st.number_input("Overall Flexural Rigidity (G) [mg/cm]", value=res_g0, key="gq1")
        th_mm = st.number_input("Fabric Thickness (g) [mm]", value=0.0, format="%.2f", key="th1_l")
        # Conversion to cm for formula: mm / 10
        th_cm = th_mm / 10
        res_q = (12 * g_in_q * 1e-6) / (th_cm**3) if th_cm > 0 else 0.0
    elif target_q == "Rigidity (G)":
        q_in = st.number_input("Bending Modulus (q) [kg/cm²]", value=0.0, key="qi2_l")
        th_mm = st.number_input("Fabric Thickness (g) [mm]", value=0.0, format="%.2f", key="th2_l")
        th_cm = th_mm / 10
        res_q = (q_in * (th_cm**3)) / (12 * 1e-6) if th_cm > 0 else 0.0
    else: # Thickness (mm)
        q_in = st.number_input("Bending Modulus (q) [kg/cm²]", value=0.0, key="qi3_l")
        g_in_q = st.number_input("Flexural Rigidity (G) [mg·cm]", value=res_g0, key="gq3")
        # Internal cm calculation converted back to mm for result
        res_q = (((12 * g_in_q * 1e-6) / q_in)**(1/3)) * 10 if q_in > 0 else 0.0

with col_q2:
    if (g_in_q > 0 or (target_q == "Thickness (mm)" and q_in > 0) or th_mm > 0):
        u = " kg/cm²" if "Modulus" in target_q else (" mg·cm" if "Rigidity" in target_q else " mm")
        st.metric(f"Result: {target_q}", f"{res_q:.4f}{u}")

# 5. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **W (Weight):** Cloth weight expressed in $g/cm^2$ (GSM / 10,000).
* **C (Bending Length):** Measured distance from the Shirley Stiffness Tester ($cm$).
* **G (Flexural Rigidity):** Resistance of the fabric to bending forces ($mg \cdot cm$).
* **G₀ (Overall Rigidity):** The geometric mean of stiffness in both directions.
* **g (Thickness):** Fabric thickness measured in millimeters ($mm$) and converted to $cm$ for calculation.
* **q (Bending Modulus):** The intrinsic stiffness of the fabric material ($kg/cm^2$).
* **10³ / 10⁻⁶ / 12:** Mathematical constants for unit normalization and geometric moment calculation.
""")