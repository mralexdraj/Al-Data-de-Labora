import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="English Count Calculator", layout="wide", initial_sidebar_state="collapsed")

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

st.title("English Count (Ne) 🔬")
st.markdown("### **What is English Count?**")
st.markdown("""
<div style="text-align: justify;">
English Count, denoted as Ne, is the most widely used indirect yarn numbering system in the cotton industry. It originated from the British textile tradition and is defined as the number of hanks, each measuring 840 yards in length, that weigh exactly one pound. Since it is an indirect system, the count is inversely proportional to the yarn's linear density; therefore, a higher Ne number represents a finer yarn, while a lower number indicates a coarser yarn.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 3. METHODOLOGY
st.subheader("1. Determination of Ne")
st.markdown("""
**Procedure:**
1. Measure the total length of the yarn sample in hanks (1 hank = 840 yards).
2. Weigh the sample accurately to determine its mass in pounds (lb).
3. Divide the number of hanks by the weight in pounds to find the English Count.
""")

st.latex(r"Ne = \frac{Length \ (Hanks)}{Weight \ (lb)}")
st.info("**Unit Note:** To convert yards to hanks, use the relationship: $Hanks = \Large\\frac{Yards}{840}$")

# 4. CALCULATOR SECTION
st.subheader("2. Ne Analytical Calculator")

# Selection for Reverse Algebra
target_ne = st.radio(
    "Solve for:",
    ["Ne Count", "Length (Hanks)", "Weight (lb)"],
    horizontal=True,
    key="solve_ne_master"
)

col_main1, col_main2 = st.columns([3, 1])

# Initialize Gatekeepers
h_g, w_g, ne_g = 0.0, 0.0, 0.0

with col_main1:
    if target_ne == "Ne Count":
        h_g = st.number_input("Enter Length [Hanks]", value=0.0, key="h1")
        w_g = st.number_input("Enter Weight [lb]", value=0.0, key="w1")
        res_ne = h_g / w_g if w_g > 0 else 0.0
        
    elif target_ne == "Length (Hanks)":
        ne_g = st.number_input("Enter Ne Count", value=0.0, key="ne2")
        w_g = st.number_input("Enter Weight [lb]", value=0.0, key="w2")
        res_ne = ne_g * w_g

    else: # Weight (lb)
        h_g = st.number_input("Enter Length [Hanks]", value=0.0, key="h3")
        ne_g = st.number_input("Enter Ne Count", value=0.0, key="ne3")
        res_ne = h_g / ne_g if ne_g > 0 else 0.0

with col_main2:
    # Result Display Guard (Metric only appears if inputs > 0)
    if (h_g > 0 or w_g > 0 or ne_g > 0):
        u = " Ne" if "Count" in target_ne else (" Hanks" if "Length" in target_ne else " lb")
        st.metric(f"Result: {target_ne}", f"{res_ne:.2f}{u}")

# 5. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **Hank:** A standard length unit for cotton yarn equal to 840 yards.
* **Weight (lb):** The mass of the yarn sample measured in pounds.
* **Ne (English Count):** The number of 840-yard hanks per pound ($hanks/lb$).
* **Indirect System:** A numbering system where the count decreases as the yarn becomes heavier.
        
**Industrial Standard:** English Count remains the primary specification for cotton spinning mills and is the basis for calculating the Count Strength Product (CSP) in quality testing.
""")