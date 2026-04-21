import joblib
import numpy as np
import streamlit as st

st.set_page_config(
    page_title="TAST Calculator",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
:root {
    --bg: #f6f8fc;
    --card: #ffffff;
    --text: #122033;
    --muted: #667085;
    --accent: #138a7e;
    --accent-dark: #0f766e;
    --border: #e3e8f0;
}

.stApp {
    background: linear-gradient(180deg, #f8fbff 0%, #eef3f9 100%);
    color: var(--text);
}

.block-container {
    max-width: 980px;
    padding-top: 0rem !important;
    padding-bottom: 2rem;
}

header[data-testid="stHeader"] { height: 0 !important; }
footer { visibility: hidden; }

.title-row {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 0.4rem;
}

.app-title {
    font-size: 3rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.05;
    margin: 0;
}

.score-guide {
    background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
    border: 1px solid #dbe4ee;
    border-radius: 24px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 6px 18px rgba(16,24,40,0.04);
}

.score-guide-title {
    font-size: 1rem;
    font-weight: 800;
    color: #102134;
    margin-bottom: 0.65rem;
}

.score-guide-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
}

.score-guide-card {
    background: #fbfdff;
    border: 1px solid #e3e8f0;
    border-radius: 16px;
    padding: 0.85rem 0.9rem;
}

.score-guide-threshold {
    font-size: 0.98rem;
    font-weight: 800;
    color: #0f766e;
    margin-bottom: 0.22rem;
}

.score-guide-label {
    font-size: 0.92rem;
    color: #667085;
    line-height: 1.4;
}

.input-card {
    background: rgba(255,255,255,0.72);
    border: 1px solid #dbe4ee;
    border-radius: 20px;
    padding: 1.2rem;
    height: 100%;
    box-shadow: 0 6px 18px rgba(16,24,40,0.04);
    backdrop-filter: blur(4px);
}

.input-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #102134;
    margin-bottom: 0.15rem;
}

.input-subtitle {
    font-size: 0.92rem;
    color: #667085;
    margin-bottom: 0.8rem;
}

