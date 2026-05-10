import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(
    page_title="SLE Clinical Trial Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --blue-dark:   #0057B8;
    --blue:        #1A7FE8;
    --blue-light:  #EBF4FF;
    --blue-mid:    #C8E0FF;
    --teal:        #00A896;
    --cyan:        #00f5d4;
    --red:         #E53E3E;
    --amber:       #D97706;
    --green:       #059669;
    --neon-green:  #00f5a0;
    --neon-yellow: #ffd60a;
    --neon-red:    #ff3860;
    --gray-400:    #94A3B8;
    --gray-600:    #475569;
    --gray-800:    #1E293B;
    --white:       #FFFFFF;
    --bg:          #0D1117;
    --card:        #161B22;
    --border:      rgba(0,245,212,0.15);
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #c8d8f0 !important;
}

#MainMenu, footer, header, [data-testid="stDecoration"], [data-testid="stToolbar"] {
    display: none !important;
}

.main .block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Nav ── */
.nav-bar {
    background: var(--card);
    border-bottom: 1px solid var(--border);
    padding: 1rem 3rem;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 1px 12px rgba(0,245,212,0.05);
}
.nav-logo { display:flex; align-items:center; gap:0.75rem; }
.nav-logo-icon {
    width:36px; height:36px;
    background: linear-gradient(135deg, var(--blue), var(--cyan));
    border-radius:10px; display:flex; align-items:center;
    justify-content:center; font-size:1.1rem;
}
.nav-logo-text {
    font-family:'DM Serif Display',serif; font-size:1.2rem;
    color:var(--cyan); letter-spacing:-0.02em;
}
.nav-badge {
    background:rgba(0,245,212,0.1); color:var(--cyan);
    font-size:0.7rem; font-weight:600; padding:0.2rem 0.6rem;
    border-radius:20px; letter-spacing:0.05em;
    border:1px solid rgba(0,245,212,0.25);
}
.nav-version {
    font-size:0.75rem; color:rgba(0,245,212,0.35);
    font-family:'IBM Plex Mono',monospace;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0057B8 0%, #1A7FE8 60%, #00f5d4 100%);
    padding: 3.5rem 3rem; color:white; position:relative; overflow:hidden;
}
.hero::before {
    content:''; position:absolute; top:-50%; right:-10%;
    width:500px; height:500px;
    background:radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
    border-radius:50%;
}
.hero-tag {
    display:inline-flex; align-items:center; gap:0.4rem;
    background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.2);
    color:white; font-size:0.72rem; font-weight:500;
    padding:0.3rem 0.8rem; border-radius:20px;
    letter-spacing:0.1em; text-transform:uppercase; margin-bottom:1.25rem;
}
.hero h1 {
    font-family:'DM Serif Display',serif; font-size:2.8rem;
    font-weight:400; line-height:1.15; margin:0 0 1rem; color:white;
}
.hero h1 em { font-style:italic; color:rgba(255,255,255,0.8); }
.hero p { font-size:1rem; color:rgba(255,255,255,0.75); max-width:550px; line-height:1.6; margin:0; }
.hero-stats { display:flex; gap:2.5rem; margin-top:2rem; }
.hero-stat-val { font-family:'DM Serif Display',serif; font-size:1.8rem; color:white; line-height:1; }
.hero-stat-label { font-size:0.72rem; color:rgba(255,255,255,0.6); text-transform:uppercase; letter-spacing:0.08em; margin-top:0.25rem; }

/* ── Content ── */
.content-area { padding:2rem 3rem; max-width:1400px; margin:0 auto; }

/* ── Section titles — NEON ── */
.section-title {
    font-family:'DM Serif Display',serif; font-size:1.4rem;
    color: var(--cyan);
    text-shadow: 0 0 20px rgba(0,245,212,0.4);
    margin:0 0 1.25rem;
    display:flex; align-items:center; gap:0.6rem;
    border-left:3px solid var(--cyan); padding-left:0.75rem;
}

