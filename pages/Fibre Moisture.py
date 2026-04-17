import streamlit as st
import pandas as pd
import math

# 1. PAGE SETUP
st.set_page_config(page_title="Fiber Moisture Lab", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Fiber Moisture Lab 💧")
st.markdown("### **What is Moisture Content and Regain?**")
st.write("""
Moisture plays a critical role in fiber weight, processing, and commercial trading. 
Since fibers are hygroscopic, they absorb or release moisture based on the relative humidity of the environment. 
Standardizing weight through moisture calculations is essential for fair trade and consistent manufacturing.
""")

st.markdown("---")

# --- METHOD 1: MOISTURE CONTENT ---
st.subheader("1. Moisture Content (MC)")
st.latex(r"MC \% = \frac{W - D}{W} \times 100")

col_mc1, col_mc2 = st.columns([3, 1])
with col_mc1:
    target_mc = st.radio("Solve for (MC):", ["Moisture Content (MC %)", "Original Weight (W)", "Oven Dry Weight (D)"], horizontal=True, key="solve_mc")
    res_mc = 0.0
    if target_mc == "Moisture Content (MC %)":
        w_mc = st.number_input("Original (Wet) Weight (W) [g]", value=0.0, key="w_mc_in")
        d_mc = st.number_input("Oven Dry Weight (D) [g]", value=0.0, key="d_mc_in")
        res_mc = ((w_mc - d_mc) / w_mc) * 100 if w_mc > 0 else 0.0
    elif target_mc == "Original Weight (W)":
        mc_in = st.number_input("Known MC %", value=0.0, key="mc_val_in")
        d_mc = st.number_input("Oven Dry Weight (D) [g]", value=0.0, key="d_mc_val")
        res_mc = d_mc / (1 - (mc_in / 100)) if mc_in < 100 else 0.0
    else: # Oven Dry Weight (D)
        w_mc = st.number_input("Original (Wet) Weight (W) [g]", value=0.0, key="w_mc_val")
        mc_in = st.number_input("Known MC %", value=0.0, key="mc_val_d")
        res_mc = w_mc * (1 - (mc_in / 100))

with col_mc2:
    if res_mc != 0:
        unit = " g" if "Weight" in target_mc else "%"
        st.metric(f"Result: {target_mc}", f"{res_mc:.2f}{unit}")

st.markdown("---")

# --- METHOD 2: MOISTURE REGAIN ---
st.subheader("2. Moisture Regain (MR)")
st.latex(r"MR \% = \frac{W - D}{D} \times 100")

col_mr1, col_mr2 = st.columns([3, 1])
with col_mr1:
    target_mr = st.radio("Solve for (MR):", ["Moisture Regain (MR %)", "Original Weight (W)", "Oven Dry Weight (D)"], horizontal=True, key="solve_mr")
    res_mr = 0.0
    if target_mr == "Moisture Regain (MR %)":
        w_mr = st.number_input("Original (Wet) Weight (W) [g]", value=0.0, key="w_mr_in")
        d_mr = st.number_input("Oven Dry Weight (D) [g]", value=0.0, key="d_mr_in")
        res_mr = ((w_mr - d_mr) / d_mr) * 100 if d_mr > 0 else 0.0
    elif target_mr == "Original Weight (W)":
        mr_in = st.number_input("Known MR %", value=0.0, key="mr_val_in")
        d_mr = st.number_input("Oven Dry Weight (D) [g]", value=0.0, key="d_mr_val")
        res_mr = d_mr * (1 + (mr_in / 100))
    else: # Oven Dry Weight (D)
        w_mr = st.number_input("Original (Wet) Weight (W) [g]", value=0.0, key="w_mr_val")
        mr_in = st.number_input("Known MR %", value=0.0, key="mr_val_d")
        res_mr = w_mr / (1 + (mr_in / 100)) if mr_in > -100 else 0.0

with col_mr2:
    if res_mr != 0:
        unit = " g" if "Weight" in target_mr else "%"
        st.metric(f"Result: {target_mr}", f"{res_mr:.2f}{unit}")

st.markdown("---")

# --- METHOD 3: CONVERSION ---
st.subheader("3. Conversion between MC and MR")
col_conv1, col_conv2 = st.columns([3, 1])
with col_conv1:
    conv_mode = st.radio("Direction:", ["Regain (MR) → Content (MC)", "Content (MC) → Regain (MR)"], horizontal=True)
    if conv_mode == "Regain (MR) → Content (MC)":
        st.latex(r"MC = \frac{MR}{100 + MR} \times 100")
        val_in = st.number_input("Known Moisture Regain (MR %)", value=0.0, key="mr_to_mc")
        res_conv = (val_in / (100 + val_in)) * 100 if (100 + val_in) != 0 else 0.0
    else:
        st.latex(r"MR = \frac{MC}{100 - MC} \times 100")
        val_in = st.number_input("Known Moisture Content (MC %)", value=0.0, key="mc_to_mr")
        res_conv = (val_in / (100 - val_in)) * 100 if (100 - val_in) != 0 else 0.0
with col_conv2:
    if res_conv != 0:
        st.metric("Converted Result", f"{res_conv:.2f}%")

st.markdown("---")

# --- METHOD 4: BLEND REGAIN ---
st.subheader("4. Blend Moisture Regain")
st.latex(r"MR_{blend} = \frac{\sum (P_i \times R_i)}{100}")

col_bl1, col_bl2 = st.columns([3, 1])
with col_bl1:
    # Value must be >= min_value. Defaulting to 1 to satisfy your 1-based indexing logic.
    num_fibers = st.number_input("Number of fiber components in blend", min_value=1, value=1, step=1, key="num_f_blend")
    
    df_blend = pd.DataFrame({
        "Composition (P) %": [0.0] * num_fibers,
        "Standard Regain (R) %": [0.0] * num_fibers
    })
    df_blend.index = range(1, num_fibers + 1)
    
    edited_blend = st.data_editor(df_blend, use_container_width=True, key="blend_editor")
    
    # Calculation logic
    total_pr = (edited_blend.iloc[:,0] * edited_blend.iloc[:,1]).sum()
    res_bl = total_pr / 100

with col_bl2:
    # Only show if a calculation has actually happened (product > 0)
    if total_pr > 0:
        st.metric("Blend MR", f"{res_bl:.2f}%")
        
        total_p = edited_blend.iloc[:,0].sum()
        if total_p != 100 and total_p > 0:
            st.warning(f"Total composition: {total_p}%")

st.markdown("---")

# --- REFERENCE DATA ---
with st.expander("📊 View Standard Moisture Regain Table"):
    data = {
        "Fiber Type": ["Polypropylene", "Polyester", "Acrylic", "Nylon", "Cotton", "Silk", "Viscose Rayon", "Linen", "Wool"],
        "Standard Regain (%)": ["0.04", "0.40", "1.50", "4.50", "8.50", "11.00", "11-13", "12.00", "16-18"]
    }
    df_ref = pd.DataFrame(data)
    df_ref.index = range(1, len(df_ref) + 1)
    st.table(df_ref)

# --- JUSTIFICATION FOOTER ---
st.info("""
**Parameters & Definitions:**
* **W (Original Weight):** The mass of the sample in its natural state.
* **D (Oven Dry Weight):** The mass after removing all moisture at 105°C.
* **MC (Moisture Content):** Moisture as a percentage of wet weight.
* **MR (Moisture Regain):** Moisture as a percentage of bone-dry weight.
* **Pi (Composition %):** The weight percentage of a specific fiber within a blend.
* **Ri (Standard Regain %):** The official standard moisture regain value for that specific fiber type.
        
**Note:** Standard Moisture Regain ($MR$) is the value used in commercial transactions to ensure buyers aren't paying for excess water weight.
""")