import streamlit as st
import math
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Fiber Fineness Lab", layout="wide", initial_sidebar_state="collapsed")


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

st.title("Fiber Fineness Lab 🔬")
st.markdown("### **What is Fiber Fineness?**")
st.write("Fiber fineness is the linear density of a fiber, representing its weight per unit length. It is a critical quality parameter that determines spinning limits and yarn appearance.")

st.markdown("---")

# 4. METHOD 1: GRAVIMETRIC METHOD
st.subheader("1. Gravimetric Method (Direct Measurement)")

tab_cotton, tab_wool = st.tabs(["Cotton Fibre", "Wool Fibre"])

with tab_cotton:
    st.markdown("""
    **Procedure:**
    1. Extract exactly 100 fibers from each length group provided by a comb sorter.
    2. Measure the exact length of these fibers and weigh them on a high-precision balance.
    3. Calculate fineness using the weight-to-length ratio.
    """)
    st.latex(r"Fineness = \frac{Weight (W)}{Length (L)}")
    
    col_c1, col_c2 = st.columns([3, 1])
    with col_c1:
        target_cot = st.radio("Solve for (Cotton):", ["Fineness (µg/inch)", "Weight (W) [µg]", "Length (L) [inch]"], horizontal=True)
        if target_cot == "Fineness (µg/inch)":
            w_c = st.number_input("Weight (W) [µg]", value=0.0, key="wc1")
            l_c = st.number_input("Length (L) [inch]", value=0.0, key="lc1")
            res_cot = (w_c / l_c) if l_c > 0 else 0.0
        elif target_cot == "Weight (W) [µg]":
            f_c = st.number_input("Fineness [µg/inch]", value=0.0, key="fc2")
            l_c = st.number_input("Length (L) [inch]", value=0.0, key="lc2")
            res_cot = f_c * l_c
        else:
            f_c = st.number_input("Fineness [µg/inch]", value=0.0, key="fc3")
            w_c = st.number_input("Weight (W) [µg]", value=0.0, key="wc3")
            res_cot = (w_c / f_c) if f_c > 0 else 0.0
    with col_c2:
        if res_cot > 0:
            st.metric(f"Result: {target_cot}", f"{res_cot:.2f}")

with tab_wool:
    st.markdown("""
    **Procedure:**
    1. Sort wool fibers into 'classes' based on length.
    2. Record **Class Length (h)** and count the **Number of Fibers (n)** in each class.
    3. Sum these products to find the total length ($\sum hn$) and weigh the sample ($W$).
    """)
    
    # Step A
    st.markdown("#### Step A: Calculate Total Length ($\sum hn$)")
    num_classes = st.number_input("How many length classes?", min_value=1, value=1)
    df_wool = pd.DataFrame({"Class Length (h) [cm]": [0.0]*num_classes, "Fiber Count (n)": [0]*num_classes})
    df_wool.index = range(1, num_classes + 1)
    edited_wool = st.data_editor(df_wool, use_container_width=True)
    sum_hn = (edited_wool.iloc[:,0] * edited_wool.iloc[:,1]).sum()
    st.metric(label="Total Length (Σhn)", value=f"{sum_hn:.3f} cm")

    # Step B: Gravimetric Diameter Calculation
    st.markdown("---")
    st.markdown("#### Step B: Gravimetric Diameter Calculation")
    st.latex(r"d_{grav} (\mu m) = \sqrt{97190 \cdot \frac{W}{\sum hn}}")

    col_w1, col_w2 = st.columns([3, 1])
    with col_w1:
        target_w = st.radio("Solve for:", ["Diameter (µm)", "Weight (W) [mg]", "Total Length (Σhn)"], horizontal=True)
        
        # Logic: Use Step A result as default if it exists, otherwise 0.0
        default_l = sum_hn if sum_hn > 0 else 0.0

        if target_w == "Diameter (µm)":
            w_w = st.number_input("Total Weight (W) [mg]", value=0.0, key="ww_b1")
            l_input = st.number_input("Total Length (Σhn) [cm]", value=default_l, key="l_b1")
            res_w = math.sqrt((97190 * w_w) / l_input) if l_input > 0 else 0.0
            label_w = "Diameter (µm)"
            
        elif target_w == "Weight (W) [mg]":
            d_w = st.number_input("Diameter (d) [µm]", value=0.0, key="dw_b2")
            l_input = st.number_input("Total Length (Σhn) [cm]", value=default_l, key="l_b2")
            # W = (d^2 * Σhn) / 97190
            res_w = (d_w**2 * l_input) / 97190
            label_w = "Weight (W) [mg]"
            
        else: # Total Length (Σhn)
            d_w = st.number_input("Diameter (d) [µm]", value=0.0, key="dw_b3")
            w_w = st.number_input("Total Weight (W) [mg]", value=0.0, key="ww_b3")
            # Σhn = (97190 * W) / d^2
            res_w = (97190 * w_w) / (d_w**2) if d_w > 0 else 0.0
            label_w = "Total Length (Σhn)"
                
    with col_w2:
        if res_w > 0:
            st.metric(f"Calculated {label_w}", f"{res_w:.3f}")

    # 4. JUSTIFICATION & NOTES
    st.markdown("---")
    st.info("""
        **Justification for the Wool Constant (97190)**
            
        This constant accounts for the specific gravity of wool (1.31) and geometric factors to calculate a circular diameter equivalent in microns.
        
        **Parameters:**
        * **W:** Total weight of fibers (mg).
        * **Σhn:** Cumulative length of all fibers (cm).
        * **d:** Average fiber diameter (µm).
        """)

