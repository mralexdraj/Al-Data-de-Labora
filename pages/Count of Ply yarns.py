import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Plied Yarn Calculator", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Folded & Plied Yarn Calculator 🧶")
st.markdown("### **What is Resultant Count?**")
st.markdown("""
<div style="text-align: justify;">
Resultant count is the final yarn count achieved when two or more individual threads, known as single yarns, are twisted together to form a plied or folded yarn. The mathematical approach to finding this value differs based on the counting system used: in direct systems like Tex or Denier, the counts are additive, whereas in indirect systems like English (Ne) or Metric (Nm), the harmonic mean of the component counts is calculated.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- SECTION 1: DIRECT SYSTEM ---
st.subheader("1. Direct System Calculation (Tex, Denier)")
st.markdown("""
**Procedure:**
1. Determine the number of single yarn components to be plied.
2. Enter the individual count of each component yarn.
3. The resultant count is the simple arithmetic sum of the component counts.
""")
st.latex(r"N_{RD} = N_1 + N_2 + \dots + N_n")

col_d1, col_d2 = st.columns([3, 1])
with col_d1:
    num_d = st.number_input("Number of components (Direct):", min_value=1, value=1, step=1, key="num_d")
    d_counts = []
    for i in range(num_d):
        d_val = st.number_input(f"Count of Single {i+1} [Direct]:", value=0.0, key=f"d_in_{i}")
        d_counts.append(d_val)
    
    res_d = sum(d_counts)

with col_d2:
    # Result Display Guard
    if any(v > 0 for v in d_counts):
        st.metric("Resultant Count (Direct)", f"{res_d:.2f}")

st.markdown("---")

# --- SECTION 2: INDIRECT SYSTEM ---
st.subheader("2. Indirect System Calculation (Ne, Nm)")
st.markdown("""
**Procedure:**
1. Identify the number of threads being folded.
2. Enter the individual count of each thread.
3. Calculate the reciprocal sum to find the final resultant count.
""")
st.latex(r"\frac{1}{N_R} = \frac{1}{N_1} + \frac{1}{N_2} + \dots + \frac{1}{N_n}")

col_i1, col_i2 = st.columns([3, 1])
with col_i1:
    num_i = st.number_input("Number of components (Indirect):", min_value=1, value=1, step=1, key="num_i")
    i_counts = []
    for i in range(num_i):
        i_val = st.number_input(f"Count of Single {i+1} [Indirect]:", value=0.0, key=f"i_in_{i}")
        i_counts.append(i_val)
    
    # Avoid zero division
    recip_sum = sum(1/n for n in i_counts if n > 0)
    res_i = 1 / recip_sum if recip_sum > 0 else 0.0

with col_i2:
    # Result Display Guard
    if any(v > 0 for v in i_counts):
        st.metric("Resultant Count (Indirect)", f"{res_i:.2f}")

# 4. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **Single Yarn:** An individual strand of fibers twisted together.
* **Folding/Plying:** The process of twisting two or more single yarns together.
* **NR (Resultant Count):** The equivalent count of the final plied yarn.
* **Direct System:** Systems where count = weight per unit length (Additive logic).
* **Indirect System:** Systems where count = length per unit weight (Reciprocal logic).
        
**Note:** In the indirect system, plying always results in a coarser (lower) count than the individual component threads.
""")