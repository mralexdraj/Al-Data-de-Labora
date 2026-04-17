import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE SETUP
st.set_page_config(page_title="Fabric Lab - Cover Factor", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Fabric Cover Factor Analysis 🧶")

# 3. DEFINITIONS
st.markdown("### **What is Fabric Cover Factor?**")
st.markdown("""
<div style="text-align: justify;">
The Fabric Cover Factor (K) is a numerical expression indicating the extent to which the area of a fabric is covered by one set of threads (warp or weft). It serves as a measure of the density, opacity, and compactness of the weave construction. In the cotton system, it represents the ratio of threads per inch to the square root of the cotton count. When considering both sets of threads, the Total Cloth Cover Factor (Kc) accounts for the overlap at thread intersections to provide an accurate representation of the total area covered.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Cover Parameters")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Extract a sample of the fabric and determine the thread density by counting the Ends Per Inch (n1) and Picks Per Inch (n2) using a pick glass or traveling microscope.</li>
<li>Determine the yarn count (Ne) for both warp and weft sets using a Knowles balance or by weighing a known length of yarn removed from the fabric.</li>
<li>Calculate the individual fractional cover for each direction to identify the relative density of each yarn set.</li>
<li>Apply the geometric overlap formula to calculate the Total Cloth Cover Factor, which mathematically subtracts the intersection areas to prevent double-counting.</li>
</ol>
</div>
""", unsafe_allow_html=True)



# 5. CALCULATORS

# --- SECTION I: INDIVIDUAL FACTORS (Side-by-Side) ---
st.subheader("2. Individual Cover Factors (Warp & Weft)")

# WARP CALCULATOR
st.markdown("**Warp Cover Factor (K1)**")
target_k1 = st.radio(
    "Solve for (Warp):", 
    ["Warp Cover Factor (K1)", "Ends Per Inch (n1)", "Warp Count (N1) [Ne]"], 
    horizontal=True, key="rk1"
)
col1_in, col1_res = st.columns([3, 1])
res_k1 = 0.0
with col1_in:
    if "K1" in target_k1:
        n1 = st.number_input("Ends Per Inch (n1)", value=0.0, key="n1_in")
        N1 = st.number_input("Warp Count (N1) [Ne]", value=0.0, key="N1_in")
        if N1 > 0: res_k1 = n1 / np.sqrt(N1)
    elif "n1" in target_k1:
        K1 = st.number_input("Warp Cover Factor (K1)", value=0.0, key="k1_in")
        N1 = st.number_input("Warp Count (N1) [Ne]", value=0.0, key="N1_in2")
        res_k1 = K1 * np.sqrt(N1)
    else:
        K1 = st.number_input("Warp Cover Factor (K1)", value=0.0, key="k1_in2")
        n1 = st.number_input("Ends Per Inch (n1)", value=0.0, key="n1_in2")
        if K1 > 0: res_k1 = (n1 / K1)**2
with col1_res:
    if res_k1 > 0:
        st.metric(f"Result: {target_k1.split(' (')[0]}", f"{res_k1:.2f}")

st.write("")

# WEFT CALCULATOR
st.markdown("**Weft Cover Factor (K2)**")
target_k2 = st.radio(
    "Solve for (Weft):", 
    ["Weft Cover Factor (K2)", "Picks Per Inch (n2)", "Weft Count (N2) [Ne]"], 
    horizontal=True, key="rk2"
)
col2_in, col2_res = st.columns([3, 1])
res_k2 = 0.0
with col2_in:
    if "K2" in target_k2:
        n2 = st.number_input("Picks Per Inch (n2)", value=0.0, key="n2_in")
        N2 = st.number_input("Weft Count (N2) [Ne]", value=0.0, key="N2_in")
        if N2 > 0: res_k2 = n2 / np.sqrt(N2)
    elif "n2" in target_k2:
        K2 = st.number_input("Weft Cover Factor (K2)", value=0.0, key="k2_in")
        N2 = st.number_input("Weft Count (N2) [Ne]", value=0.0, key="N2_in2")
        res_k2 = K2 * np.sqrt(N2)
    else:
        K2 = st.number_input("Weft Cover Factor (K2)", value=0.0, key="k2_in2")
        n2 = st.number_input("Picks Per Inch (n2)", value=0.0, key="n2_in2")
        if K2 > 0: res_k2 = (n2 / K2)**2
with col2_res:
    if res_k2 > 0:
        st.metric(f"Result: {target_k2.split(' (')[0]}", f"{res_k2:.2f}")

st.markdown("---")

# --- SECTION II: TOTAL CLOTH COVER ---
st.subheader("3. Total Cloth Cover Factor (Kc)")
st.latex(r"K_c = K_1 + K_2 - \frac{K_1 \times K_2}{28}")

target_kc = st.radio(
    "Solve for (Total):", 
    ["Total Cover Factor (Kc)", "Required Warp Factor (K1)", "Required Weft Factor (K2)"], 
    horizontal=True, key="rkc"
)
col3_in, col3_res = st.columns([3, 1])
res_kc = 0.0
with col3_in:
    if "Kc" in target_kc:
        k1_v = st.number_input("Warp Factor (K1)", value=res_k1 if res_k1 > 0 else 0.0, key="tk1")
        k2_v = st.number_input("Weft Factor (K2)", value=res_k2 if res_k2 > 0 else 0.0, key="tk2")
        res_kc = k1_v + k2_v - ((k1_v * k2_v) / 28)
    elif "K1" in target_kc:
        kc_v = st.number_input("Target Total Cover (Kc)", value=0.0, key="tkc1")
        k2_v = st.number_input("Known Weft Factor (K2)", value=res_k2 if res_k2 > 0 else 0.0, key="tk2b")
        denom = (1 - (k2_v / 28))
        if denom != 0: res_kc = (kc_v - k2_v) / denom
    else:
        kc_v = st.number_input("Target Total Cover (Kc)", value=0.0, key="tkc2")
        k1_v = st.number_input("Known Warp Factor (K1)", value=res_k1 if res_k1 > 0 else 0.0, key="tk1b")
        denom = (1 - (k1_v / 28))
        if denom != 0: res_kc = (kc_v - k1_v) / denom
with col3_res:
    if res_kc > 0:
        st.metric(f"Result: {target_kc.split(' (')[0]}", f"{res_kc:.2f}")

# 6. JUSTIFICATION & DERIVATION
st.markdown("---")
st.info("""
**Parameters & Derivation:**
* **K (Cover Factor):** The ratio of threads per inch to the square root of the yarn count ($K = n / \sqrt{Ne}$). It is a simplified version of Fractional Cover ($C$), where $K = 28 \times C$.
* **Kc (Total Cover):** Derived from the geometry of overlapping circles (yarns). To find the area actually covered, we add warp and weft fractional covers and subtract the overlap: $C_{total} = C_1 + C_2 - (C_1 \times C_2)$.
* **The Constant 28:** In the cotton system, the yarn diameter is approximately $1 / (28\sqrt{Ne})$ inches. 
* **n1 / n2:** Ends per inch and Picks per inch, respectively.
* **Ne:** The English cotton count; a coarser yarn (lower Ne) has a larger diameter, increasing the cover.
* **Overlap Logic:** The term $(K_1 \times K_2) / 28$ mathematically represents the area where warp and weft yarns overlap, ensuring intersections are not counted twice.
""")