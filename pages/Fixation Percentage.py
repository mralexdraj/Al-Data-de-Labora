import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Fixation Analysis", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Dye Fixation Analysis 🧪")

# 3. DEFINITIONS
st.markdown("### **What is Dye Fixation?**")
st.markdown("""
<div style="text-align: justify;">
Dye Fixation (%F) is the measure of the amount of dye that has chemically bonded or physically trapped within the fiber structure, remaining after the post-dyeing washing-off process. While exhaustion measures the dye moving from the liquor to the fiber, fixation represents the permanent color yield. Fixation efficiency is a vital metric for reactive dyes on cotton, as unfixed dye (hydrolyzed dye) can lead to poor wash fastness and increased environmental load in the effluent.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. METHODOLOGY
st.subheader("1. Determination of Fixation & Efficiency")
st.markdown("""
<div style="text-align: justify;">
<b>Procedure:</b>
<ol>
<li>Measure the initial weight of the dye taken for the dyeing process ($W_{total}$).</li>
<li>Conduct the dyeing process and record the weight of dye that has successfully migrated from the bath to the fiber (Exhausted Dye).</li>
<li>Perform a standardized "soap-off" or washing procedure to remove any loosely held or unreacted dye from the fiber surface.</li>
<li>Determine the weight of the dye remaining permanently on the fabric ($W_{fixed}$) using spectrophotometric analysis of the wash-off liquor.</li>
<li>Calculate the Fixation Percentage and the Fixation Ratio to assess how much of the exhausted dye was actually bonded.</li>
</ol>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 5. CALCULATORS

# --- SECTION II: DYE FIXATION ---
st.subheader("2. Dye Fixation Calculation (%F)")
st.latex(r"\%F = \left( \frac{W_{fixed}}{W_{total}} \right) \times 100")

t_fix = st.radio(
    "Solve for (Fixation):", 
    ["Fixation Percentage (%F) [%]", "Weight of Fixed Dye (Wf) [g]", "Total Dye Taken (Wt) [g]"], 
    horizontal=True, key="r_fix"
)
c1_in, c1_res = st.columns([3, 1])
res_fix = 0.0
with c1_in:
    if "Percentage" in t_fix:
        wf = st.number_input("Weight of Fixed Dye (Wf) [g]", value=0.0, key="wf_1")
        wt = st.number_input("Total Dye Taken (Wt) [g]", value=0.0, key="wt_1")
        if wt > 0: res_fix = (wf / wt) * 100
    elif "Fixed Dye" in t_fix:
        pf = st.number_input("Fixation Percentage (%F) [%]", value=0.0, key="pf_2")
        wt = st.number_input("Total Dye Taken (Wt) [g]", value=0.0, key="wt_2")
        res_fix = (pf / 100) * wt
    else:
        pf = st.number_input("Fixation Percentage (%F) [%]", value=0.0, key="pf_3")
        wf = st.number_input("Weight of Fixed Dye (Wf) [g]", value=0.0, key="wf_3")
        if pf > 0: res_fix = (wf / pf) * 100

with c1_res:
    if res_fix > 0:
        u = " %" if "Percentage" in t_fix else " g"
        st.metric(f"Result: {t_fix.split(' (')[0]}", f"{res_fix:.2f}{u}")

st.markdown("---")

# --- SECTION III: PROCESS EFFICIENCY ---
st.subheader("3. Process Efficiency & Exhaustion (%E)")
st.latex(r"\%E = \left( \frac{W_{exh}}{W_{total}} \right) \times 100")

t_eff = st.radio(
    "Solve for (Efficiency):", 
    ["Exhaustion Percentage (%E) [%]", "Weight of Dye Exhausted (We) [g]"], 
    horizontal=True, key="r_eff"
)
c2_in, c2_res = st.columns([3, 1])
res_eff = 0.0
with c2_in:
    if "Percentage" in t_eff:
        we = st.number_input("Weight of Dye Exhausted (We) [g]", value=0.0, key="we_1")
        wt_e = st.number_input("Total Dye Taken (Wt) [g]", value=0.0, key="wt_e1")
        if wt_e > 0: res_eff = (we / wt_e) * 100
    else:
        pe = st.number_input("Exhaustion Percentage (%E) [%]", value=0.0, key="pe_2")
        wt_e = st.number_input("Total Dye Taken (Wt) [g]", value=0.0, key="wt_e2")
        res_eff = (pe / 100) * wt_e

with c2_res:
    if res_eff > 0:
        u = " %" if "Percentage" in t_eff else " g"
        st.metric(f"Result: {t_eff.split(' (')[0]}", f"{res_eff:.2f}{u}")

# 6. REFERENCE DATA
st.markdown("---")
with st.expander("📖 View Typical Fixation Ranges by Dye Class"):
    data = {
        "Dye Class": ["Reactive (M/H)", "Reactive (VS/Hot)", "Direct Dyes", "Vat Dyes", "Disperse Dyes"],
        "Typical Fixation (%)": ["60 - 80%", "80 - 95%", "70 - 90%", "85 - 95%", "90 - 98%"],
        "Substrate": ["Cotton", "Cotton/Viscose", "Cellulosics", "Cellulosics", "Polyester"]
    }
    df = pd.DataFrame(data)
    df.index = range(1, len(df) + 1)
    st.table(df)

# 7. JUSTIFICATION FOOTER
st.info("""
**Parameters & Justification:**
* **%F (Fixation Percentage):** The absolute yield of dye chemically bonded to the fiber relative to the total dye starting amount.
* **%E (Exhaustion Percentage):** The proportion of dye that moved from the liquor to the fiber, including both bonded and unbonded dye.
* **Wf (Fixed Dye):** The dye mass remaining after standardized soaping/washing.
* **We (Exhausted Dye):** The dye mass removed from the bath during the dyeing cycle.
* **Fixation Ratio:** A secondary metric (calculated as $W_f / W_e$) that describes how much of the "exhausted" dye actually became permanently fixed.
* **Environmental Impact:** Low fixation leads to high concentrations of unfixed dye in wash-off water, requiring extensive effluent treatment.
""")