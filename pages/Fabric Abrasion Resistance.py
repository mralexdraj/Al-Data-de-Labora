import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE SETUP
st.set_page_config(page_title="Fabric Lab - Abrasion Resistance", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Abrasion Resistance Analysis 🔄")

# 3. DEFINITIONS
st.markdown("### **What is Abrasion Resistance?**")
st.markdown("""
<div style="text-align: justify;">
Abrasion resistance is the ability of a fabric to withstand surface wear caused by flat rubbing contact with another material. It is a critical durability factor that determines the service life of a textile product. Abrasion leads to the physical destruction of fibers through mechanisms like fibrillation, snagging, and heat degradation, eventually resulting in the loss of aesthetic appeal, thickness, and tensile strength.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Abrasion Resistance (Martindale Method)")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Condition the fabric specimen in a standard atmosphere (20°C ± 2°C, 65% ± 2% RH) before testing.</li>
<li>Cut circular specimens and mount them securely in the Martindale specimen holders with standard felt backing.</li>
<li>Place a standard woolen abradant fabric on the rubbing tables and secure it under tension.</li>
<li>Apply the specific laboratory load (typically 9 kPa for apparel or 12 kPa for upholstery) to the spindles.</li>
<li>Set the machine to run at a rotational speed of 47.5 ± 2.5 rpm. The specimens move in a complex geometric path known as a Lissajous figure (16 rubs per cycle).</li>
<li>Assess the fabric at predetermined intervals for thread breakage, significant weight loss, or change in appearance.</li>
</ol>
</div>
""", unsafe_allow_html=True)



# 5. PRE-TEST LOAD CALCULATOR
st.subheader("2. Pre-Test: Pressure & Load Calculator")

target_calc = st.radio(
    "Solve for (Load Section):", 
    ["Pressure (P) [kPa]", "Required Slot Weight (m) [g]"], 
    horizontal=True, key="p_calc"
)

col_p1, col_p2 = st.columns([3, 1])
res_p = 0.0
with col_p1:
    # Industry conversion factor for standard Martindale holder area
    k_factor = 0.0152 
    base_holder = st.number_input("Base Spindle/Holder Weight [g]", value=0.0, key="bh_w")
    
    if "Pressure" in target_calc:
        slot_w = st.number_input("Added Slot Weight [g]", value=0.0, key="sw_in")
        total_m = base_holder + slot_w
        if total_m > 0: res_p = total_m * k_factor
    else:
        target_kpa = st.number_input("Target Pressure [kPa]", value=0.0, key="tkpa")
        if target_kpa > 0: res_p = (target_kpa / k_factor) - base_holder

with col_p2:
    if res_p > 0:
        u = " kPa" if "Pressure" in target_calc else " g"
        st.metric(f"Result: {target_calc.split(' [')[0]}", f"{res_p:.2f}{u}")

st.info("""
**Standard Lab Targets:**
* **9 kPa:** Standard Apparel and Clothing.
* **12 kPa:** Upholstery, Protective Workwear, and Heavy Contract fabrics.
* **Note:** For rapid screening, a total mass of approximately 400g is commonly utilized.
""")

st.markdown("---")

# 6. PERFORMANCE CALCULATORS
st.subheader("3. Abrasion Performance Calculators")

tab1, tab2, tab3, tab4 = st.tabs([
    "Weight Loss (%)", "Thickness Loss (%)", "Strength Loss (%)", "ARI Index"
])

with tab1:
    st.latex(r"W_L\% = \left( \frac{W_1 - W_2}{W_1} \right) \times 100")
    t_wl = st.radio("Solve for (Weight):", ["Weight Loss (WL%) [%]", "Final Weight (W2) [g]", "Initial Weight (W1) [g]"], horizontal=True, key="twl")
    c1, c2 = st.columns([3, 1]); res_wl = 0.0
    with c1:
        if "Loss" in t_wl:
            w1 = st.number_input("Initial Weight (W1) [g]", value=0.0, format="%.4f", key="w1_1")
            w2 = st.number_input("Final Weight (W2) [g]", value=0.0, format="%.4f", key="w2_1")
            if w1 > 0: res_wl = ((w1 - w2) / w1) * 100
        elif "Final" in t_wl:
            w1 = st.number_input("Initial Weight (W1) [g]", value=0.0, format="%.4f", key="w1_2")
            l_in = st.number_input("Target Loss [%]", value=0.0, key="lw_2")
            res_wl = w1 * (1 - (l_in / 100))
        else:
            w2 = st.number_input("Final Weight (W2) [g]", value=0.0, format="%.4f", key="w2_3")
            l_in = st.number_input("Target Loss [%]", value=0.0, key="lw_3")
            if l_in < 100: res_wl = w2 / (1 - (l_in / 100))
    with c2: 
        if res_wl > 0: st.metric(f"Result: {t_wl.split(' [')[0]}", f"{res_wl:.4f}")

with tab2:
    st.latex(r"T_L\% = \left( \frac{T_1 - T_2}{T_1} \right) \times 100")
    t_tl = st.radio("Solve for (Thickness):", ["Thickness Loss (TL%) [%]", "Final Thickness (T2) [mm]"], horizontal=True, key="ttl")
    c1, c2 = st.columns([3, 1]); res_tl = 0.0
    with c1:
        if "Loss" in t_tl:
            t1 = st.number_input("Initial Thickness (T1) [mm]", value=0.0, key="t1_1")
            t2 = st.number_input("Final Thickness (T2) [mm]", value=0.0, key="t2_1")
            if t1 > 0: res_tl = ((t1 - t2) / t1) * 100
        else:
            t1 = st.number_input("Initial Thickness (T1) [mm]", value=0.0, key="t1_2")
            l_in = st.number_input("Target Loss [%]", value=0.0, key="lt_2")
            res_tl = t1 * (1 - (l_in / 100))
    with c2:
        if res_tl > 0: st.metric(f"Result: {t_tl.split(' [')[0]}", f"{res_tl:.2f}")

with tab3:
    st.latex(r"S_L\% = \left( \frac{S_1 - S_2}{S_1} \right) \times 100")
    t_sl = st.radio("Solve for (Strength):", ["Strength Loss (SL%) [%]", "Retained Strength (S2) [N]"], horizontal=True, key="tsl")
    c1, c2 = st.columns([3, 1]); res_sl = 0.0
    with c1:
        if "Loss" in t_sl:
            s1 = st.number_input("Initial Strength (S1) [N]", value=0.0, key="s1_1")
            s2 = st.number_input("Final Strength (S2) [N]", value=0.0, key="s2_1")
            if s1 > 0: res_sl = ((s1 - s2) / s1) * 100
        else:
            s1 = st.number_input("Initial Strength (S1) [N]", value=0.0, key="s1_2")
            l_in = st.number_input("Acceptable Loss [%]", value=0.0, key="ls_2")
            res_sl = s1 * (1 - (l_in / 100))
    with c2:
        if res_sl > 0: st.metric(f"Result: {t_sl.split(' [')[0]}", f"{res_sl:.1f}")

with tab4:
    st.latex(r"ARI = \frac{N}{W_{loss}(mg)}")
    t_ari = st.radio("Solve for (Index):", ["Abrasion Resistance Index (ARI)", "Total Cycles (N)"], horizontal=True, key="tari")
    c1, c2 = st.columns([3, 1]); res_ari = 0.0
    with c1:
        if "ARI" in t_ari:
            n_in = st.number_input("Total Cycles (N)", value=0.0, key="ni_1")
            w_mg = st.number_input("Weight Loss [mg]", value=0.0, key="wmg_1")
            if w_mg > 0: res_ari = n_in / w_mg
        else:
            ari_in = st.number_input("Target ARI Index", value=0.0, key="ari_2")
            w_mg = st.number_input("Weight Loss [mg]", value=0.0, key="wmg_2")
            res_ari = ari_in * w_mg
    with c2:
        if res_ari > 0: st.metric(f"Result: {t_ari.split(' [')[0]}", f"{res_ari:.2f}")

# 7. REFERENCE TABLE
st.markdown("---")
with st.expander("📖 View Durability Grading Reference"):
    grade_data = {
        "S/No": [1, 2, 3],
        "Cycles to Breakdown": ["< 15,000", "15,000 – 30,000", "30,000 <"],
        "End Use Category": ["Light Domestic (Curtains)", "General Domestic (Furniture)", "Heavy Duty / Contract (Public Transport)"]
    }
    st.table(pd.DataFrame(grade_data).set_index("S/No"))

# 8. JUSTIFICATION FOOTER
st.info("""
**Parameters & Derivation:**
* **Δ (Delta):** Every percentage loss formula follows the logic $(\text{Initial} - \text{Final}) / \text{Initial}$. This represents the relative change in material property caused by the abradant.
* **ARI (Abrasion Resistance Index):** Normalizes fabric durability against weight loss. It defines how many cycles a fabric survives for every 1 mg of material shed.
* **Lissajous Figure:** A complex geometric motion used to ensure the specimen is rubbed in all directions; 1 Lissajous cycle equals 16 rubs.
* **Weight vs. Pressure:** Fabric wear is highly sensitive to load. 9 kPa is the standard pressure for apparel, ensuring the test correlates to human wear patterns.
* **Work of Rupture:** Synthetics typically exhibit higher ARI because their molecular chains require more energy to break compared to the rigid cellulose chains in natural fibers.
""")