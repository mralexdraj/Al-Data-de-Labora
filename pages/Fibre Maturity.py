import streamlit as st
import pandas as pd
import math

# 1. PAGE SETUP
st.set_page_config(page_title="Fiber Maturity Lab", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Fiber Maturity Lab 🔬")
st.markdown("### **What is Fiber Maturity?**")
st.write("Fiber maturity measures the cell wall thickness relative to the fiber's width. Think of it like a water hose: a mature fiber is round and full, while an immature fiber is flat and ribbon-like.")

st.markdown("---")

# 3. METHOD 1: CAUSTIC SODA SWELLING (Fiber Analysis)
st.subheader("1. Fiber Analysis (Microscope Data)")
st.markdown("""
**Procedure:**
1. Take out a bundle of approximately 100 fibers and arrange them parallel on a glass slide.
2. Add few drops of 18% Caustic Soda (NaOH) solution to swell the fibers.
3. Place a cover slip on top and wait for the swelling action to happen.
4. Observe under a microscope and count the fibers based on their visual appearance.
""")

st.write("Enter the number of fibers counted in your sample:")
col_in1, col_in2, col_in3 = st.columns(3)

# All defaults set to 0
with col_in1: count_m = st.number_input("Mature Fibers (Count)", min_value=0, value=0, step=1, key="m_in")
with col_in2: count_h = st.number_input("Half-Mature Fibers", min_value=0, value=0, step=1, key="h_in")
with col_in3: count_d = st.number_input("Dead Fibers", min_value=0, value=0, step=1, key="d_in")

total_fibers = count_m + count_h + count_d
if total_fibers > 0:
    perc_m, perc_h, perc_d = (count_m/total_fibers)*100, (count_h/total_fibers)*100, (count_d/total_fibers)*100
else:
    perc_m, perc_h, perc_d = 0.0, 0.0, 0.0

st.markdown(f"**Total Fibers Examined: {total_fibers}**")
c1, c2, c3 = st.columns(3)
c1.metric("Normal (Mature) %", f"{perc_m:.1f}%")
c2.metric("Half-Mature %", f"{perc_h:.1f}%")
c3.metric("Dead (Immature) %", f"{perc_d:.1f}%")

st.markdown("---")

# 4. MATURITY RATIO ($M$)
st.subheader("Maturity Ratio (\$M\$)")
st.latex(r"M = \frac{N - D}{200} + 0.70")

col_m1, col_m2 = st.columns([3, 1])
with col_m1:
    target_m = st.radio("Solve for:", ["Ratio (\$M\$)", "Mature % (N)", "Dead % (D)"], horizontal=True, key="solve_m")
    if target_m == "Ratio ($M$)":
        n_in = st.number_input("Mature % (N)", value=perc_m, min_value=0.0, max_value=100.0, key="n_m")
        d_in = st.number_input("Dead % (D)", value=perc_d, min_value=0.0, max_value=100.0, key="d_m")
        res_m = (n_in - d_in) / 200 + 0.70 if (n_in > 0 or d_in > 0) else 0.0
    elif target_m == "Mature % (N)":
        m_in = st.number_input("Ratio (\$M\$)", value=0.0, key="m_n")
        d_in = st.number_input("Dead % (D)", value=0.0, key="d_n")
        res_m = 200 * (m_in - 0.70) + d_in if m_in > 0 else 0.0
    else:
        m_in = st.number_input("Ratio (\$M\$)", value=0.0, key="m_d")
        n_in = st.number_input("Mature % (N)", value=0.0, key="n_d")
        res_m = n_in - 200 * (m_in - 0.70) if m_in > 0 else 0.0

with col_m2:
    if res_m != 0:
        st.metric(f"Result: {target_m}", f"{res_m:.3f}")

st.markdown("---")

# 5. MATURITY COEFFICIENT (Mc)
st.subheader("Maturity Coefficient (M)")
st.latex(r"M_c = \frac{Mature\% + 0.6(Half\%) + 0.4(Dead\%)}{100}")

col_mc1, col_mc2 = st.columns([3, 1])
with col_mc1:
    target_mc = st.radio("Solve for (M):", ["Coefficient (M)", "Mature %", "Half-Mature %", "Dead %"], horizontal=True, key="solve_mc")
    if target_mc == "Coefficient (M)":
        m_val = st.number_input("Mature %", value=perc_m, key="mat_mc")
        h_val = st.number_input("Half-Mature %", value=perc_h, key="half_mc")
        d_val = st.number_input("Dead %", value=perc_d, key="dead_mc")
        res_mc = (m_val + 0.6*h_val + 0.4*d_val) / 100 if (m_val + h_val + d_val) > 0 else 0.0
    elif target_mc == "Mature %":
        mc_in = st.number_input("Coefficient (M)", value=0.0, key="mc_m")
        h_val = st.number_input("Half-Mature %", value=0.0, key="h_m")
        d_val = st.number_input("Dead %", value=0.0, key="d_m_mc")
        res_mc = (100 * mc_in) - (0.6 * h_val) - (0.4 * d_val) if mc_in > 0 else 0.0
    elif target_mc == "Half-Mature %":
        mc_in = st.number_input("Coefficient (M)", value=0.0, key="mc_h")
        m_val = st.number_input("Mature %", value=0.0, key="m_h")
        d_val = st.number_input("Dead %", value=0.0, key="d_h")
        res_mc = ((100 * mc_in) - m_val - (0.4 * d_val)) / 0.6 if mc_in > 0 else 0.0
    else:
        mc_in = st.number_input("Coefficient (M)", value=0.0, key="mc_d")
        m_val = st.number_input("Mature %", value=0.0, key="m_d_mc")
        h_val = st.number_input("Half-Mature %", value=0.0, key="h_d")
        res_mc = ((100 * mc_in) - m_val - (0.6 * h_val)) / 0.4 if mc_in > 0 else 0.0

with col_mc2:
    if res_mc != 0:
        st.metric(f"Result: {target_mc}", f"{res_mc:.3f}")

# REFERENCE TABLES 1 & 2
st.markdown("---")
with st.expander("📖 View Standard Reference Ranges"):
    st.markdown('**1. Visual Identification**')
    df_vis = pd.DataFrame({"Category": ["Mature", "Half-Mature", "Immature"], "Visual Appearance": ["Rod-like, swollen", "Rod-like, distinct line inside", "Flat ribbon, transparent"], "Wall Thickness": ["Thick", "Medium", "Thin (or None)"]})
    df_vis.index = range(1, len(df_vis) + 1)
    st.table(df_vis)

    st.markdown('**2. Maturity Ratio (\$M\$)**')
    df_m = pd.DataFrame({"Range": ["< 0.70", "0.70 - 0.80", "0.80 - 1.00", "1.00<"], "Verdict": ["Very Immature", "Immature", "Mature", "Very Mature"]})
    df_m.index = range(1, len(df_m) + 1)
    st.table(df_m)

st.markdown("---")

# 6. LUMEN / WALL THICKNESS RATIO
st.subheader("2. Theoretical Maturity (Lumen/Wall Ratio)")
st.latex(r"Ratio = \frac{\text{Lumen Width (L)}}{\text{Wall Thickness (W)}}")

col_lw1, col_lw2 = st.columns([3, 1])
with col_lw1:
    target_lw = st.radio("Solve for (L/W):", ["Ratio (L/W)", "Lumen Width (L)", "Wall Thickness (W)"], horizontal=True, key="solve_lw")
    if target_lw == "Ratio (L/W)":
        l_w = st.number_input("Lumen Width (L) [µm]", value=0.0, key="l_calc")
        w_t = st.number_input("Wall Thickness (W) [µm]", value=0.0, key="w_calc")
        res_lw = l_w / w_t if w_t > 0 else 0.0
    elif target_lw == "Lumen Width (L)":
        r_in = st.number_input("Target Ratio (L/W)", value=0.0, key="r_l")
        w_t = st.number_input("Wall Thickness (W) [µm]", value=0.0, key="w_l")
        res_lw = r_in * w_t
    else:
        l_w = st.number_input("Lumen Width (L) [µm]", value=0.0, key="l_w")
        r_in = st.number_input("Target Ratio (L/W)", value=0.0, key="r_w")
        res_lw = l_w / r_in if r_in > 0 else 0.0

with col_lw2:
    if res_lw > 0:
        st.metric(f"Result: {target_lw}", f"{res_lw:.3f}")

# REFERENCE TABLE 3
st.markdown("---")
with st.expander("📖 View Reference Standards"):
   st.markdown('**Lumen (L)/Wall (W)**')
   df_LW = pd.DataFrame({"Category": ["Mature", "Half-Mature", "Immature"], "Condition": ["Lumen (L)/Wall (W) < 1", "1 < Lumen (L)/Wall (W) < 2", "2 < Lumen (L)/Wall (W)"], "Ratio Range": ["< 1.0", "1.0 - 2.0", "2.0<"]})
   df_LW.index = range(1, len(df_LW) + 1)
   st.table(df_LW)

# 7. JUSTIFICATION FOOTER
st.info("""
**Parameters & Definitions:**
* **N:** Percentage of Mature fibers in the sample.
* **D:** Percentage of Dead (Immature) fibers in the sample.
* **\$M\$:** Maturity Ratio (The degree of cell wall thickening).
* **M:** Maturity Coefficient (Weighted average of fiber types).
""")