st.markdown("---")

# 2. OPTICAL METHOD (Microscopic Analysis)
st.subheader("2. Optical Method (Microscopic Analysis)")

# --- PROCEDURE SECTION ---
st.markdown("""
**Procedure:**
1. Prepare a specimen slide with fibers arranged for a longitudinal or cross-sectional view.
2. Use a **Projection Microscope** to project the fiber image onto a screen or digital interface.
3. Measure the diameter ($d$) of a large number of individual fibers.
4. The observed diameters must be averaged to find the **Mean Diameter** used in the formulas below.
""")

# --- TABBED CALCULATOR SECTION ---
tab_decitex, tab_denier = st.tabs(["Decitex Calculation", "Denier Calculation"])

with tab_decitex:
    st.latex(r"Decitex = 7.85 \cdot 10^{-3} \cdot \rho \cdot d^2")
    col_deci1, col_deci2 = st.columns([3, 1])
    
    with col_deci1:
        target_deci = st.radio("Solve for (Decitex):", ["Fineness", "Diameter (d)", "Density (ρ)"], horizontal=True, key="solve_deci")
        k_deci = 7.85e-3
        
        if target_deci == "Fineness":
            d_deci = st.number_input("Mean Diameter (d) [µm]", value=0.0, key="d_deci1")
            rho_deci = st.number_input("Density (ρ) [g/cm³]", value=1.52, key="rho_deci1")
            res_deci = k_deci * rho_deci * (d_deci**2)
        elif target_deci == "Diameter (d)":
            f_deci = st.number_input("Fineness [Decitex]", value=0.0, key="f_deci2")
            rho_deci = st.number_input("Density (ρ) [g/cm³]", value=1.52, key="rho_deci2")
            res_deci = math.sqrt(f_deci / (k_deci * rho_deci)) if (k_deci * rho_deci) > 0 else 0.0
        else: # Density
            f_deci = st.number_input("Fineness [Decitex]", value=0.0, key="f_deci3")
            d_deci = st.number_input("Mean Diameter (d) [µm]", value=0.0, key="d_deci3")
            res_deci = f_deci / (k_deci * d_deci**2) if (k_deci * d_deci**2) > 0 else 0.0

    with col_deci2:
        if res_deci > 0:
            st.metric(f"Result: {target_deci}", f"{res_deci:.3f}")

