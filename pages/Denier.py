import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Denier Calculator", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Denier (Direct System) 🔬")
st.markdown("### **What is Denier?**")
st.markdown("""
<div style="text-align: justify;">
Denier is a direct yarn numbering system predominantly used for silk and synthetic filament yarns like nylon and polyester. It is defined as the weight in grams of 9,000 meters of yarn. Because it is a direct system, the denier value is a straight measure of the yarn's linear density: a higher denier indicates a thicker, heavier yarn, while a lower denier represents a finer yarn. This system is particularly useful in the hosiery and filament industries to specify fiber thickness with high precision.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 3. METHODOLOGY
st.subheader("1. Determination of Denier")
st.markdown("""
**Procedure:**
1. Measure a specific length of the filament yarn in meters ($L$).
2. Use a high-precision electronic balance to find the weight of the sample in grams ($W$).
3. Calculate the Denier by determining the weight equivalent for a standard 9,000-meter length.
""")

st.latex(r"Denier = \frac{Weight \ (g)}{Length \ (9km)} = \frac{Weight \ (g)}{Length \ (9000m)}")

# 4. CALCULATOR SECTION
st.subheader("2. Denier Analytical Calculator")

# Selection for Reverse Algebra
target_den = st.radio(
    "Solve for:",
    ["Denier Value", "Weight (g)", "Length (m)"],
    horizontal=True,
    key="solve_den_master"
)

col_main1, col_main2 = st.columns([3, 1])

# Initialize Gatekeepers
w_g, l_g, den_g = 0.0, 0.0, 0.0

with col_main1:
    if target_den == "Denier Value":
        w_g = st.number_input("Enter Weight [g]", value=0.0, key="w1_d")
        l_g = st.number_input("Enter Length [m]", value=0.0, key="l1_d")
        # Formula: (W * 9000) / L
        res_den = (w_g * 9000) / l_g if l_g > 0 else 0.0
        
    elif target_den == "Weight (g)":
        den_g = st.number_input("Enter Denier Value", value=0.0, key="den2_d")
        l_g = st.number_input("Enter Length [m]", value=0.0, key="l2_d")
        # Formula: (Denier * L) / 9000
        res_den = (den_g * l_g) / 9000

    else: # Length (m)
        w_g = st.number_input("Enter Weight [g]", value=0.0, key="w3_d")
        den_g = st.number_input("Enter Denier Value", value=0.0, key="den3_d")
        # Formula: (W * 9000) / Denier
        res_den = (w_g * 9000) / den_g if den_g > 0 else 0.0

with col_main2:
    # Result Display Guard (Metric only appears if inputs > 0)
    if (w_g > 0 or l_g > 0 or den_g > 0):
        u = " Denier" if "Value" in target_den else (" g" if "Weight" in target_den else " m")
        st.metric(f"Result: {target_den}", f"{res_den:.2f}{u}")

# 5. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **Weight (g):** The mass of the yarn filament in grams.
* **Length (m):** The total length of the filament measured in meters.
* **Denier:** The weight in grams of 9,000 meters of yarn.
* **Direct System:** A system where numerical count is proportional to the yarn's cross-sectional area.
        
**Industrial Note:** While Tex is the universal SI unit, Denier remains the industry standard for identifying the "sheerness" of hosiery and the thickness of synthetic microfiber.
""")