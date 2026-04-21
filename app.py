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
    --bg: #f4f7fb;
    --card: rgba(255,255,255,0.78);
    --text: #102134;
    --muted: #667085;
    --accent: #138a7e;
    --accent-dark: #0f766e;
    --border: #dbe4ee;
    --soft-shadow: 0 10px 28px rgba(16,24,40,0.06);
}

html, body, [class*="css"]  {
    font-family: "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(19,138,126,0.05), transparent 30%),
        linear-gradient(180deg, #f8fbff 0%, #eef3f9 100%);
    color: var(--text);
}

.block-container {
    max-width: 980px;
    padding-top: 2.5rem !important;
    padding-bottom: 2rem;
}

header[data-testid="stHeader"] { height: 0 !important; }
footer { visibility: hidden; }

.title-row {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-top: 0.1rem;
    margin-bottom: 0.35rem;
}

.app-title {
    font-size: 3.2rem;
    font-weight: 850;
    color: #0f172a;
    line-height: 1.02;
    letter-spacing: -0.02em;
    margin: 0;
}

.app-subtitle {
    font-size: 1rem;
    color: #667085;
    margin-bottom: 1rem;
}

.score-guide {
    background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
    border: 1px solid var(--border);
    border-radius: 26px;
    padding: 1.15rem 1.35rem;
    margin-top: 0.1rem;
    margin-bottom: 0.9rem;
    box-shadow: var(--soft-shadow);
}

.score-guide-title {
    font-size: 1.04rem;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 0.72rem;
}

.score-guide-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.85rem;
}

.score-guide-card {
    background: #fbfdff;
    border: 1px solid #e4ebf2;
    border-radius: 18px;
    padding: 0.95rem 1rem;
    min-height: 92px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.score-guide-threshold {
    font-size: 1.02rem;
    font-weight: 800;
    color: var(--accent-dark);
    margin-bottom: 0.25rem;
}

.score-guide-label {
    font-size: 0.95rem;
    color: var(--muted);
    line-height: 1.45;
}

.input-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 1.25rem 1.25rem 1rem 1.25rem;
    min-height: 168px;
    box-shadow: var(--soft-shadow);
    backdrop-filter: blur(6px);
}

.input-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 0.18rem;
}

.input-subtitle {
    font-size: 0.97rem;
    color: var(--muted);
    line-height: 1.55;
    margin-bottom: 0.9rem;
}

div[data-testid="stTextInput"] label p {
    color: var(--text) !important;
    font-weight: 700 !important;
    font-size: 0.98rem !important;
}

div[data-testid="stTextInput"] input {
    background: #ffffff !important;
    color: var(--text) !important;
    border: 1px solid #d7dee8 !important;
    border-radius: 16px !important;
    padding: 0.82rem 1rem !important;
    font-size: 1.08rem !important;
    box-shadow: inset 0 1px 2px rgba(16,24,40,0.04);
}

div[data-testid="stTextInput"] input:focus {
    border: 1px solid #87d7cc !important;
    box-shadow: 0 0 0 3px rgba(19,138,126,0.12) !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #169587 0%, #0f766e 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    font-weight: 800 !important;
    font-size: 1.08rem !important;
    padding: 0.9rem 1rem !important;
    box-shadow: 0 10px 22px rgba(15,118,110,0.18);
}

.stButton > button:hover {
    filter: brightness(0.98);
}

div[data-testid="stHorizontalBlock"] > div:nth-child(2) button,
div[data-testid="stHorizontalBlock"] > div:nth-child(3) button {
    width: 40px !important;
    min-width: 40px !important;
    height: 40px !important;
    margin-top: 30px !important;
    border-radius: 14px !important;
    padding: 0 !important;
    font-size: 1.18rem !important;
    font-weight: 800 !important;
    line-height: 1 !important;
    box-shadow: 0 8px 18px rgba(15,118,110,0.14) !important;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
    margin-right: 6px !important;
}

.result-card {
    background: linear-gradient(135deg, #f3fbf8 0%, #ffffff 100%);
    border: 1px solid #cfeee7;
    border-radius: 24px;
    padding: 1.75rem 1.3rem;
    text-align: center;
    margin-top: 1.15rem;
    box-shadow: var(--soft-shadow);
}

.result-kicker {
    font-size: 0.92rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #667085;
    font-weight: 700;
}

.result-title {
    font-size: 1.28rem;
    font-weight: 800;
    color: var(--text);
    margin-top: 0.35rem;
}

.result-value {
    font-size: 4rem;
    font-weight: 850;
    color: var(--accent-dark);
    line-height: 1;
    margin-top: 0.55rem;
}

.result-caption {
    color: #667085;
    font-size: 0.98rem;
    margin-top: 0.8rem;
}

.small-note {
    font-size: 0.87rem;
    color: #8a6d1b;
    background: #fcf7ea;
    border: 1px solid #eed58f;
    border-radius: 18px;
    padding: 0.9rem 1rem;
    margin-top: 0.2rem;
    margin-bottom: 1rem;
}

@media (max-width: 900px) {
    .app-title { font-size: 2.4rem; }
    .score-guide-grid { grid-template-columns: 1fr; }
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
    <div style="font-size:2.5rem;">🩺</div>
    <div class="app-title">TAST Calculator</div>
</div>
<div class="app-subtitle">Enter AST and TSI score to calculate the predicted TAST value.</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="input-card">
        <div class="input-title">AST Input</div>
        <div class="input-subtitle">Enter the patient's AST value directly or adjust it using the controls.</div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([8.6, 0.85, 0.85], gap="small")
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
        <div class="input-subtitle">Enter the patient's TSI score directly or adjust it using the controls.</div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([8.6, 0.85, 0.85], gap="small")
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
    <div class="result-card">
        <div class="result-kicker">Prediction result</div>
        <div class="result-title">TAST score</div>
        <div class="result-value">{tast_value:.2f}</div>
        <div style="display: inline-block; margin-top: 0.95rem; padding: 0.38rem 1rem;
                    background: {band_bg}; border: 1px solid {band_border};
                    color: {band_color}; font-weight: 800; font-size: 0.97rem;
                    border-radius: 999px;">
            {band_label}
        </div>
        <div class="result-caption">Computed automatically from AST and TSI score.</div>
    </div>
    """, unsafe_allow_html=True)
