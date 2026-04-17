import streamlit as st
import pandas as pd
import math

import streamlit as st

# 1. PAGE CONFIG (Enforce Wide Layout)
st.set_page_config(page_title="Fibre Diameter", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Fiber Diameter Lab 📏")
st.markdown("### **Diameter from Linear Density**")
st.write("Directly measuring the diameter of a fiber can be difficult due to its irregular cross-section. However, by using the linear density and volumetric density, we can calculate a theoretical equivalent diameter assuming a cylindrical form.")

st.markdown("---")

# 4. METHOD 1: THEORETICAL CALCULATION
st.subheader("1. Theoretical Diameter Calculation")

st.markdown("""
**Procedure:**
1. Determine the **Linear Density (Tex)** of the fiber sample using the gravimetric method.
2. Identify the **Volumetric Density (ρ)** of the fiber material from standard reference tables.
3. Apply the geometric formula for a cylinder to derive the equivalent diameter.
""")

st.latex(r"d (mm) = \sqrt{\frac{4 \times Tex}{\pi \times \rho}}")

# 5. CALCULATOR SECTION
col_d1, col_d2 = st.columns([3, 1])

with col_d1:
    target_mode = st.radio(
        "Solve for:",
        ["Diameter (d) [mm]", "Linear Density (Tex)", "Volumetric Density (ρ)"],
        horizontal=True,
        key="solver_dia"
    )
    
    res_val = 0.0
    res_microns = 0.0

    if target_mode == "Diameter (d) [mm]":
        tex_in = st.number_input("Linear Density (Tex) [g/1000m]", value=0.0, key="tex_1")
        rho_in = st.number_input("Volumetric Density (ρ) [kg/m³]", value=0.0, key="rho_1")
        if rho_in > 0:
            res_val = math.sqrt((4 * tex_in) / (math.pi * rho_in))
            res_microns = res_val * 1000

    elif target_mode == "Linear Density (Tex)":
        d_in = st.number_input("Diameter (d) [mm]", value=0.0, key="d_2")
        rho_in = st.number_input("Volumetric Density (ρ) [kg/m³]", value=0.0, key="rho_2")
        res_val = (d_in**2 * math.pi * rho_in) / 4

    else: # Volumetric Density
        tex_in = st.number_input("Linear Density (Tex) [g/1000m]", value=0.0, key="tex_3")
        d_in = st.number_input("Diameter (d) [mm]", value=0.0, key="d_3")
        if d_in > 0:
            res_val = (4 * tex_in) / (math.pi * d_in**2)

with col_d2:
    if res_val > 0:
        st.metric(f"Result: {target_mode}", f"{res_val:.5f}")
        if res_microns > 0:
            st.metric("Diameter (d) [µm]", f"{res_microns:.2f} µm")

# 6. REFERENCE DATA
st.markdown("---")
with st.expander("📖 View Reference Densities & Diameters"):
    data = {
        "Fiber Type": ["Polypropylene", "Nylon", "Acrylic", "Silk", "Wool", "Polyester", "Cotton", "Viscose", "Glass"],
        "Density (kg/m³)": ["910", 1140, 1170, 1250, 1310, 1380, 1520, 1520, 2540],
        "Typical Diameter (µm)": ["15 - 40", "15 - 25", "15 - 25", "10 - 15", "15 - 45", "12 - 25", "12 - 20", "12 - 25", "5 - 15"]
    }
    df = pd.DataFrame(data)
    df.index = range(1, len(df) + 1)
    st.table(df)

# 7. JUSTIFICATION FOOTER
st.info("""
**Parameters & Units:**
* **Tex:** Linear Density expressed in grams per 1000 meters ($g/km$).
* **ρ (Rho):** Volumetric Density of the fiber material ($kg/m^3$).
* **d:** Calculated equivalent cylindrical diameter.
        
**Note:** This calculation assumes a perfectly circular cross-section. For highly irregular fibers (like cotton), the result represents the 'equivalent' diameter.
""")