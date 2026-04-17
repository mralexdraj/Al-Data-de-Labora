import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Yarn Count Conversion", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Universal Count Converter 🔄")
st.markdown("### **What is Yarn Count Conversion?**")
st.markdown("""
<div style="text-align: justify;">
Yarn count conversion is the process of translating the fineness of a yarn from one numerical system to another. Since different regions and fiber types use specific systems—such as Ne for cotton, Denier for synthetic filaments, and Tex for universal applications—conversions are vital. These conversions rely on established mathematical constants that relate the mass-to-length ratios across direct and indirect systems.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 3. CONVERSION CALCULATORS

# --- SECTION 1: CONVERTING TO TEX ---
st.subheader("1. Convert to Tex")
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    from_tex = st.radio("Convert from:", ["Denier", "English (Ne)", "Metric (Nm)"], horizontal=True, key="c_to_tex")
    val_in, res_tex = 0.0, 0.0
    if from_tex == "Denier":
        st.latex(r"Tex = \frac{Denier}{9}")
        val_in = st.number_input("Enter Denier Value", value=0.0, key="in_d_t")
        res_tex = val_in / 9
    elif from_tex == "English (Ne)":
        st.latex(r"Tex = \frac{590.5}{Ne}")
        val_in = st.number_input("Enter Ne Value", value=0.0, key="in_ne_t")
        res_tex = 590.5 / val_in if val_in > 0 else 0.0
    else: # Nm
        st.latex(r"Tex = \frac{1000}{Nm}")
        val_in = st.number_input("Enter Nm Value", value=0.0, key="in_nm_t")
        res_tex = 1000 / val_in if val_in > 0 else 0.0
with col_t2:
    if val_in > 0:
        st.metric("Resulting Tex", f"{res_tex:.2f} Tex")

st.markdown("---")

# --- SECTION 2: CONVERTING TO DENIER ---
st.subheader("2. Convert to Denier")
col_d1, col_d2 = st.columns([3, 1])
with col_d1:
    from_den = st.radio("Convert from:", ["Tex", "English (Ne)", "Metric (Nm)"], horizontal=True, key="c_to_den")
    val_in_d, res_den = 0.0, 0.0
    if from_den == "Tex":
        st.latex(r"Denier = Tex \times 9")
        val_in_d = st.number_input("Enter Tex Value", value=0.0, key="in_t_d")
        res_den = val_in_d * 9
    elif from_den == "English (Ne)":
        st.latex(r"Denier = \frac{5315}{Ne}")
        val_in_d = st.number_input("Enter Ne Value", value=0.0, key="in_ne_d")
        res_den = 5315 / val_in_d if val_in_d > 0 else 0.0
    else: # Nm
        st.latex(r"Denier = \frac{9000}{Nm}")
        val_in_d = st.number_input("Enter Nm Value", value=0.0, key="in_nm_d")
        res_den = 9000 / val_in_d if val_in_d > 0 else 0.0
with col_d2:
    if val_in_d > 0:
        st.metric("Resulting Denier", f"{res_den:.2f} Denier")

st.markdown("---")

# --- SECTION 3: CONVERTING TO ENGLISH (Ne) ---
st.subheader("3. Convert to English Count (Ne)")
col_ne1, col_ne2 = st.columns([3, 1])
with col_ne1:
    from_ne = st.radio("Convert from:", ["Tex", "Denier", "Metric (Nm)"], horizontal=True, key="c_to_ne")
    val_in_ne, res_ne = 0.0, 0.0
    if from_ne == "Tex":
        st.latex(r"Ne = \frac{590.5}{Tex}")
        val_in_ne = st.number_input("Enter Tex Value", value=0.0, key="in_t_ne")
        res_ne = 590.5 / val_in_ne if val_in_ne > 0 else 0.0
    elif from_ne == "Denier":
        st.latex(r"Ne = \frac{5315}{Denier}")
        val_in_ne = st.number_input("Enter Denier Value", value=0.0, key="in_d_ne")
        res_ne = 5315 / val_in_ne if val_in_ne > 0 else 0.0
    else: # Nm
        st.latex(r"Ne = Nm \times 0.5905")
        val_in_ne = st.number_input("Enter Nm Value", value=0.0, key="in_nm_ne")
        res_ne = val_in_ne * 0.5905
with col_ne2:
    if val_in_ne > 0:
        st.metric("Resulting Ne", f"{res_ne:.2f} Ne")

st.markdown("---")

# --- SECTION 4: CONVERTING TO METRIC (Nm) ---
st.subheader("4. Convert to Metric Count (Nm)")
col_nm1, col_nm2 = st.columns([3, 1])
with col_nm1:
    from_nm = st.radio("Convert from:", ["Tex", "Denier", "English (Ne)"], horizontal=True, key="c_to_nm")
    val_in_nm, res_nm = 0.0, 0.0
    if from_nm == "Tex":
        st.latex(r"Nm = \frac{1000}{Tex}")
        val_in_nm = st.number_input("Enter Tex Value", value=0.0, key="in_t_nm")
        res_nm = 1000 / val_in_nm if val_in_nm > 0 else 0.0
    elif from_nm == "Denier":
        st.latex(r"Nm = \frac{9000}{Denier}")
        val_in_nm = st.number_input("Enter Denier Value", value=0.0, key="in_d_nm")
        res_nm = 9000 / val_in_nm if val_in_nm > 0 else 0.0
    else: # Ne
        st.latex(r"Nm = Ne \times 1.693")
        val_in_nm = st.number_input("Enter Ne Value", value=0.0, key="in_ne_nm")
        res_nm = val_in_nm * 1.693
with col_nm2:
    if val_in_nm > 0:
        st.metric("Resulting Nm", f"{res_nm:.2f} Nm")

# 4. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Conversion Constants:**
* **Tex to Denier:** Factor of 9 ($Denier = Tex \\times 9$).
* **Tex to Ne:** Constant of 590.5 ($Ne = 590.5 / Tex$).
* **Denier to Ne:** Constant of 5315 ($Ne = 5315 / Denier$).
* **Ne to Nm:** Factor of 1.693 ($Nm = Ne \\times 1.693$).
* **Nm to Ne:** Factor of 0.5905 ($Ne = Nm \\times 0.5905$).
        
**Note:** The constants 590.5 and 5315 are specific to cotton counts. For other fibers like Worsted or Linen, these constants change based on their standard hank lengths.
""")