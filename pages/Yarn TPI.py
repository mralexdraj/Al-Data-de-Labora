import streamlit as st
import math
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Yarn Twist Lab", layout="wide", initial_sidebar_state="collapsed")

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

st.title("Yarn Twist Lab 🧵")
st.markdown("### **What is Yarn Twist?**")
st.markdown("""
<div style="text-align: justify;">
Yarn twist is the spiral arrangement of fibers around the axis of the yarn, produced by rotating one end of the fiber strand while the other is held stationary. Twist is essential for providing coherence and strength to the yarn; without it, fibers would simply slide past each other under tension. The amount of twist affects the yarn's diameter, strength, handle, and appearance, and is typically measured in Turns Per Inch (TPI) or Turns Per Meter (TPM).
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 3. METHODOLOGY
st.subheader("1. Instrumental TPI Determination")
st.markdown("""
**Procedure (Untwist-Retwist Method):**
1. Secure the yarn sample between the fixed and the rotating clamps.
2. Adjust the tension and set the dial to zero. The indicator light will glow, confirming the yarn is at the correct starting position.
3. Start rotating the lever. The light will go off as the yarn untwists. Continue rotating until the yarn becomes parallel and then begins to retwist.
4. Stop rotating the moment the indicator light comes back on.
5. Record the final reading on the dial to determine the TPI.
""")

st.markdown("---")

# 4. CALCULATORS

# --- A. TWIST & MULTIPLIER (INDIRECT SYSTEM) ---
st.subheader("2. Twist Multiplier Analysis (Indirect System)")
st.latex(r"TPI = TM \times \sqrt{Ne}")

col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    target_t = st.radio("Solve for:", ["TPI", "Twist Multiplier (TM)", "Yarn Count (Ne)"], horizontal=True, key="sel_t")
    res_t, tm_g, ne_g, tpi_g = 0.0, 0.0, 0.0, 0.0
    if target_t == "TPI":
        tm_g = st.number_input("Twist Multiplier (TM)", value=0.0, key="tm1")
        ne_g = st.number_input("Yarn Count (Ne)", value=0.0, key="ne1")
        res_t = tm_g * math.sqrt(ne_g)
    elif target_t == "Twist Multiplier (TM)":
        tpi_g = st.number_input("Turns Per Inch (TPI)", value=0.0, key="tpi2")
        ne_g = st.number_input("Yarn Count (Ne)", value=0.0, key="ne2")
        res_t = tpi_g / math.sqrt(ne_g) if ne_g > 0 else 0.0
    else: # Ne
        tpi_g = st.number_input("Turns Per Inch (TPI)", value=0.0, key="tpi3")
        tm_g = st.number_input("Twist Multiplier (TM)", value=0.0, key="tm3")
        res_t = (tpi_g / tm_g)**2 if tm_g > 0 else 0.0
with col_t2:
    if (tm_g > 0 or ne_g > 0 or tpi_g > 0):
        u = " TPI" if target_t == "TPI" else (" Ne" if target_t == "Yarn Count (Ne)" else "")
        st.metric(f"Result: {target_t}", f"{res_t:.2f}{u}")

st.info("**Application:** Standard in the Indian cotton market. As yarn count gets finer ($Ne$ increases), the yarn requires more TPI to maintain its structural integrity.")

st.markdown("---")

# --- B. TWIST FACTOR (DIRECT SYSTEM) ---
st.subheader("3. Twist Factor Analysis (Direct System)")
st.latex(r"\alpha_{tex} = \frac{TPM \times \sqrt{Tex}}{100}")

col_tf1, col_tf2 = st.columns([3, 1])
with col_tf1:
    target_tf = st.radio("Solve for:", ["Twist Factor (α-tex)", "TPM", "Tex Value"], horizontal=True, key="sel_tf")
    res_tf, tpm_g, tex_g, at_g = 0.0, 0.0, 0.0, 0.0
    if target_tf == "Twist Factor (α-tex)":
        tpm_g = st.number_input("Turns Per Meter (TPM)", value=0.0, key="tpm1")
        tex_g = st.number_input("Yarn Count (Tex)", value=0.0, key="tex1")
        res_tf = (tpm_g * math.sqrt(tex_g)) / 100
    elif target_tf == "TPM":
        at_g = st.number_input("Twist Factor (α-tex)", value=0.0, key="at2")
        tex_g = st.number_input("Yarn Count (Tex)", value=0.0, key="tex2")
        res_tf = (at_g * 100) / math.sqrt(tex_g) if tex_g > 0 else 0.0
    else: # Tex
        tpm_g = st.number_input("Turns Per Meter (TPM)", value=0.0, key="tpm3")
        at_g = st.number_input("Twist Factor (α-tex)", value=0.0, key="at3")
        res_tf = ((at_g * 100) / tpm_g)**2 if tpm_g > 0 else 0.0
with col_tf2:
    if (tpm_g > 0 or tex_g > 0 or at_g > 0):
        u = " TPM" if target_tf == "TPM" else (" Tex" if target_tf == "Tex Value" else "")
        st.metric(f"Result: {target_tf}", f"{res_tf:.2f}{u}")

st.info("**Application:** Global synthetic and filament markets use $\\alpha_{tex}$. Unlike indirect systems, as the yarn gets thicker (higher Tex), it requires fewer turns to achieve the same strength.")

st.markdown("---")

# --- C. TWIST CONTRACTION ---
st.subheader("4. Twist Contraction (C%)")
st.latex(r"C\% = \left( \frac{L_u - L_t}{L_u} \right) \times 100")

col_tc1, col_tc2 = st.columns([3, 1])
with col_tc1:
    target_tc = st.radio("Solve for:", ["Contraction %", "Untwisted Length (Lu)", "Twisted Length (Lt)"], horizontal=True, key="sel_tc")
    res_tc, lu_g, lt_g, c_g = 0.0, 0.0, 0.0, 0.0
    if target_tc == "Contraction %":
        lu_g = st.number_input("Untwisted Length (Lu)", value=0.0, key="lu1")
        lt_g = st.number_input("Twisted Length (Lt)", value=0.0, key="lt1")
        res_tc = ((lu_g - lt_g) / lu_g) * 100 if lu_g > 0 else 0.0
    elif target_tc == "Untwisted Length (Lu)":
        c_g = st.number_input("Contraction %", value=0.0, key="c2")
        lt_g = st.number_input("Twisted Length (Lt)", value=0.0, key="lt2")
        res_tc = lt_g / (1 - (c_g / 100)) if c_g < 100 else 0.0
    else: # Lt
        lu_g = st.number_input("Untwisted Length (Lu)", value=0.0, key="lu3")
        c_g = st.number_input("Contraction %", value=0.0, key="c3")
        res_tc = lu_g * (1 - (c_g / 100))
with col_tc2:
    if (lu_g > 0 or lt_g > 0 or c_g > 0):
        u = "%" if "Contraction" in target_tc else " mm/in"
        st.metric(f"Result: {target_tc}", f"{res_tc:.2f}{u}")

st.info("**Application:** Twisting fibers physically shortens the yarn length. This calculation is vital for production yield and accurate cost estimation.")

st.markdown("---")

# --- D. TWIST ANGLE ---
st.subheader("5. Twist Angle (Helix Angle)")
st.latex(r"\tan \theta = \pi \times D \times \text{Twist}")

col_ta1, col_ta2 = st.columns([3, 1])
with col_ta1:
    target_ta = st.radio("Solve for:", ["Angle (θ)", "Yarn Diameter (D)", "Twist"], horizontal=True, key="sel_ta")
    res_ta, d_g, tw_g, an_g = 0.0, 0.0, 0.0, 0.0
    if target_ta == "Angle (θ)":
        d_g = st.number_input("Yarn Diameter (D)", value=0.0, key="d1")
        tw_g = st.number_input("Twist per unit length", value=0.0, key="tw1")
        res_ta = math.degrees(math.atan(math.pi * d_g * tw_g))
    elif target_ta == "Yarn Diameter (D)":
        an_g = st.number_input("Helix Angle (θ) [degrees]", value=0.0, key="an2")
        tw_g = st.number_input("Twist per unit length", value=0.0, key="tw2")
        res_ta = math.tan(math.radians(an_g)) / (math.pi * tw_g) if tw_g > 0 else 0.0
    else: # Twist
        an_g = st.number_input("Helix Angle (θ) [degrees]", value=0.0, key="an3")
        d_g = st.number_input("Yarn Diameter (D)", value=0.0, key="d3")
        res_ta = math.tan(math.radians(an_g)) / (math.pi * d_g) if d_g > 0 else 0.0
with col_ta2:
    if (d_g > 0 or tw_g > 0 or an_g > 0):
        u = "°" if target_ta == "Angle (θ)" else ""
        st.metric(f"Result: {target_ta}", f"{res_ta:.2f}{u}")

st.info("**Application:** The 'Science' of fabric feel. It measures the slope of the fiber helix relative to the yarn axis, determining if a yarn feels soft or hard regardless of its count.")

# 6. JUSTIFICATION FOOTER
st.markdown("---")
st.info("""
**Parameters & Definitions:**
* **TPI / TPM:** Turns per inch or per meter; the amount of twist inserted into the yarn.
* **Twist Multiplier (TM):** A factor that defines the "twistiness" independent of yarn count.
* **Twist Factor (α):** The equivalent of TM used in the direct system (Tex/Metric).
* **Contraction (C%):** The reduction in yarn length caused by the spiraling of fibers during twisting.
* **Helix Angle (θ):** The angle at which fibers lie relative to the yarn axis; determines the yarn's handle and softness.
""")