with tab_denier:
    st.latex(r"Denier = 7.07 \cdot 10^{-3} \cdot \rho \cdot d^2")
    col_den1, col_den2 = st.columns([3, 1])
    
    with col_den1:
        target_den = st.radio("Solve for (Denier):", ["Fineness", "Diameter (d)", "Density (ρ)"], horizontal=True, key="solve_den")
        k_den = 7.07e-3
        
        if target_den == "Fineness":
            d_den = st.number_input("Mean Diameter (d) [µm]", value=0.0, key="d_den1")
            rho_den = st.number_input("Density (ρ) [g/cm³]", value=1.52, key="rho_den1")
            res_den = k_den * rho_den * (d_den**2)
        elif target_den == "Diameter (d)":
            f_den = st.number_input("Fineness [Denier]", value=0.0, key="f_den2")
            rho_den = st.number_input("Density (ρ) [g/cm³]", value=1.52, key="rho_den2")
            res_den = math.sqrt(f_den / (k_den * rho_den)) if (k_den * rho_den) > 0 else 0.0
        else: # Density
            f_den = st.number_input("Fineness [Denier]", value=0.0, key="f_den3")
            d_den = st.number_input("Mean Diameter (d) [µm]", value=0.0, key="d_den3")
            res_den = f_den / (k_den * d_den**2) if (k_den * d_den**2) > 0 else 0.0

    with col_den2:
        if res_den > 0:
            st.metric(f"Result: {target_den}", f"{res_den:.3f}")


st.markdown("---")

import streamlit as st
import math

st.subheader("3. Vibroscope Method Analysis")

st.markdown("""
    **Procedure:**
    1. Hang a single fiber filament between two fixed points of a known length ($l$).
    2. Apply tension ($T$) to the fiber by attaching a **Weighing Clip ($W_g$)**.
    3. Start the Frequency Generator and slowly adjust the frequency ($f$) until the fiber reaches its **Natural Fundamental Frequency** (maximum vibration width).
    4. Record the resonance frequency ($f$), length ($l$), and the clip mass ($W_g$).
""")

# --- CALCULATOR 1: FUNDAMENTAL PHYSICS ---
st.markdown("#### A. Frequency Calculator")
st.latex(r"f = \frac{1}{2l} \cdot \sqrt{\frac{T}{M}}")

# Physics Formula Solver: Variables in Col 1, Result in Col 2
col_p1, col_p2 = st.columns([3, 1])

with col_p1:
    target_p = st.radio("Solve for:", ["Frequency (f)", "Length (l)", "Tension (T)", "Mass  per unit length of a perfectly flexible string (M)"], horizontal=True, key="phys_solve_final")
    
    # Standardizing inputs into a single column logic
    if target_p == "Frequency (f)":
        l_p = st.number_input("Length (l) [cm]", value=0.0, key="v_l_f")
        t_p = st.number_input("Tension (T) [dynes]", value=0.0, key="v_t_f")
        m_p = st.number_input("Mass  per unit length (M) [g/cm]", value=0.0, key="v_m_f")
        res_p = (1 / (2 * l_p)) * math.sqrt(t_p / m_p) if (l_p > 0 and m_p > 0) else 0.0
        
    elif target_p == "Length (l)":
        f_p = st.number_input("Frequency (f) [Hz]", value=0.0, key="v_f_l")
        t_p = st.number_input("Tension (T) [dynes]", value=0.0, key="v_t_l")
        m_p = st.number_input("Mass per unit length (M) [g/cm]", value=0.0, key="v_m_l")
        res_p = (1 / (2 * f_p)) * math.sqrt(t_p / m_p) if (f_p > 0 and m_p > 0) else 0.0
        
    elif target_p == "Tension (T)":
        f_p = st.number_input("Frequency (f) [Hz]", value=0.0, key="v_f_t")
        l_p = st.number_input("Length (l) [cm]", value=0.0, key="v_l_t")
        m_p = st.number_input("Mass per unit length (M) [g/cm]", value=0.0, key="v_m_t")
        res_p = (2 * l_p * f_p)**2 * m_p
        
    else: # Mass (M)
        f_p = st.number_input("Frequency (f) [Hz]", value=0.0, key="v_f_m")
        l_p = st.number_input("Length (l) [cm]", value=0.0, key="v_l_m")
        t_p = st.number_input("Tension (T) [dynes]", value=0.0, key="v_t_m")
        res_p = t_p / (2 * l_p * f_p)**2 if (l_p * f_p) > 0 else 0.0