/* ── Cards ── */
.card {
    background: var(--card);
    border:1px solid var(--border);
    border-radius:16px; padding:1.5rem;
    box-shadow:0 0 20px rgba(0,245,212,0.03); margin-bottom:1.5rem;
    transition:box-shadow 0.2s, border-color 0.2s;
}
.card:hover {
    box-shadow:0 0 30px rgba(0,245,212,0.08);
    border-color:rgba(0,245,212,0.3);
}
.card-header {
    font-size:0.78rem; font-weight:600; color:var(--white);
    text-transform:uppercase; letter-spacing:0.1em;
    margin-bottom:1rem; padding:0.6rem 0.75rem;
    border-radius:8px;
    background: linear-gradient(135deg, var(--blue-dark), var(--blue));
}

/* ── Inputs — visible on dark bg ── */
[data-testid="stNumberInput"] input {
    background: #0d1117 !important;
    border:1.5px solid rgba(0,245,212,0.2) !important;
    border-radius:8px !important;
    color: #e0f0ff !important;
    font-family:'DM Sans',sans-serif !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: var(--cyan) !important;
    box-shadow:0 0 0 3px rgba(0,245,212,0.1) !important;
}
[data-testid="stSelectbox"] > div > div {
    background: #0d1117 !important;
    border:1.5px solid rgba(0,245,212,0.2) !important;
    border-radius:8px !important;
    color: #e0f0ff !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: var(--cyan) !important;
    box-shadow:0 2px 8px rgba(0,245,212,0.4) !important;
}

