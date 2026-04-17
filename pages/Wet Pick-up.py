import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Wet Pick-up Analysis", layout="wide", initial_sidebar_state="collapsed")

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
        st.switch_page("pages/Processing's lab selection.py")

st.title("Wet Pick-up Analysis 🗜️")

# 3. DEFINITIONS
st.markdown("### **What is Wet Pick-up?**")
st.markdown("""
<div style="text-align: justify;">
Wet Pick-up (P%) is a fundamental parameter in textile finishing and padding processes. It represents the mass of liquid (water, dyes, or finishing chemicals) that a fabric retains after it has been immersed in a treatment bath and passed through the squeeze rollers of a padding mangle. Controlling the pick-up is crucial for ensuring the uniform application of chemicals, preventing shade variation, and optimizing energy consumption during the subsequent drying process.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Wet Pick-up Percentage")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Precisely weigh the dry fabric specimen before any treatment and record it as the Dry Weight (Wd).</li>
<li>Pass the fabric through the chemical bath or dye liquor in the padding mangle.</li>
<li>The fabric then travels through the nip (the point of contact between two rollers) where excess liquid is squeezed out under a specified Nip Pressure.</li>
<li>Immediately weigh the saturated fabric after it exits the rollers and record it as the Wet Weight (Ww).</li>
<li>Calculate the percentage of liquid retained relative to the initial dry weight of the fabric.</li>
</ol>
</div>
""", unsafe_allow_html=True)



# 5. CALCULATOR SECTION
st.subheader("2. Wet Pick-up Analytical Calculator")

st.latex(r"P\% = \left( \frac{W_{wet} - W_{dry}}{W_{dry}} \right) \times 100")

# MCP: Radio buttons placed outside and above columns
target_mode = st.radio(
    "Solve for:",
    ["Wet Pick-up (P) [%]", "Wet Weight (Ww) [g]", "Dry Weight (Wd) [g]"],
    horizontal=True,
    key="solver_wet_pickup"
)

# MCP: 3:1 Column Ratio
col_main1, col_main2 = st.columns([3, 1])

res_val = 0.0
ww_in, wd_in, p_in = 0.0, 0.0, 0.0

with col_main1:
    if "Pick-up" in target_mode:
        wd_in = st.number_input("Dry Weight of Fabric (Wd) [g]", value=0.0, key="wd_1")
        ww_in = st.number_input("Wet Weight of Fabric (Ww) [g]", value=0.0, key="ww_1")
        if wd_in > 0:
            res_val = ((ww_in - wd_in) / wd_in) * 100
            
    elif "Wet Weight" in target_mode:
        wd_in = st.number_input("Dry Weight of Fabric (Wd) [g]", value=0.0, key="wd_2")
        p_in = st.number_input("Wet Pick-up (P) [%]", value=0.0, key="p_2")
        res_val = wd_in * (1 + (p_in / 100))
        
    else: # Dry Weight
        ww_in = st.number_input("Wet Weight of Fabric (Ww) [g]", value=0.0, key="ww_3")
        p_in = st.number_input("Wet Pick-up (P) [%]", value=0.0, key="p_3")
        if p_in > -100:
            res_val = ww_in / (1 + (p_in / 100))

with col_main2:
    st.write("")
    st.write("")
    if res_val > 0:
        unit = " %" if "Pick-up" in target_mode else " g"
        st.metric(f"Result: {target_mode.split(' (')[0]}", f"{res_val:.2f}{unit}")

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Justification:**
* **Ww (Wet Weight):** The mass of the fabric after passing through the mangle, containing both fiber and liquor.
* **Wd (Dry Weight):** The initial conditioned mass of the fabric before liquid application.
* **Nip Pressure:** The mechanical force applied by the rollers; increasing this pressure reduces the P% by squeezing more liquid out.
* **Fiber Influence:** Highly absorbent fibers like cotton and viscose exhibit higher pick-up ranges (65-100%) compared to synthetic fibers like polyester (25-40%).
* **Padding Efficiency:** Correct pick-up ensures the exact required concentration of chemicals is applied to the fabric substrate without waste.
""")