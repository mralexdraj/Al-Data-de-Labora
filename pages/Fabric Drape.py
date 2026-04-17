import streamlit as st
import pandas as pd
import math

# 1. PAGE SETUP
st.set_page_config(page_title="Fabric Drape Lab", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Fabric Drape Lab 👗")

# 3. DEFINITIONS
st.markdown("### **The Drape Coefficient**")
st.markdown("""
<div style="text-align: justify;">
Fabric drape is the manner in which a fabric hangs or falls over a three-dimensional form under its own weight. It is a critical aesthetic property that determines how a garment conforms to the human body. The Drape Coefficient (F) is a numerical value representing the percentage of the area of a fabric specimen that is covered by its projected shadow. A lower drape coefficient indicates a fluid fabric that drapes easily, while a higher coefficient indicates a stiff fabric.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Drape Coefficient")

st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Prepare a circular fabric specimen of 30 cm diameter and mount it centrally on an 18 cm diameter supporting disc.</li>
<li>Use a Drapemeter to allow the fabric to hang naturally and project its shadow onto a ring of paper.</li>
<li>Trace the shadow outline, cut it out, and weigh the resulting paper shape.</li>
<li>Compare the weight of the shadow paper against the proportional weights of the supporting disc and the full specimen area.</li>
</ol>
</div>
""", unsafe_allow_html=True)

st.latex(r"F = \frac{A_s - A_d}{A_D - A_d}")

# 5. CALCULATOR SECTION
target_mode = st.radio(
        "Solve for:",
        ["Drape Coefficient (F) [%]", "Projected Area (As) [cm²]", "Supporting Disc Area (Ad) [cm²]", "Total Specimen Area (AD) [cm²]"],
        horizontal=True,
        key="solver_drape_fixed"
    )
col_main1, col_main2 = st.columns([3, 1])

with col_main1:
    
    res_val = 0.0
    as_in, ad_in, ad_large, f_in = 0.0, 0.0, 0.0, 0.0

    if target_mode == "Drape Coefficient (F) [%]":
        as_in = st.number_input("Projected Area of Specimen (As) [cm²]", value=0.0, key="as_1")
        ad_in = st.number_input("Area of Supporting Disc (Ad) [cm²]", value=0.0, key="ad_1")
        ad_large = st.number_input("Total Specimen Area (AD) [cm²]", value=0.0, key="adl_1")
        if (ad_large - ad_in) != 0:
            res_val = ((as_in - ad_in) / (ad_large - ad_in)) * 100

    elif target_mode == "Projected Area (As) [cm²]":
        f_in = st.number_input("Drape Coefficient (F) [%]", value=0.0, key="f_2")
        ad_in = st.number_input("Area of Supporting Disc (Ad) [cm²]", value=0.0, key="ad_2")
        ad_large = st.number_input("Total Specimen Area (AD) [cm²]", value=0.0, key="adl_2")
        res_val = ((f_in / 100) * (ad_large - ad_in)) + ad_in

    elif target_mode == "Supporting Disc Area (Ad) [cm²]":
        f_in = st.number_input("Drape Coefficient (F) [%]", value=0.0, key="f_3")
        as_in = st.number_input("Projected Area of Specimen (As) [cm²]", value=0.0, key="as_3")
        ad_large = st.number_input("Total Specimen Area (AD) [cm²]", value=0.0, key="adl_3")
        if f_in != 100:
            res_val = (as_in - ((f_in / 100) * ad_large)) / (1 - (f_in / 100))

    else: # Total Specimen Area (AD)
        f_in = st.number_input("Drape Coefficient (F) [%]", value=0.0, key="f_4")
        as_in = st.number_input("Projected Area of Specimen (As) [cm²]", value=0.0, key="as_4")
        ad_in = st.number_input("Area of Supporting Disc (Ad) [cm²]", value=0.0, key="ad_4")
        if f_in > 0:
            res_val = ((as_in - ad_in) / (f_in / 100)) + ad_in

with col_main2:
    st.write("")
    st.write("")
    if res_val > 0:
        u = " %" if "Coefficient" in target_mode else " cm²"
        st.metric(f"Result: {target_mode.split(' (')[0]}", f"{res_val:.2f}{u}")

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Units:**
* **F (Drape Coefficient):** The percentage of the specimen area covered by its projected shadow.
* **As (Projected Area):** The area of the draped fabric's shadow [cm²].
* **Ad (Supporting Disc Area):** The area of the internal disc that holds the specimen centrally [cm²].
* **AD (Specimen Area):** The total area of the flat circular specimen before draping [cm²].
* **Weight Method:** In lab practice, the weight of paper cutouts (in grams) is used as a direct proxy for these area values.
""")