/* ── Labels — visible ── */
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label,
[data-testid="stCheckbox"] label {
    color: #a0c4e8 !important;
    font-size:0.8rem !important;
    font-weight:500 !important;
}
[data-testid="stCheckbox"] label span {
    color: #a0c4e8 !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    width:100% !important;
    background: linear-gradient(135deg, #003d8f, #1A7FE8, #00c4aa) !important;
    border:1px solid rgba(0,245,212,0.3) !important;
    border-radius:12px !important;
    color:white !important;
    font-family:'DM Sans',sans-serif !important;
    font-size:1rem !important; font-weight:600 !important;
    padding:0.9rem 2rem !important;
    box-shadow:0 4px 20px rgba(0,87,184,0.3), 0 0 30px rgba(0,245,212,0.1) !important;
    transition:all 0.2s !important;
    letter-spacing:0.05em !important;
}
[data-testid="stButton"] > button:hover {
    box-shadow:0 8px 30px rgba(0,87,184,0.4), 0 0 50px rgba(0,245,212,0.2) !important;
    transform:translateY(-1px) !important;
}

/* ── Metric cards ── */
.metric-card {
    background: var(--card);
    border-radius:16px; padding:1.5rem;
    box-shadow:0 4px 16px rgba(0,0,0,0.2);
    border-top:4px solid transparent;
    text-align:center; animation:slideUp 0.5s ease-out forwards;
    opacity:0; transform:translateY(16px);
}
@keyframes slideUp { to { opacity:1; transform:translateY(0); } }
.metric-card.blue  { border-top-color:#1A7FE8; box-shadow:0 0 20px rgba(26,127,232,0.1); }
.metric-card.green { border-top-color:#00f5a0; box-shadow:0 0 20px rgba(0,245,160,0.1); }
.metric-card.red   { border-top-color:#ff3860; box-shadow:0 0 20px rgba(255,56,96,0.1); }
.metric-card.amber { border-top-color:#ffd60a; box-shadow:0 0 20px rgba(255,214,10,0.1); }
.metric-card.teal  { border-top-color:#00f5d4; box-shadow:0 0 20px rgba(0,245,212,0.1); }

.metric-tag {
    font-size:0.7rem; font-weight:600; text-transform:uppercase;
    letter-spacing:0.12em; color:rgba(0,245,212,0.5); margin-bottom:0.6rem;
    font-family:'IBM Plex Mono',monospace;
}
.metric-val { font-family:'DM Serif Display',serif; font-size:2.4rem; line-height:1; margin-bottom:0.3rem; }
.metric-sub { font-size:0.72rem; color:rgba(160,196,232,0.5); font-family:'IBM Plex Mono',monospace; }

/* ── Verdict banners ── */
.verdict-banner {
    border-radius:20px; padding:2.5rem 3rem;
    display:flex; align-items:center; gap:2rem;
    animation:slideUp 0.6s ease-out 0.3s forwards; opacity:0;
    margin:1.5rem 0;
}
.verdict-banner.proceed {
    background:linear-gradient(135deg,rgba(0,245,160,0.08),rgba(0,245,160,0.03));
    border:1.5px solid rgba(0,245,160,0.3);
    box-shadow:0 0 40px rgba(0,245,160,0.06);
}
.verdict-banner.monitor {
    background:linear-gradient(135deg,rgba(255,214,10,0.08),rgba(255,214,10,0.03));
    border:1.5px solid rgba(255,214,10,0.3);
    box-shadow:0 0 40px rgba(255,214,10,0.06);
}
.verdict-banner.exclude {
    background:linear-gradient(135deg,rgba(255,56,96,0.08),rgba(255,56,96,0.03));
    border:1.5px solid rgba(255,56,96,0.3);
    box-shadow:0 0 40px rgba(255,56,96,0.06);
}
.verdict-icon-wrap {
    width:72px; height:72px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:2rem; flex-shrink:0;
}
.proceed .verdict-icon-wrap { background:rgba(0,245,160,0.1); }
.monitor .verdict-icon-wrap { background:rgba(255,214,10,0.1); }
.exclude .verdict-icon-wrap { background:rgba(255,56,96,0.1); }

.verdict-label {
    font-size:0.72rem; font-weight:600; text-transform:uppercase;
    letter-spacing:0.15em; margin-bottom:0.3rem;
    font-family:'IBM Plex Mono',monospace;
}
.proceed .verdict-label { color:#00f5a0; }
.monitor .verdict-label { color:#ffd60a; }
.exclude .verdict-label { color:#ff3860; }

.verdict-title-text {
    font-family:'DM Serif Display',serif; font-size:2rem;
    line-height:1.1; margin-bottom:0.5rem;
}
.proceed .verdict-title-text { color:#00f5a0; text-shadow:0 0 20px rgba(0,245,160,0.4); }
.monitor .verdict-title-text { color:#ffd60a; text-shadow:0 0 20px rgba(255,214,10,0.4); }
.exclude .verdict-title-text { color:#ff3860; text-shadow:0 0 20px rgba(255,56,96,0.4); }

.verdict-desc { font-size:0.9rem; color:#a0c4e8; line-height:1.5; }
.verdict-conf { margin-left:auto; text-align:center; flex-shrink:0; }
.conf-val { font-family:'DM Serif Display',serif; font-size:2.5rem; }
.proceed .conf-val { color:#00f5a0; text-shadow:0 0 15px rgba(0,245,160,0.5); }
.monitor .conf-val { color:#ffd60a; text-shadow:0 0 15px rgba(255,214,10,0.5); }
.exclude .conf-val { color:#ff3860; text-shadow:0 0 15px rgba(255,56,96,0.5); }
.conf-label {
    font-size:0.7rem; color:rgba(0,245,212,0.4); text-transform:uppercase;
    letter-spacing:0.1em; font-weight:600; font-family:'IBM Plex Mono',monospace;
}

/* ── Chart cards ── */
.chart-card {
    background: var(--card);
    border:1px solid var(--border);
    border-radius:16px; padding:1.5rem;
    box-shadow:0 0 20px rgba(0,245,212,0.03);
    animation:slideUp 0.5s ease-out forwards; opacity:0;
    margin-bottom:1.5rem;
}
.chart-title {
    font-family:'DM Serif Display',serif; font-size:1.05rem;
    color: #ffffff; margin-bottom:0.2rem;
}
.chart-subtitle {
    font-size:0.7rem; color:rgba(0,245,212,0.4); margin-bottom:0.5rem;
    font-family:'IBM Plex Mono',monospace; text-transform:uppercase; letter-spacing:0.08em;
}

/* ── Divider ── */
.section-divider {
    border:none;
    border-top:1px solid rgba(0,245,212,0.1);
    margin:2rem 0;
}

[data-testid="column"] { padding:0 0.5rem !important; }

::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-thumb { background:rgba(0,245,212,0.2); border-radius:3px; }

/* ── Footer ── */
.app-footer {
    background: var(--card);
    border-top:1px solid var(--border);
    padding:1.5rem 3rem; text-align:center;
    font-size:0.72rem; color:rgba(0,245,212,0.3);
    font-family:'IBM Plex Mono',monospace; letter-spacing:0.05em; margin-top:3rem;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_pipeline():
    return joblib.load('clinical_trial_pipeline_v1.pkl')

bundle = load_pipeline()

class FinalDecisionEngine:
    SE_WEIGHTS  = {'Low': 1.0, 'Medium': 0.6, 'High': 0.2}
    RISK_LABELS = {0: 'Low', 1: 'Medium', 2: 'High'}
    def decide(self, success_prob, eligible, se_risk):
        if not eligible: return 'Exclude', 0.95
        if se_risk == 'High': return 'Exclude', 0.85
        composite = success_prob * self.SE_WEIGHTS[se_risk]
        if composite >= 0.55: return 'Proceed', min(0.95, round(composite + 0.20, 3))
        if composite >= 0.35: return 'Monitor', 0.70
        return 'Exclude', 0.80

engine = FinalDecisionEngine()

# ── NAV ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
    <div class="nav-logo">
        <div class="nav-logo-icon">🧬</div>
        <span class="nav-logo-text">SLE Trial Intelligence</span>
    </div>
    <div style="display:flex;align-items:center;gap:1rem;">
        <span class="nav-badge">AI POWERED</span>
        <span class="nav-version">v1.0 · Research Use Only</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">🔬 Systemic Lupus Erythematosus</div>
    <h1>Clinical Trial <em>Enrollment</em><br>Decision Support</h1>
    <p>AI-powered pipeline using 3 models to evaluate patient eligibility,
       trial success probability, and side effect risk in real time.</p>
    <div class="hero-stats">
        <div><div class="hero-stat-val">3</div><div class="hero-stat-label">ML Models</div></div>
        <div><div class="hero-stat-val">11</div><div class="hero-stat-label">Patient Features</div></div>
        <div><div class="hero-stat-val">12</div><div class="hero-stat-label">Trial Features</div></div>
        <div><div class="hero-stat-val">3</div><div class="hero-stat-label">Outcomes</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="content-area">', unsafe_allow_html=True)

# ── TRIAL PARAMS ──────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">📋 Trial Parameters</p>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="card"><div class="card-header">🔬 Phase & Duration</div>', unsafe_allow_html=True)
    phase_num      = st.selectbox("Trial Phase", [1, 2, 3, 4])
    trial_duration = st.number_input("Duration (Days)", value=365, min_value=1)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card"><div class="card-header">👥 Enrollment</div>', unsafe_allow_html=True)
    enrollment        = st.number_input("Enrollment Size", value=100, min_value=1)
    is_interventional = st.checkbox("Interventional Trial", value=True)
    has_collaborator  = st.checkbox("Has Collaborator")
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="card"><div class="card-header">💰 Funding Source</div>', unsafe_allow_html=True)
    is_industry = st.checkbox("Industry Sponsored")
    is_nih      = st.checkbox("NIH Funded")
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="card"><div class="card-header">🏥 Disease Area</div>', unsafe_allow_html=True)
    disease_autoimmune = st.checkbox("Autoimmune", value=True)
    disease_cardiology = st.checkbox("Cardiology")
    disease_infectious = st.checkbox("Infectious Disease")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-title">🏥 Patient Profile</p>', unsafe_allow_html=True)

col5, col6, col7 = st.columns(3)
with col5:
    st.markdown('<div class="card"><div class="card-header">👤 Demographics</div>', unsafe_allow_html=True)
    age          = st.number_input("Age (Years)", value=40, min_value=18, max_value=100)
    bmi          = st.number_input("BMI", value=24.5, min_value=10.0, max_value=60.0)
    genetic_risk = st.slider("Genetic Risk Score", 0.0, 1.0, 0.25)
    st.markdown('</div>', unsafe_allow_html=True)
with col6:
    st.markdown('<div class="card"><div class="card-header">💊 Treatment History</div>', unsafe_allow_html=True)
    comorbidities      = st.slider("Comorbidities", 0, 10, 1)
    prior_treatments   = st.slider("Prior Treatments", 0, 10, 2)
    trial_phase        = st.selectbox("Patient Trial Phase", [1, 2, 3])
    drug_dosage        = st.number_input("Drug Dosage (mg)", value=5.0)
    treatment_duration = st.number_input("Treatment Duration (Days)", value=90, min_value=1)
    st.markdown('</div>', unsafe_allow_html=True)
with col7:
    st.markdown('<div class="card"><div class="card-header">🔬 Lab Values</div>', unsafe_allow_html=True)
    biomarker_level = st.number_input("Biomarker Level", value=3.2)
    creatinine      = st.number_input("Creatinine Level", value=0.9)
    liver_enzyme    = st.number_input("Liver Enzyme Level", value=28.0)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
run = st.button("🔍 Run Clinical Trial Analysis")

if run:
    with st.spinner("Running AI pipeline — analyzing patient data..."):
        time.sleep(1.2)

    trial_dict = {
        'phase_num': float(phase_num), 'log_enrollment': np.log1p(enrollment),
        'trial_duration': trial_duration, 'is_industry': int(is_industry),
        'is_nih': int(is_nih), 'is_interventional': int(is_interventional),
        'has_collaborator': int(has_collaborator),
        'phase_x_enrollment': float(phase_num) * np.log1p(enrollment),
        'disease_autoimmune': int(disease_autoimmune),
        'disease_cardiology': int(disease_cardiology),
        'disease_infectious': int(disease_infectious), 'disease_other': 0,
    }
    patient_dict = {
        'patient_age': float(age), 'patient_bmi': float(bmi),
        'comorbidities': comorbidities, 'prior_treatments': prior_treatments,
        'biomarker_level': biomarker_level, 'trial_phase': trial_phase,
        'drug_dosage': drug_dosage, 'treatment_duration': treatment_duration,
        'genetic_risk_score': genetic_risk, 'lab_creatinine': creatinine,
        'lab_liver_enzyme': liver_enzyme,
    }

    trial_df     = pd.DataFrame([trial_dict])
    X1           = bundle['scaler1'].transform(trial_df[bundle['m1_features']])
    success_prob = float(bundle['model1'].predict_proba(X1)[0, 1])
    patient_df   = pd.DataFrame([patient_dict])
    X2           = bundle['scaler2'].transform(patient_df[bundle['m23_features']])
    eligible     = bool(bundle['model2'].predict(X2)[0])
    X3           = bundle['scaler3'].transform(patient_df[bundle['m23_features']])
    risk_label   = engine.RISK_LABELS[bundle['model3'].predict(X3)[0]]
    rec, conf    = engine.decide(success_prob, eligible, risk_label)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">📊 Analysis Results</p>', unsafe_allow_html=True)

    # ── Metric Cards ──────────────────────────────────────────────────────────
    elig_col  = "green" if eligible else "red"
    elig_hex  = "#00f5a0" if eligible else "#ff3860"
    elig_text = "Eligible ✓" if eligible else "Ineligible ✗"
    risk_hex  = {"Low": "#00f5a0", "Medium": "#ffd60a", "High": "#ff3860"}
    risk_cls  = {"Low": "teal", "Medium": "amber", "High": "red"}

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""<div class="metric-card blue" style="animation-delay:0s">
            <div class="metric-tag">Trial Success Probability</div>
            <div class="metric-val" style="color:#1A7FE8;text-shadow:0 0 20px rgba(26,127,232,0.5)">{success_prob:.1%}</div>
            <div class="metric-sub">Gradient Boosting Model</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="metric-card {elig_col}" style="animation-delay:0.15s">
            <div class="metric-tag">Patient Eligibility</div>
            <div class="metric-val" style="color:{elig_hex};text-shadow:0 0 20px {elig_hex}88">{elig_text}</div>
            <div class="metric-sub">Logistic Regression Model</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="metric-card {risk_cls[risk_label]}" style="animation-delay:0.3s">
            <div class="metric-tag">Side Effect Risk</div>
            <div class="metric-val" style="color:{risk_hex[risk_label]};text-shadow:0 0 20px {risk_hex[risk_label]}88">{risk_label}</div>
            <div class="metric-sub">Random Forest Model</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Verdict ───────────────────────────────────────────────────────────────
    icons = {"Proceed": "✅", "Monitor": "⚠️", "Exclude": "🚫"}
    descs = {
        "Proceed": "Patient is a strong candidate. Recommend proceeding with full enrollment and standard monitoring protocols.",
        "Monitor": "Patient may be eligible but requires close supervision. Additional screening recommended before final decision.",
        "Exclude": "Patient does not meet trial criteria based on composite risk assessment. Exclusion recommended."
    }
    vclass = rec.lower()
    st.markdown(f"""
    <div class="verdict-banner {vclass}">
        <div class="verdict-icon-wrap">{icons[rec]}</div>
        <div class="verdict-body">
            <div class="verdict-label">Final Recommendation</div>
            <div class="verdict-title-text">{rec}</div>
            <div class="verdict-desc">{descs[rec]}</div>
        </div>
        <div class="verdict-conf">
            <div class="conf-val">{conf:.0%}</div>
            <div class="conf-label">Confidence Score</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">📈 Diagnostic Charts</p>', unsafe_allow_html=True)

    CHART_BG = '#161B22'
    GRID_COL = '#1e2d3d'
    TICK_COL = '#4a7a9b'

    ch1, ch2 = st.columns(2)

    # Gauge
    with ch1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=success_prob * 100,
            number={'suffix': '%', 'valueformat': '.1f',
                    'font': {'size': 44, 'family': 'DM Serif Display', 'color': '#00f5d4'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1,
                         'tickcolor': TICK_COL, 'tickfont': {'size': 10, 'color': TICK_COL}},
                'bar':  {'color': '#00f5d4', 'thickness': 0.22},
                'bgcolor': CHART_BG, 'borderwidth': 0,
                'steps': [
                    {'range': [0,  40], 'color': '#1a0a0a'},
                    {'range': [40, 65], 'color': '#1a1500'},
                    {'range': [65, 100],'color': '#001a12'},
                ],
                'threshold': {'line': {'color': '#00f5d4', 'width': 3},
                              'thickness': 0.8, 'value': success_prob * 100}
            },
            title={'text': 'Trial Success Probability',
                   'font': {'size': 13, 'family': 'DM Sans', 'color': '#a0c4e8'}}
        ))
        fig_gauge.update_layout(
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
            height=280, margin=dict(t=60, b=20, l=30, r=30),
            font={'family': 'DM Sans'}
        )
        st.markdown('<div class="chart-card" style="animation-delay:0.4s">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Trial Success Gauge</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-subtitle">MODEL 1 · GRADIENT BOOSTING · RED=LOW / AMBER=MED / GREEN=HIGH</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Radar
    with ch2:
        categories = ['Genetic Risk', 'Comorbidity', 'Lab Risk', 'Treatment Hx', 'Age Risk']
        vals = [
            round(genetic_risk, 2),
            round(min(comorbidities / 10, 1), 2),
            round(min((creatinine / 2.5 + liver_enzyme / 100) / 2, 1), 2),
            round(min(prior_treatments / 10, 1), 2),
            round(min((age - 18) / 52, 1), 2),
        ]
        fig_radar = go.Figure(go.Scatterpolar(
            r=vals + [vals[0]], theta=categories + [categories[0]],
            fill='toself', fillcolor='rgba(0,245,212,0.08)',
            line=dict(color='#00f5d4', width=2),
            marker=dict(color='#00f5d4', size=7)
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor=CHART_BG,
                radialaxis=dict(visible=True, range=[0, 1],
                                tickfont=dict(size=9, color=TICK_COL),
                                gridcolor=GRID_COL, linecolor=GRID_COL),
                angularaxis=dict(tickfont=dict(size=10, color='#a0c4e8'),
                                 gridcolor=GRID_COL, linecolor=GRID_COL)
            ),
            paper_bgcolor=CHART_BG, height=280,
            margin=dict(t=30, b=20, l=50, r=50),
            showlegend=False, font={'family': 'DM Sans'}
        )
        st.markdown('<div class="chart-card" style="animation-delay:0.5s">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Patient Risk Radar</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-subtitle">MODEL 3 · NORMALIZED RISK DIMENSIONS</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    ch3, ch4 = st.columns(2)

    # Bar
    with ch3:
        features = ['Age', 'BMI', 'Comorbid.', 'Prior Tx', 'Biomarker',
                    'Creatinine', 'Liver Enz.', 'Genetic', 'Dosage']
        raw_vals = [
            age / 100, bmi / 40, comorbidities / 10, prior_treatments / 10,
            min(biomarker_level / 15, 1), min(creatinine / 2.5, 1),
            min(liver_enzyme / 100, 1), genetic_risk, min(drug_dosage / 15, 1)
        ]
        bar_colors = ['#00f5d4' if v < 0.5 else '#ffd60a' if v < 0.75 else '#ff3860'
                      for v in raw_vals]
        fig_bar = go.Figure(go.Bar(
            x=features, y=[round(v, 2) for v in raw_vals],
            marker_color=bar_colors, marker_line_width=0,
            text=[f"{v:.0%}" for v in raw_vals],
            textposition='outside',
            textfont=dict(size=9, color='#a0c4e8')
        ))
        fig_bar.update_layout(
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG, height=280,
            margin=dict(t=20, b=20, l=20, r=20),
            xaxis=dict(tickfont=dict(size=9, color=TICK_COL),
                       gridcolor=GRID_COL, linecolor=GRID_COL),
            yaxis=dict(tickfont=dict(size=9, color=TICK_COL),
                       gridcolor=GRID_COL, linecolor=GRID_COL, range=[0, 1.25]),
            showlegend=False, font={'family': 'DM Sans'}, bargap=0.35
        )
        st.markdown('<div class="chart-card" style="animation-delay:0.6s">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Patient Feature Profile</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-subtitle">NORMALIZED VALUES · CYAN=SAFE / AMBER=CAUTION / RED=HIGH RISK</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Donut
    with ch4:
        composite = success_prob * engine.SE_WEIGHTS[risk_label]
        remaining = max(1 - composite, 0)
        fig_donut = go.Figure(go.Pie(
            values=[round(composite, 3), round(remaining, 3)],
            labels=['Composite Score', 'Remaining'],
            hole=0.62,
            marker=dict(colors=['#00f5d4', '#1e2d3d'],
                        line=dict(color=CHART_BG, width=3)),
            textinfo='none', hoverinfo='label+percent'
        ))
        fig_donut.add_annotation(
            text=f"<b>{composite:.0%}</b>",
            x=0.5, y=0.55, showarrow=False,
            font=dict(size=28, family='DM Serif Display', color='#00f5d4')
        )
        fig_donut.add_annotation(
            text="composite",
            x=0.5, y=0.38, showarrow=False,
            font=dict(size=11, family='DM Sans', color='rgba(0,245,212,0.4)')
        )
        fig_donut.update_layout(
            paper_bgcolor=CHART_BG, height=280,
            margin=dict(t=20, b=30, l=20, r=20),
            showlegend=True,
            legend=dict(font=dict(size=10, color='#a0c4e8'),
                        orientation='h', x=0.1, y=-0.12),
            font={'family': 'DM Sans'}
        )
        st.markdown('<div class="chart-card" style="animation-delay:0.7s">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Composite Decision Score</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-subtitle">SUCCESS PROB × SIDE EFFECT WEIGHT · THRESHOLD: 0.55 = PROCEED</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="app-footer">
    SLE CLINICAL TRIAL INTELLIGENCE &nbsp;·&nbsp;
    GB + LR + RF MODELS &nbsp;·&nbsp;
    FOR RESEARCH USE ONLY — NOT FOR CLINICAL DIAGNOSIS
</div>
""", unsafe_allow_html=True)