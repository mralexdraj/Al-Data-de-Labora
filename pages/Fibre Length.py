import streamlit as st
import pandas as pd
import math
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Fiber Length Lab", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Fiber Length Lab (Comb Sorter) 📏")
st.markdown("### **What is Fiber Length Analysis?**")
st.write("""
Fiber length is a primary determinant of spinning performance and yarn quality. Using a Baer Comb Sorter, 
fibers are separated by length to create a 'Fibrogram.' This geometric representation allows us to calculate 
critical industrial parameters like Effective Length, Mean Length, and Dispersion.
""")

st.markdown("---")

# 3. PREPARATION & DIAGRAM
st.subheader("1. Fiber Sample Preparation")
st.markdown("""
**Procedure:**
1. Collect a representative fiber sample and use the **Comb Sorter** apparatus to parallelize and align them at one end.
2. Carefully transfer fibers from the combs onto a black velvet board, starting from the longest to the shortest.
3. This creates a **Fibrogram** (a curve representing the cumulative length distribution).
4. Trace the outline of this fibrogram onto paper for geometric construction.
""")

# --- IMAGE LOADING LOGIC (Preserved) ---
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "cleaned_fiber_diagram.png")

c_left, c_center, c_right = st.columns([1, 4, 1])
with c_center:
    if os.path.exists(image_path):
        st.image(image_path, caption="Fig: Fiber Diagram Analysis (Geometric Construction)", use_container_width=True)
    else:
        st.error(f"⚠️ Image not found. Move 'cleaned_fiber_diagram.png' into: {script_dir}")

# 4. GEOMETRIC CONSTRUCTION
st.subheader("Geometric Construction Steps")
st.markdown("""
1. **Maximum Length ($OA$):** Vertical axis represents the longest fibers. **Base ($OB$):** Horizontal axis represents total fiber count.
2. **Find $P'$ and $P$:** Halve $OA$ at point **$Q$**. Draw a horizontal line to cut the curve at **$P'$**. Drop a perpendicular to **$P$**.
3. **Find $K'$ and $K$:** Mark off $OK = 1/4 \ OP$. Erect a perpendicular to **$K'$**.
4. **Find $R'$ and $R$:** Halve the vertical line $KK'$ at point **$S$**. Draw a horizontal line to cut the curve at **$R'$**. Drop a perpendicular to **$R$**.
5. **Find Effective Length ($LL'$):** Mark off $OL = 1/4 \ OR$. Erect a perpendicular to **$L'$**.
6. **Find Lower Quartile ($MM'$):** Mark off $OM = 3/4 \ OR$. Erect a perpendicular to **$M'$**.
""")

st.markdown("---")

# 5. PARAMETER MAPPING (Non-calculator section)
st.subheader("3. Geometric Parameter Mapping")
st.write("Based on the geometric construction, the following specific fiber length parameters are identified:")

data_map = {
    "Parameter": [
        "Maximum Length", 
        "Effective Length", 
        "Upper Quartile Length (UQL)", 
        "Lower Quartile Length (LQL)", 
        "Quartile Range"
    ],
    "Diagram Reference": [
        "OA", 
        "LL'", 
        "KK'", 
        "MM'", 
        "KK' - MM'"
    ]
}

df_map = pd.DataFrame(data_map)
df_map.index = range(1, len(df_map) + 1)
st.table(df_map)

st.markdown("---")

# 6. CALCULATORS (One below another)
st.subheader("4. Analytical Calculations")

# --- A. DISPERSION ---
st.markdown("#### A. Dispersion %")
st.latex(r"Dispersion \% = \frac{NL'}{LL'} \times 100")
col_disp1, col_disp2 = st.columns([3, 1])
with col_disp1:
    target_disp = st.radio("Solve for (Dispersion):", ["Dispersion %", "NL'", "LL' (Effective Length)"], horizontal=True, key="sd1")
    res_disp = 0.0
    if target_disp == "Dispersion %":
        nl = st.number_input("NL' [mm]", value=0.0, key="nl_1")
        ll = st.number_input("LL' (Effective Length) [mm]", value=0.0, key="ll_1")
        res_disp = (nl / ll) * 100 if ll > 0 else 0.0
    elif target_disp == "NL'":
        disp = st.number_input("Dispersion %", value=0.0, key="disp_2")
        ll = st.number_input("LL' (Effective Length) [mm]", value=0.0, key="ll_2")
        res_disp = (disp * ll) / 100
    else:
        nl = st.number_input("NL' [mm]", value=0.0, key="nl_3")
        disp = st.number_input("Dispersion %", value=0.0, key="disp_3")
        res_disp = (nl * 100) / disp if disp > 0 else 0.0
