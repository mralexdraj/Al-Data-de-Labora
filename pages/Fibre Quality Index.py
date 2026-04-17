import streamlit as st
import pandas as pd
import math

# 1. PAGE SETUP
st.set_page_config(page_title="Fiber Lab - FQI", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Fibre Quality Index (FQI) 🧪")
st.markdown("### **What is FQI?**")
st.markdown("""
<div style="text-align: justify;">
The Fibre Quality Index (FQI) is a comprehensive mathematical value used to assess the overall spinning potential of cotton. 
By combining length, strength, and fineness into a single index, it provides a more accurate prediction of yarn quality 
and the Highest Spinnable Count than any single fiber property alone.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 3. METHODOLOGY
st.subheader("FQI Analysis")
st.markdown("""
**Procedure:**
1. Determine the **Mean Length (L)** of the cotton sample using a comb sorter or HVI.
2. Measure the **Fibre Strength (S)** in grams per tex.
3. Obtain the **Micronaire (M)** value representing the fiber fineness.
4. Calculate the index to evaluate suitability for specific yarn counts.
""")

st.latex(r"FQI = \frac{L \times S}{M}")

# 4. CALCULATOR SECTION
col_f1, col_f2 = st.columns([3, 1])

with col_f1:
    target_fqi = st.radio(
        "Solve for:",
        ["FQI Value", "Mean Length (L)", "Fibre Strength (S)", "Micronaire (M)"],
        horizontal=True,
        key="solve_fqi_final"
    )
    
    res_fqi = 0.0

    if target_fqi == "FQI Value":
        l_in = st.number_input("Mean Length (L) [mm]", value=0.0, key="l_f1")
        s_in = st.number_input("Fibre Strength (S) [g/tex]", value=0.0, key="s_f1")
        m_in = st.number_input("Micronaire (M) [µg/inch]", value=0.0, key="m_f1")
        res_fqi = (l_in * s_in) / m_in if m_in > 0 else 0.0

    elif target_fqi == "Mean Length (L)":
        fqi_in = st.number_input("Target FQI Value", value=0.0, key="fqi_l2")
        m_in = st.number_input("Micronaire (M) [µg/inch]", value=0.0, key="m_l2")
        s_in = st.number_input("Fibre Strength (S) [g/tex]", value=0.0, key="s_l2")
        res_fqi = (fqi_in * m_in) / s_in if s_in > 0 else 0.0

    elif target_fqi == "Fibre Strength (S)":
        fqi_in = st.number_input("Target FQI Value", value=0.0, key="fqi_s3")
        m_in = st.number_input("Micronaire (M) [µg/inch]", value=0.0, key="m_s3")
        l_in = st.number_input("Mean Length (L) [mm]", value=0.0, key="l_s3")
        res_fqi = (fqi_in * m_in) / l_in if l_in > 0 else 0.0

    else: # Micronaire (M)
        l_in = st.number_input("Mean Length (L) [mm]", value=0.0, key="l_m4")
        s_in = st.number_input("Fibre Strength (S) [g/tex]", value=0.0, key="s_m4")
        fqi_in = st.number_input("Target FQI Value", value=0.0, key="fqi_m4")
        res_fqi = (l_in * s_in) / fqi_in if fqi_in > 0 else 0.0

with col_f2:
    if res_fqi > 0:
        st.metric(f"Result: {target_fqi}", f"{res_fqi:.2f}")

# 5. REFERENCE DATA
st.markdown("---")
with st.expander("📖 View FQI Quality Reference"):
    st.write("Standard interpretation of FQI values for spinning potential:")
    data_q = {
        "FQI Range": ["< 35", "35 - 45", "45 - 60", "60 - 80", "80 <"],
        "Spinning Quality": ["Very Poor", "Poor", "Fair", "Good", "Excellent"],
        "Suitability": ["Not suitable for quality yarn", "Coarse counts only", "Medium count yarns", "Fine counts", "Superfine counts"]
    }
    df_q = pd.DataFrame(data_q)
    df_q.index = range(1, len(df_q) + 1)
    st.table(df_q)

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **L (Mean Length):** The average length of the fibers in the sample (mm).
* **S (Fibre Strength):** The tenacity or breaking strength expressed in grams per tex (g/tex).
* **M (Micronaire):** An indicator of fiber fineness and maturity expressed in micrograms per inch (µg/inch).
* **FQI:** A composite index where higher values indicate better spinning performance and higher yarn strength.
""")