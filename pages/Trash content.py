import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Fiber Lab - Trash Analysis", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Trash Analysis Lab 🏭")
st.markdown("### **What is Trash Content?**")
st.markdown("""
<div style="text-align: justify;">
Trash content refers to the non-lint material present in a raw cotton sample, such as leaf bits, stalk, seed coat fragments, and dust. Analyzing trash is vital for determining the commercial value of cotton and the cleaning efficiency of blowroom machinery. Higher trash content leads to increased waste, potential fiber damage during cleaning, and lower yarn quality.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- SECTION 1: CLEANING EFFICIENCY ---
st.subheader("1. Cleaning Efficiency (CE%)")
st.markdown("""
**Procedure:**
1. Determine the percentage of trash in the raw material before it enters the machine (Feed).
2. Measure the percentage of trash remaining in the material after it leaves the machine (Delivery).
3. Calculate the efficiency to evaluate the machine's performance in removing impurities.
""")
st.latex(r"CE\% = \frac{\text{Trash Feed} - \text{Trash Delivery}}{\text{Trash Feed}} \times 100")

col_ce1, col_ce2 = st.columns([3, 1])
with col_ce1:
    target_ce = st.radio("Solve for (Efficiency):", ["Efficiency (CE%)", "Trash in Feed", "Trash in Delivery"], horizontal=True, key="ce_solve")
    res_ce = 0.0
    if target_ce == "Efficiency (CE%)":
        t_feed = st.number_input("Trash in Feed [%]", value=0.0, key="tf1")
        t_del = st.number_input("Trash in Delivery [%]", value=0.0, key="td1")
        res_ce = ((t_feed - t_del) / t_feed * 100) if t_feed > 0 else 0.0
    elif target_ce == "Trash in Feed":
        ce_in = st.number_input("Cleaning Efficiency [%]", value=0.0, key="ce2")
        t_del = st.number_input("Trash in Delivery [%]", value=0.0, key="td2")
        res_ce = t_del / (1 - (ce_in / 100)) if ce_in < 100 else 0.0
    else: # Trash in Delivery
        t_feed = st.number_input("Trash in Feed [%]", value=0.0, key="tf3")
        ce_in = st.number_input("Cleaning Efficiency [%]", value=0.0, key="ce3")
        res_ce = t_feed * (1 - (ce_in / 100))
with col_ce2:
    if res_ce != 0:
        st.metric(f"Result: {target_ce}", f"{res_ce:.2f}%")

st.markdown("---")

# --- SECTION 2: TRASH CONTENT ---
st.subheader("2. Trash Content Analysis")
st.markdown("""
**Procedure:**
1. Weigh a raw cotton sample (Sample Weight).
2. Process the sample through a Shirley Analyzer or similar lint separator.
3. Weigh the separated non-lint material (Trash Weight) to find the percentage.
""")
st.latex(r"Trash\% = \frac{\text{Trash Weight}}{\text{Sample Weight}} \times 100")

col_tr1, col_tr2 = st.columns([3, 1])
with col_tr1:
    target_tr = st.radio("Solve for (Trash):", ["Trash %", "Trash Weight", "Sample Weight"], horizontal=True, key="tr_solve")
    res_tr = 0.0
    if target_tr == "Trash %":
        t_wt = st.number_input("Trash Weight [g]", value=0.0, key="tw1")
        s_wt = st.number_input("Sample Weight [g]", value=0.0, key="sw1")
        res_tr = (t_wt / s_wt * 100) if s_wt > 0 else 0.0
    elif target_tr == "Trash Weight":
        t_pct = st.number_input("Trash %", value=0.0, key="tp2")
        s_wt = st.number_input("Sample Weight [g]", value=0.0, key="sw2")
        res_tr = (t_pct * s_wt) / 100
    else: # Sample Weight
        t_wt = st.number_input("Trash Weight [g]", value=0.0, key="tw3")
        t_pct = st.number_input("Trash %", value=0.0, key="tp3")
        res_tr = (t_wt * 100) / t_pct if t_pct > 0 else 0.0
with col_tr2:
    if res_tr != 0:
        u = "%" if "Trash %" in target_tr else " g"
        st.metric(f"Result: {target_tr}", f"{res_tr:.2f}{u}")

st.markdown("---")

# --- SECTION 3: LINT CONTENT ---
st.subheader("3. Lint Content (Fiber Recovery)")
st.latex(r"Lint\% = 100\% - Trash\%")

# Initialize gatekeepers
t_pct, l_pct = 0.0, 0.0

col_li1, col_li2 = st.columns([3, 1])
with col_li1:
    target_li = st.radio("Solve for (Lint):", ["Lint %", "Trash %"], horizontal=True, key="li_solve")
    res_li = 0.0
    if target_li == "Lint %":
        t_pct = st.number_input("Known Trash %", value=0.0, key="tp_li1")
        res_li = 100 - t_pct
    else: # Trash % from Lint %
        l_pct = st.number_input("Known Lint %", value=0.0, key="lp_li2")
        res_li = 100 - l_pct

with col_li2:
    # Only show if the user has entered a value greater than 0
    if t_pct > 0 or l_pct > 0:
        st.metric(f"Result: {target_li}", f"{res_li:.2f}%")

# 5. REFERENCE DATA
st.markdown("---")
with st.expander("📖 View Standard Machine Ranges"):
    st.write("Average expected cleaning efficiencies for standard blowroom machinery:")
    data_ref = {
        "Machine Type": ["Step Cleaner", "Monocylinder", "ERM Cleaner", "Shirley Analyzer (Lab)"],
        "Expected Efficiency (%)": ["30 - 40%", "40 - 50%", "50 - 60%", "95 - 99%"]
    }
    df_ref = pd.DataFrame(data_ref)
    df_ref.index = range(1, len(df_ref) + 1)
    st.table(df_ref)

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **Trash Feed:** The percentage of impurities in the material before cleaning.
* **Trash Delivery:** The percentage of impurities remaining after a cleaning process.
* **CE% (Cleaning Efficiency):** A measure of how effectively a machine removes trash.
* **Trash Weight:** The actual mass of non-lint material recovered from a sample.
* **Lint Content:** The percentage of pure, usable fiber recovered after analysis.
        
**Note:** Standardized testing for trash content is typically performed using the Shirley Analyzer, which uses buoyancy differences to separate lint from heavier trash particles.
""")