with col_p2:
    if res_p > 0:
        st.metric(f"Result: {target_p}", f"{res_p:.4f}")

# --- CALCULATOR 2: INDUSTRIAL DENIER ---
st.subheader("B. Fineness Calculator (Denier)")
st.markdown('''Use the above calculated Frequency (f) in the below formula.            
''')
st.latex(r"M = \left( \frac{W_g}{l^2 \cdot f^2} \right) \cdot (9 \cdot 10^5)")

col_v1, col_v2 = st.columns([3, 1])

with col_v1:
    target_v = st.radio("Solve for:", ["Fineness (M)", "Clip Mass (Wg)", "Frequency (f)", "Length (l)"], horizontal=True, key="den_solve_final")
    
    if target_v == "Fineness (M)":
        wgv = st.number_input("Clip Mass (Wg) [mg]", value=0.0, key="v_wg_m")
        lv = st.number_input("Length (l) [cm]", value=0.0, key="v_l_m")
        fv = st.number_input("Freq (f) [Hz]", value=0.0, key="v_f_m")
        res_v = (wgv / (lv**2 * fv**2)) * 9e5 if (lv * fv) > 0 else 0.0
        
    elif target_v == "Clip Mass (Wg)":
        mv = st.number_input("Fineness (M) [Denier]", value=0.0, key="v_m_wg")
        lv = st.number_input("Length (l) [cm]", value=0.0, key="v_l_wg")
        fv = st.number_input("Freq (f) [Hz]", value=0.0, key="v_f_wg")
        res_v = (mv * lv**2 * fv**2) / 9e5
        
    elif target_v == "Frequency (f)":
        mv = st.number_input("Fineness (M) [Denier]", value=0.0, key="v_m_f")
        wgv = st.number_input("Clip Mass (Wg) [mg]", value=0.0, key="v_wg_f")
        lv = st.number_input("Length (l) [cm]", value=0.0, key="v_l_f")
        res_v = math.sqrt((wgv * 9e5) / (mv * lv**2)) if (mv * lv) > 0 else 0.0
        
    else: # Length (l)
        mv = st.number_input("Fineness (M) [Denier]", value=0.0, key="v_m_l")
        wgv = st.number_input("Clip Mass (Wg) [mg]", value=0.0, key="v_wg_l")
        fv = st.number_input("Freq (f) [Hz]", value=0.0, key="v_f_l")
        res_v = math.sqrt((wgv * 9e5) / (mv * fv**2)) if (mv * fv) > 0 else 0.0

with col_v2:
    if res_v > 0:
        st.metric(f"Result: {target_v}", f"{res_v:.3f}")

st.write("")
st.info('''
**Justification for above expression** 

Mass per unit length and fineness both represent the same physical property ($M$). The constant **$9 \cdot 10^5$** is used to express this ratio in **Denier**, which is the industrial standard for fiber fineness.
''')

st.markdown("---")  

# 7. METHOD 4: AIRFLOW
st.subheader("4. Airflow Method (Indirect Measurement)")
st.markdown("""
**Procedure:**
1. Weigh exactly **3.24 g** of fiber sample.
2. Pack the fiber into the cylindrical chamber.
3. Allow compressed air to flow through. Finer fibers have higher specific surface area ($S$), creating more resistance and a higher pressure drop.
4. Enter the number of readings and the readings taken from the instrument to calculate the Average, SD and CV %.
""")

col_a1, col_a2 = st.columns([3, 1])
with col_a1:
    st.write("**Instrument Readings (Micronaire - µg/inch)**")
    r_count = st.number_input("Number of samples", min_value=1, value=1)
    df_air = pd.DataFrame({"Value": [0.0]*r_count})
    df_air.index = range(1, r_count + 1) 
    ed_air = st.data_editor(df_air, use_container_width=True)
    vals = ed_air["Value"]

with col_a2:
    if vals.sum() > 0:
        avg = vals.mean()
        std = vals.std()
        cv = (std/avg)*100 if avg > 0 else 0
        st.metric("Mean Micronaire", f"{avg:.2f} µg/inch")
        st.write(f"**SD:** {std:.3f} | **CV%:** {cv:.2f}%")