div[data-testid="stTextInput"] input {
    background: #ffffff !important;
    color: #122033 !important;
    border: 1px solid #d7dee8 !important;
    border-radius: 14px !important;
    padding: 0.78rem 0.95rem !important;
    font-size: 1.05rem !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #138a7e 0%, #0f766e 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    padding: 0.85rem 1rem !important;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(2) button,
div[data-testid="stHorizontalBlock"] > div:nth-child(3) button {
    width: 38px !important;
    min-width: 38px !important;
    height: 38px !important;
    margin-top: 30px !important;
    border-radius: 12px !important;
    padding: 0 !important;
    font-size: 1.2rem !important;
    line-height: 1 !important;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
    margin-right: 6px !important;
}
</style>
""", unsafe_allow_html=True)

MODEL_PATH = "model.pkl"

@st.cache_resource
def load_model():
    bundle = joblib.load(MODEL_PATH)
    return bundle["rf"], bundle["bag"], bundle["svr"], bundle["gbr"], bundle["calibrator"]

rf, bag, svr, gbr, calibrator = load_model()

def parse_value(s: str, name: str) -> float:
    try:
        v = float(str(s).strip())
    except Exception:
        st.error(f"Please enter a valid numeric value for {name}.")
        st.stop()
    if v < 0:
        st.error(f"{name} must be non-negative.")
        st.stop()
    return v

if "ast_text" not in st.session_state:
    st.session_state.ast_text = "23.00"
if "tsi_text" not in st.session_state:
    st.session_state.tsi_text = "82.00"

def adjust_value(key: str, delta: float):
    try:
        current = float(str(st.session_state[key]).strip())
    except Exception:
        current = 0.0
    current = max(0.0, current + delta)
    st.session_state[key] = f"{current:.2f}"

st.markdown("""
<div class="score-guide">
    <div class="score-guide-title">Clinical interpretation guide</div>
    <div class="score-guide-grid">
        <div class="score-guide-card">
            <div class="score-guide-threshold">TAST ≤ 0.35</div>
            <div class="score-guide-label">Likely non-MASH</div>
        </div>
        <div class="score-guide-card">
            <div class="score-guide-threshold">0.35 &lt; TAST &lt; 0.67</div>
            <div class="score-guide-label">Intermediate zone</div>
        </div>
        <div class="score-guide-card">
            <div class="score-guide-threshold">TAST ≥ 0.67</div>
            <div class="score-guide-label">Likely MASH</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-row">
    <div style="font-size:2.4rem;">🩺</div>
    <div class="app-title">TAST Calculator</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="input-card">
        <div class="input-title">AST Input</div>
        <div class="input-subtitle">You can type a value directly or use the buttons to adjust it.</div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([8.8, 0.8, 0.8], gap="small")
    with c1:
        st.text_input("AST value", key="ast_text")
    with c2:
        st.button("−", key="ast_minus", on_click=adjust_value, args=("ast_text", -1.0))
    with c3:
        st.button("+", key="ast_plus", on_click=adjust_value, args=("ast_text", 1.0))

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="input-card">
        <div class="input-title">TSI Input</div>
        <div class="input-subtitle">You can type a value directly or use the buttons to adjust it.</div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([8.8, 0.8, 0.8], gap="small")
    with c1:
        st.text_input("TSI score", key="tsi_text")
    with c2:
        st.button("−", key="tsi_minus", on_click=adjust_value, args=("tsi_text", -1.0))
    with c3:
        st.button("+", key="tsi_plus", on_click=adjust_value, args=("tsi_text", 1.0))

    st.markdown("</div>", unsafe_allow_html=True)

if st.button("Calculate TAST"):
    ast_value = parse_value(st.session_state.ast_text, "AST")
    tsi_value = parse_value(st.session_state.tsi_text, "TSI score")

    X_new = np.array([[ast_value, tsi_value]], dtype=float)

    pred_rf = float(rf.predict(X_new)[0])
    pred_bag = float(bag.predict(X_new)[0])
    pred_svr = float(svr.predict(X_new)[0])
    pred_gbr = float(gbr.predict(X_new)[0])

    mean_pred = np.mean([pred_rf, pred_bag, pred_svr, pred_gbr])
    tast_value = float(calibrator.predict(np.array([[mean_pred]], dtype=float))[0])

    if tast_value <= 0.35:
        band_label = "Likely non-MASH"
        band_color = "#0f766e"
        band_bg = "#ecfdf5"
        band_border = "#a7f3d0"
    elif tast_value >= 0.67:
        band_label = "Likely MASH"
        band_color = "#b42318"
        band_bg = "#fef2f2"
        band_border = "#fecaca"
    else:
        band_label = "Intermediate zone"
        band_color = "#a16207"
        band_bg = "#fffbeb"
        band_border = "#fde68a"

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f3fbf8 0%, #ffffff 100%);
                border: 1px solid #cfeee7; border-radius: 22px;
                padding: 1.6rem 1.2rem; text-align: center; margin-top: 1rem;">
        <div style="font-size: 0.92rem; letter-spacing: 0.08em; text-transform: uppercase; color: #667085; font-weight: 600;">
            Prediction Result
        </div>
        <div style="font-size: 1.25rem; font-weight: 700; color: #102134; margin-top: 0.3rem;">
            TAST score
        </div>
        <div style="font-size: 3.6rem; font-weight: 800; color: #0f766e; line-height: 1; margin-top: 0.5rem;">
            {tast_value:.2f}
        </div>
        <div style="display: inline-block; margin-top: 0.9rem; padding: 0.35rem 0.95rem;
                    background: {band_bg}; border: 1px solid {band_border};
                    color: {band_color}; font-weight: 700; font-size: 0.95rem;
                    border-radius: 999px;">
            {band_label}
        </div>
        <div style="color: #667085; font-size: 0.95rem; margin-top: 0.7rem;">
            Computed automatically from AST and TSI score
        </div>
    </div>
    """, unsafe_allow_html=True)
