import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Fiber Lab - Bundle Strength", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Fibre Bundle Strength Lab ⚖️")
st.markdown("### **What is Bundle Strength?**")
st.markdown("""
<div style="text-align: justify;">
Fibre bundle strength is a measure of the tenacity of a group of fibers tested together, rather than individually. It is a critical parameter in textile manufacturing as it directly influences the strength and performance of the resulting yarn. By using instruments like the Stelometer, we can determine the breaking tenacity of fibers, which helps in categorizing cotton and predicting its spinnability.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 3. METHODOLOGY
st.subheader("1. Bundle Strength Analysis (Stelometer)")
st.markdown("""
**Procedure:**
1. Comb a fiber bundle until the fibers are parallel and free of trash.
2. Load the bundle into the Stelometer clamps ($J_1$ and $J_2$).
3. Select the appropriate gauge length (Zero or 1/8 inch) and set the corresponding spacers.
4. Release the pendulum lever to apply a Constant Rate of Loading (CRL).
5. Record the **Breaking Load (kg)** and the **Bundle Weight (mg)**.
""")

# --- 4. CALCULATOR SECTION ---
st.subheader("2. Strength Analytical Calculator")

# Gauge Tabs (Replaces the Dropdown Selector)
tab_18, tab_zero = st.tabs(["1/8 inch Gauge (K=15.0)", "Zero inch Gauge (K=11.81)"])

# Logic for 1/8 inch Gauge
with tab_18:
    k_18 = 15.0
    st.latex(fr"Tenacity \ (g/tex) = \frac{{Load \ (kg) \times {k_18}}}{{Weight \ (mg)}}")
    
    target_18 = st.radio(
        "Solve for (1/8 Gauge):", 
        ["Tenacity (g/tex)", "Breaking Load (kg)", "Bundle Weight (mg)"], 
        horizontal=True, key="solve_18"
    )
    
    col_18a, col_18b = st.columns([3, 1])
    res_18 = 0.0
    
    with col_18a:
        if target_18 == "Tenacity (g/tex)":
            l = st.number_input("Breaking Load [kg]", value=0.0, key="l_18")
            w = st.number_input("Bundle Weight [mg]", value=0.0, key="w_18")
            res_18 = (l * k_18) / w if w > 0 else 0.0
        elif target_18 == "Breaking Load (kg)":
            t = st.number_input("Known Tenacity [g/tex]", value=0.0, key="t_18")
            w = st.number_input("Bundle Weight [mg]", value=0.0, key="w_18_load")
            res_18 = (t * w) / k_18
        else:
            l = st.number_input("Breaking Load [kg]", value=0.0, key="l_18_weight")
            t = st.number_input("Known Tenacity [g/tex]", value=0.0, key="t_18_weight")
            res_18 = (l * k_18) / t if t > 0 else 0.0
            
    with col_18b:
        if res_18 > 0:
            st.metric(f"Result", f"{res_18:.3f}")

# Logic for Zero inch Gauge
with tab_zero:
    k_zero = 11.81
    st.latex(fr"Tenacity \ (g/tex) = \frac{{Load \ (kg) \times {k_zero}}}{{Weight \ (mg)}}")
    
    target_zero = st.radio(
        "Solve for (Zero Gauge):", 
        ["Tenacity (g/tex)", "Breaking Load (kg)", "Bundle Weight (mg)"], 
        horizontal=True, key="solve_zero"
    )
    
    col_z1, col_z2 = st.columns([3, 1])
    res_zero = 0.0
    
    with col_z1:
        if target_zero == "Tenacity (g/tex)":
            l = st.number_input("Breaking Load [kg]", value=0.0, key="l_z")
            w = st.number_input("Bundle Weight [mg]", value=0.0, key="w_z")
            res_zero = (l * k_zero) / w if w > 0 else 0.0
        elif target_zero == "Breaking Load (kg)":
            t = st.number_input("Known Tenacity [g/tex]", value=0.0, key="t_z")
            w = st.number_input("Bundle Weight [mg]", value=0.0, key="w_z_load")
            res_zero = (t * w) / k_zero
        else:
            l = st.number_input("Breaking Load [kg]", value=0.0, key="l_z_weight")
            t = st.number_input("Known Tenacity [g/tex]", value=0.0, key="t_z_weight")
            res_zero = (l * k_zero) / t if t > 0 else 0.0
            
    with col_z2:
        if res_zero > 0:
            st.metric(f"Result", f"{res_zero:.3f}")

# 5. REFERENCE DATA
st.markdown("---")
with st.expander("📖 View Cotton Strength Standards"):
    st.write("Standard interpretation of cotton tenacity (at 1/8 inch gauge):")
    data_str = {
        "Tenacity (g/tex)": ["Below 15", "15 - 22", "22 - 28", "Above 28"],
        "Category": ["Weak", "Average", "Strong", "Very Strong"]
    }
    df_str = pd.DataFrame(data_str)
    df_str.index = range(1, len(df_str) + 1)
    st.table(df_str)

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **Load (kg):** The force recorded at the moment the fiber bundle breaks.
* **Weight (mg):** The mass of the fiber bundle clamped between the gauge points.
* **K (Constant):** A geometric constant related to the gauge length (15.0 for 1/8" and 11.81 for 0").
* **Tenacity:** The breaking strength per unit linear density, expressed in grams per tex.
* **Gauge Length:** The distance between the clamping jaws during the test.
""")