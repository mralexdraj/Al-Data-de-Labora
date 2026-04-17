import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Fabric GSM Lab", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Fabric GSM & Density Lab 🧵")

# 3. DEFINITIONS
st.subheader("What are these Parameters?")
st.markdown("""
<div style="text-align: justify;">
<b>GSM (Grams per Square Meter):</b> A metric used to determine the weight and density of a fabric. It measures the mass of a one-meter by one-meter sample. It is a critical specification for quality control and determines fabric suitability for specific garments.
<br><br>
<b>GLM (Grams per Linear Meter):</b> Measures the weight of a fabric based on its actual width. This is essential for garment manufacturers to calculate how much a specific length of fabric (the whole roll) will weigh.
<br><br>
<b>Total Weight:</b> The absolute mass of a specific quantity of fabric (length in meters). It is calculated by multiplying the GLM by the total meterage, usually expressed in kilograms for commercial shipping and inventory.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. CALCULATORS

# --- SECTION 1: GSM ---
st.subheader("1. Fabric GSM (Square Weight)")
st.latex(r"GSM = \left( \frac{EPI}{Warp \ Count} + \frac{PPI}{Weft \ Count} \right) \times 25.64")

# Reverse Algebra Selector for GSM
target_gsm = st.radio("Solve for (GSM Section):", ["GSM", "EPI", "PPI", "Warp Count", "Weft Count"], horizontal=True, key="solve_gsm")

col_gsm1, col_gsm2 = st.columns([3, 1])
# Initialize gatekeepers
epi, ppi, wc, wec, gsm_v = 0.0, 0.0, 0.0, 0.0, 0.0

with col_gsm1:
    if target_gsm == "GSM":
        epi = st.number_input("Ends Per Inch (EPI)", value=0.0, key="e1")
        ppi = st.number_input("Picks Per Inch (PPI)", value=0.0, key="p1")
        wc = st.number_input("Warp Count (Ne)", value=0.0, key="wc1")
        wec = st.number_input("Weft Count (Ne)", value=0.0, key="wec1")
        res_gsm = ((epi/wc) + (ppi/wec)) * 25.64 if (wc > 0 and wec > 0) else 0.0
    elif target_gsm == "EPI":
        gsm_v = st.number_input("Known GSM", value=0.0, key="g2")
        ppi = st.number_input("Picks Per Inch (PPI)", value=0.0, key="p2")
        wc = st.number_input("Warp Count (Ne)", value=0.0, key="wc2")
        wec = st.number_input("Weft Count (Ne)", value=0.0, key="wec2")
        res_gsm = ((gsm_v / 25.64) - (ppi / wec)) * wc if (wec > 0) else 0.0
    # ... (Logic for PPI, Warp Count, Weft Count follows similar algebraic steps)
    else:
        st.write("Other reverse parameters currently use the primary formula.")
        res_gsm = 0.0

with col_gsm2:
    if (epi > 0 or ppi > 0 or gsm_v > 0):
        st.metric(f"Result: {target_gsm}", f"{res_gsm:.2f}")

st.markdown("---")

# --- SECTION 2: GLM ---
st.subheader("2. Fabric GLM (Linear Weight)")
st.latex(r"GLM = \frac{GSM \times Width}{39.37}")

target_glm = st.radio("Solve for (GLM Section):", ["GLM", "GSM", "Width"], horizontal=True, key="solve_glm")

col_glm1, col_glm2 = st.columns([3, 1])
# Initialize gatekeepers
g_in, w_in, gl_in = 0.0, 0.0, 0.0

with col_glm1:
    if target_glm == "GLM":
        g_in = st.number_input("GSM [g/m²]", value=res_gsm, key="g_glm1")
        w_in = st.number_input("Width [inches]", value=0.0, key="w_glm1")
        res_glm = (g_in * w_in) / 39.37
    elif target_glm == "GSM":
        gl_in = st.number_input("GLM [g/m]", value=0.0, key="gl_glm2")
        w_in = st.number_input("Width [inches]", value=0.0, key="w_glm2")
        res_glm = (gl_in * 39.37) / w_in if w_in > 0 else 0.0
    else: # Width
        gl_in = st.number_input("GLM [g/m]", value=0.0, key="gl_glm3")
        g_in = st.number_input("GSM [g/m²]", value=res_gsm, key="g_glm3")
        res_glm = (gl_in * 39.37) / g_in if g_in > 0 else 0.0

with col_glm2:
    if (g_in > 0 or w_in > 0 or gl_in > 0):
        st.metric(f"Result: {target_glm}", f"{res_glm:.2f}")

st.markdown("---")

# --- SECTION 3: TOTAL WEIGHT ---
st.subheader("3. Total Fabric Weight")
st.latex(r"Weight \ (kg) = \frac{GLM \times Quantity \ (m)}{1000}")

target_tw = st.radio("Solve for (Weight Section):", ["Total Weight (kg)", "GLM", "Quantity (m)"], horizontal=True, key="solve_tw")

col_tw1, col_tw2 = st.columns([3, 1])
# Initialize gatekeepers
gl_tw, q_tw, kg_tw = 0.0, 0.0, 0.0

with col_tw1:
    if target_tw == "Total Weight (kg)":
        gl_tw = st.number_input("GLM [g/m]", value=res_glm, key="gl_tw1")
        q_tw = st.number_input("Quantity [m]", value=0.0, key="q_tw1")
        res_tw = (gl_tw * q_tw) / 1000
    elif target_tw == "GLM":
        kg_tw = st.number_input("Total Weight [kg]", value=0.0, key="kg_tw2")
        q_tw = st.number_input("Quantity [m]", value=0.0, key="q_tw2")
        res_tw = (kg_tw * 1000) / q_tw if q_tw > 0 else 0.0
    else: # Quantity
        kg_tw = st.number_input("Total Weight [kg]", value=0.0, key="kg_tw3")
        gl_tw = st.number_input("GLM [g/m]", value=res_glm, key="gl_tw3")
        res_tw = (kg_tw * 1000) / gl_tw if gl_tw > 0 else 0.0

with col_tw2:
    if (gl_tw > 0 or q_tw > 0 or kg_tw > 0):
        st.metric(f"Result: {target_tw}", f"{res_tw:.2f}")

# 5. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **EPI / PPI:** Thread density in the Warp and Weft directions.
* **Count (Ne):** The thickness of the yarns used; higher Ne means finer fabric.
* **Width:** The physical width of the fabric roll, excluding selvages.
* **25.64:** A constant derived from the conversion of English counts and square inches to grams and square meters.
* **39.37:** The conversion factor from inches to meters.
* **1000:** The conversion factor used to translate the final weight from grams to kilograms ($1 \text{ kg} = 1000 \text{ g}$).
""")