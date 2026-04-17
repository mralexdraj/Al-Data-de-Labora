import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Metric Count Calculator", layout="wide", initial_sidebar_state="collapsed")

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
        st.switch_page("pages/Yarn's lab selection.py")

st.title("Metric Count (Nm) 🔬")
st.markdown("### **What is Metric Count?**")
st.markdown("""
<div style="text-align: justify;">
Metric Count (Nm) is a standard indirect yarn numbering system used primarily in Europe and for wool and synthetic fibers globally. It is formally defined as the number of 1000-meter hanks required to weigh one kilogram. In practical laboratory terms, this is equivalent to the length in kilometers per kilogram of weight. As an indirect system, the higher the Nm value, the finer the yarn.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 3. METHODOLOGY
st.subheader("1. Determination of Nm")
st.markdown("""
**Procedure:**
1. Measure the total length of the yarn sample in meters ($L$).
2. Weigh the sample accurately to find its mass in kilograms ($W$).
3. Calculate the Metric Count by dividing the length in kilometers by the weight in kilograms.
""")

st.latex(r"Nm = \frac{Length \ (km)}{Weight \ (kg)}")

# 4. CALCULATOR SECTION
st.subheader("2. Metric Analytical Calculator")

target_nm = st.radio(
    "Solve for:",
    ["Nm Count", "Length (m)", "Weight (kg)"],
    horizontal=True,
    key="solve_nm_fixed"
)

col_main1, col_main2 = st.columns([3, 1])

# Initialize Gatekeepers
l_g, w_g, nm_g = 0.0, 0.0, 0.0

with col_main1:
    if target_nm == "Nm Count":
        l_g = st.number_input("Enter Length [m]", value=0.0, key="l1_f")
        w_g = st.number_input("Enter Weight [kg]", value=0.0, key="w1_f")
        # Conversion: (meters/1000) / kg
        res_nm = (l_g / 1000) / w_g if w_g > 0 else 0.0
        
    elif target_nm == "Length (m)":
        nm_g = st.number_input("Enter Nm Count", value=0.0, key="nm2_f")
        w_g = st.number_input("Enter Weight [kg]", value=0.0, key="w2_f")
        # Conversion: Nm * kg * 1000
        res_nm = nm_g * w_g * 1000

    else: # Weight (kg)
        l_g = st.number_input("Enter Length [m]", value=0.0, key="l3_f")
        nm_g = st.number_input("Enter Nm Count", value=0.0, key="nm3_f")
        # Conversion: (meters/1000) / Nm
        res_nm = (l_g / 1000) / nm_g if nm_g > 0 else 0.0

with col_main2:
    if (l_g > 0 or w_g > 0 or nm_g > 0):
        u = " Nm" if "Count" in target_nm else (" m" if "Length" in target_nm else " kg")
        st.metric(f"Result: {target_nm}", f"{res_nm:.2f}{u}")

# 5. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **Length (m):** The total length of the yarn sample in meters.
* **Weight (kg):** The mass of the yarn sample measured in kilograms.
* **Nm (Metric Count):** The number of 1-kilometer hanks per kilogram ($km/kg$).
* **Indirect System:** A system where the count value increases as the yarn becomes finer.
        
**Historical Context:** The Metric system was designed to unify various regional European counts (like French and German) into a single standard based on decimal kilograms and meters.
""")