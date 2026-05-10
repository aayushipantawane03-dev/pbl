import streamlit as st
import plotly.graph_objects as go
import time
import requests
import math

st.set_page_config(
    page_title="SLE Clinical Trial Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- DECISION ENGINE (KEEP) ----------------
class FinalDecisionEngine:
    SE_WEIGHTS  = {'Low': 1.0, 'Medium': 0.6, 'High': 0.2}
    def decide(self, success_prob, eligible, se_risk):
        if not eligible: return 'Exclude', 0.95
        if se_risk == 'High': return 'Exclude', 0.85
        composite = success_prob * self.SE_WEIGHTS[se_risk]
        if composite >= 0.55: return 'Proceed', min(0.95, round(composite + 0.20, 3))
        if composite >= 0.35: return 'Monitor', 0.70
        return 'Exclude', 0.80

engine = FinalDecisionEngine()

# ---------------- INPUT UI ----------------
st.title("🧬 SLE Clinical Trial Intelligence")

phase_num = st.selectbox("Trial Phase", [1,2,3,4])
trial_duration = st.number_input("Trial Duration", value=365)
enrollment = st.number_input("Enrollment", value=100)

age = st.number_input("Age", value=40)
bmi = st.number_input("BMI", value=24.5)
genetic_risk = st.slider("Genetic Risk", 0.0,1.0,0.2)

run = st.button("Run Analysis")

# ---------------- MAIN LOGIC ----------------
if run:
    with st.spinner("Running AI pipeline..."):
        time.sleep(1)

    trial_dict = {
        'phase_num': float(phase_num),
        'log_enrollment': math.log1p(enrollment),
        'trial_duration': trial_duration,
        'is_industry': 1,
        'is_nih': 0,
        'is_interventional': 1,
        'has_collaborator': 1,
        'phase_x_enrollment': float(phase_num) * math.log1p(enrollment),
        'disease_autoimmune': 1,
        'disease_cardiology': 0,
        'disease_infectious': 0,
        'disease_other': 0
    }

    patient_dict = {
        'patient_age': float(age),
        'patient_bmi': float(bmi),
        'comorbidities': 1,
        'prior_treatments': 2,
        'biomarker_level': 0.5,
        'trial_phase': 2,
        'drug_dosage': 5,
        'treatment_duration': 90,
        'genetic_risk_score': genetic_risk,
        'lab_creatinine': 1.0,
        'lab_liver_enzyme': 30
    }

    # 🔥 API CALL (IMPORTANT)
    api_url = "PASTE_YOUR_API_GATEWAY_URL_HERE"

    response = requests.post(api_url, json={
        "trial": trial_dict,
        "patient": patient_dict
    })

    result = response.json()

    success_prob = result['trial_success_probability']
    eligible = result['patient_eligible']
    risk_label = result['side_effect_risk']
    rec = result['final_recommendation']
    conf = result['confidence_score']

    # ---------------- OUTPUT ----------------
    st.subheader("Results")

    st.write("Success Probability:", success_prob)
    st.write("Eligible:", eligible)
    st.write("Risk:", risk_label)
    st.write("Recommendation:", rec)
    st.write("Confidence:", conf)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=success_prob * 100,
        title={'text': "Success Probability"}
    ))

    st.plotly_chart(fig)
```