with col_disp2:
    if res_disp > 0:
        u = "%" if "Dispersion" in target_disp else " mm"
        st.metric(f"Result: {target_disp}", f"{res_disp:.2f}{u}")

# --- B. SHORT FIBERS ---
st.markdown("#### B. Percent Short Fibers")
st.latex(r"Short \ Fibers \% = \frac{RB}{OB} \times 100")
col_sf1, col_sf2 = st.columns([3, 1])
with col_sf1:
    target_sf = st.radio("Solve for (Short Fibers):", ["Short Fibers %", "RB (Short Length)", "OB (Total Base)"], horizontal=True, key="sd2")
    res_sf = 0.0
    if target_sf == "Short Fibers %":
        rb = st.number_input("RB (Short Length) [mm]", value=0.0, key="rb_1")
        ob = st.number_input("OB (Base Length) [mm]", value=0.0, key="ob_1")
        res_sf = (rb / ob) * 100 if ob > 0 else 0.0
    elif target_sf == "RB (Short Length)":
        perc = st.number_input("Short Fibers %", value=0.0, key="sf_2")
        ob = st.number_input("OB (Base Length) [mm]", value=0.0, key="ob_2")
        res_sf = (perc * ob) / 100
    else:
        rb = st.number_input("RB (Short Length) [mm]", value=0.0, key="rb_3")
        perc = st.number_input("Short Fibers %", value=0.0, key="sf_3")
        res_sf = (rb * 100) / perc if perc > 0 else 0.0
with col_sf2:
    if res_sf > 0:
        u = "%" if "Short Fibers %" in target_sf else " mm"
        st.metric(f"Result: {target_sf}", f"{res_sf:.2f}{u}")

# --- C. MEAN LENGTH ---
st.markdown("#### C. Mean Length")
st.latex(r"Mean \ Length = \frac{Area}{Base \ Length (OB)}")
col_ml1, col_ml2 = st.columns([3, 1])
with col_ml1:
    target_ml = st.radio("Solve for (Mean Length):", ["Mean Length", "Area under curve", "Base Length (OB)"], horizontal=True, key="sd3")
    res_ml = 0.0
    if target_ml == "Mean Length":
        area = st.number_input("Area [sq mm]", value=0.0, key="area_1")
        ob = st.number_input("OB (Base Length) [mm]", value=0.0, key="ob_ml1")
        res_ml = area / ob if ob > 0 else 0.0
    elif target_ml == "Area under curve":
        ml = st.number_input("Mean Length [mm]", value=0.0, key="ml_2")
        ob = st.number_input("OB (Base Length) [mm]", value=0.0, key="ob_ml2")
        res_ml = ml * ob
    else:
        area = st.number_input("Area [sq mm]", value=0.0, key="area_3")
        ml = st.number_input("Mean Length [mm]", value=0.0, key="ml_3")
        res_ml = area / ml if ml > 0 else 0.0
with col_ml2:
    if res_ml > 0:
        u = " sq mm" if "Area" in target_ml else " mm"
        st.metric(f"Result: {target_ml}", f"{res_ml:.2f}{u}")

# 7. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **Effective Length ($LL'$):** A standard measure representing the length of the bulk of longer fibers.
* **Mean Length:** The average length of all fibers in the sample.
* **Dispersion %:** A measure of the variability or non-uniformity of fiber lengths.
* **Short Fiber Content:** Fibers shorter than a specific threshold (e.g., half the effective length), critical for spinning waste.
* **NL':** The length from point $N$ to $L'$ on the construction.
""")