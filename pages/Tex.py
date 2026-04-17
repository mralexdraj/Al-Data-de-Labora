import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Tex Calculator", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Tex (Direct System) 🔬")
st.markdown("### **What is Tex?**")
st.markdown("""
<div style="text-align: justify;">
Tex is a universal, direct yarn numbering system adopted as the SI standard for the textile industry. It defines the linear density of a yarn as the mass in grams per one kilometer (1000 meters) of length. Because it is a direct system, the Tex value is directly proportional to the yarn's thickness: a higher Tex number indicates a coarser or thicker yarn, while a lower number indicates a finer yarn. This system is designed to replace various regional indirect counts with a single, weight-based metric applicable to all fiber types.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 3. METHODOLOGY
st.subheader("1. Determination of Tex")
st.markdown("""
**Procedure:**
1. Measure a known length of yarn in meters ($L$).
2. Accurately weigh the yarn sample to find its mass in grams ($W$).
3. Calculate the Tex value by determining the weight per one kilometer (1000 meters).
""")

st.latex(r"Tex = \frac{Weight \ (g)}{Length \ (km)} = \frac{Weight \ (g)}{Length \ (1000m)}")

# 4. CALCULATOR SECTION
st.subheader("2. Tex Analytical Calculator")

# Selection for Reverse Algebra
target_tex = st.radio(
    "Solve for:",
    ["Tex Value", "Weight (g)", "Length (m)"],
    horizontal=True,
    key="solve_tex_master"
)

col_main1, col_main2 = st.columns([3, 1])

# Initialize Gatekeepers
w_g, l_g, tex_g = 0.0, 0.0, 0.0

with col_main1:
    if target_tex == "Tex Value":
        w_g = st.number_input("Enter Weight [g]", value=0.0, key="w1_t")
        l_g = st.number_input("Enter Length [m]", value=0.0, key="l1_t")
        # Formula: (W * 1000) / L
        res_tex = (w_g * 1000) / l_g if l_g > 0 else 0.0
        
    elif target_tex == "Weight (g)":
        tex_g = st.number_input("Enter Tex Value", value=0.0, key="tex2_t")
        l_g = st.number_input("Enter Length [m]", value=0.0, key="l2_t")
        # Formula: (Tex * L) / 1000
        res_tex = (tex_g * l_g) / 1000

    else: # Length (m)
        w_g = st.number_input("Enter Weight [g]", value=0.0, key="w3_t")
        tex_g = st.number_input("Enter Tex Value", value=0.0, key="tex3_t")
        # Formula: (W * 1000) / Tex
        res_tex = (w_g * 1000) / tex_g if tex_g > 0 else 0.0

with col_main2:
    # Result Display Guard (Metric only appears if inputs > 0)
    if (w_g > 0 or l_g > 0 or tex_g > 0):
        u = " Tex" if "Value" in target_tex else (" g" if "Weight" in target_tex else " m")
        st.metric(f"Result: {target_tex}", f"{res_tex:.2f}{u}")

# 5. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **Weight (g):** The mass of the yarn sample in grams.
* **Length (m):** The total length of the sample measured in meters.
* **Tex:** The weight in grams of 1,000 meters of yarn.
* **Direct System:** A system where the numerical count increases as the yarn becomes thicker.
        
**Industrial Standard:** Tex is the preferred unit for international trade and is the base for other derived units like decitex (dtex) and millitex (mtex).
""")