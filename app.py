import streamlit as st
import requests
import json

st.set_page_config(page_title="Cardiovascular Risk Predictor", layout="wide")

st.markdown("""
    <style>
    .stRadio [data-testid="stMarkdownContainer"] p {
        font-weight: 600;
        font-size: 14px;
    }
    div[data-testid="stBlock"] {
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .risk-low {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
    .risk-moderate {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
    }
    .risk-high {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🫀 Cardiovascular Disease Risk Prediction")
st.markdown("Enter patient health data to analyze cardiovascular risk using AI-powered assessment.")


# n8n Webhook URL

N8N_WEBHOOK_URL = "https://alexngjiansheng.app.n8n.cloud/webhook/retention"


# Input Section
st.header("📋 Patient Clinical Metrics")

col_num1, col_num2, col_cat = st.columns([1, 1, 1.2], gap="large")

with col_num1:
    st.subheader("🧬 Basic & Vital Metrics")
    
    name = st.text_input("Patient Name", value="John Doe")
    
    age = st.slider(
        "Age (years)",
        min_value=18, max_value=80, value=50, step=1
    )
    
    bmi = st.slider(
        "BMI",
        min_value=15.0, max_value=45.0, value=25.0, step=0.5
    )
    
    systolic_bp = st.slider(
        "Systolic BP (mmHg)",
        min_value=90, max_value=180, value=120, step=1
    )
    
    diastolic_bp = st.slider(
        "Diastolic BP (mmHg)",
        min_value=60, max_value=110, value=80, step=1
    )
    
    heart_rate = st.slider(
        "Heart Rate (bpm)",
        min_value=50, max_value=100, value=72, step=1
    )

with col_num2:
    st.subheader("🩸 Blood Lab Results")
    
    glucose = st.slider(
        "Glucose (mg/dL)",
        min_value=70, max_value=200, value=95, step=5
    )
    
    hba1c = st.slider(
        "HbA1c Level (%)",
        min_value=4.0, max_value=9.0, value=5.5, step=0.1
    )
    
    cholesterol = st.slider(
        "Total Cholesterol (mg/dL)",
        min_value=125, max_value=280, value=190, step=5
    )
    
    triglycerides = st.slider(
        "Triglycerides (mg/dL)",
        min_value=50, max_value=300, value=150, step=5
    )
    
    hdl = st.slider(
        "HDL Cholesterol (mg/dL)",
        min_value=35, max_value=80, value=55, step=1
    )
    
    ldl = st.slider(
        "LDL Cholesterol (mg/dL)",
        min_value=50, max_value=180, value=100, step=5
    )

with col_cat:
    st.subheader("📑 Patient Profile")
    
    gender = st.radio("Gender", ["Female", "Male"], horizontal=True)
    smoking = st.radio("Smoking History", ["Never", "Former", "Current"], horizontal=True)
    physical_activity = st.radio("Physical Activity Level", ["Low", "Moderate", "High"], horizontal=True)
    stress_level = st.radio("Stress Level", ["Low", "Medium", "High"], horizontal=True)
    sugar_consumption = st.radio("Sugar Consumption", ["Low", "Medium", "High"], horizontal=True)
    education_level = st.radio("Education Level", ["Primary", "Secondary", "Tertiary"], horizontal=True)
    employment_status = st.radio("Employment Status", ["Unemployed", "Employed", "Retired"], horizontal=True)
    
    st.markdown("**Medical History**")
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    with sub_col1:
        diabetes = st.radio("Diabetes", ["No", "Yes"], horizontal=False)
    with sub_col2:
        family_history = st.radio("Family History", ["No", "Yes"], horizontal=False)
    with sub_col3:
        st.write("")



def build_features():
    smoking_map = {"Never": 2, "Former": 1, "Current": 0}
    physical_map = {"Low": 0, "Moderate": 1, "High": 2}
    stress_map = {"Low": 0, "Medium": 1, "High": 2}
    sugar_map = {"Low": 0, "Medium": 1, "High": 2}
    education_map = {"Primary": 0, "Secondary": 1, "Tertiary": 2}
    employment_map = {"Unemployed": 0, "Employed": 1, "Retired": 2}
    
    if age < 30:
        age_level = 0
    elif age < 50:
        age_level = 1
    elif age < 65:
        age_level = 2
    else:
        age_level = 3
    
    if bmi < 18.5:
        bmi_level = 0
    elif bmi < 25:
        bmi_level = 1
    elif bmi < 30:
        bmi_level = 2
    else:
        bmi_level = 3
    
    high_bp = 1 if (systolic_bp >= 140 or diastolic_bp >= 90) else 0
    
    if gender == "Female":
        low_hdl = 1 if hdl < 50 else 0
    else:
        low_hdl = 1 if hdl < 40 else 0
    
    high_ldl = 1 if ldl >= 160 else 0
    
    features = [
        age_level,
        bmi_level,
        smoking_map[smoking],
        float(age),
        float(age) / 100,
        float(bmi),
        float(hba1c),
        float(glucose),
        float(cholesterol),
        7.0,
        float(triglycerides),
        physical_map[physical_activity],
        stress_map[stress_level],
        (systolic_bp + diastolic_bp) / 2,
        sugar_map[sugar_consumption],
        5.0,
        10.0,
        float(systolic_bp),
        float(diastolic_bp),
        10.0,
        8.0,
        float(heart_rate),
        float(hdl),
        float(ldl),
        education_map[education_level],
        employment_map[employment_status],
        1.0 if gender == "Female" else 0.0,
        1.0 if gender == "Male" else 0.0,
        1.0 if diabetes == "No" else 0.0,
        1.0 if diabetes == "Yes" else 0.0,
        1.0 if family_history == "No" else 0.0,
        1.0 if family_history == "Yes" else 0.0,
        1.0 if high_bp == 0 else 0.0,
        1.0 if high_bp == 1 else 0.0,
        1.0 if low_hdl == 0 else 0.0,
        1.0 if low_hdl == 1 else 0.0,
        1.0 if high_ldl == 0 else 0.0,
        1.0 if high_ldl == 1 else 0.0,
    ]
    return features


st.markdown("---")

if st.button("🩺 Analyze Cardiovascular Risk", type="primary", use_container_width=True):
    try:
        with st.spinner("Analyzing patient data with AI..."):
            features = build_features()
            
            payload = {
                "name": name,
                "age": age,
                "bmi": bmi,
                "systolic_bp": systolic_bp,
                "diastolic_bp": diastolic_bp,
                "heart_rate": heart_rate,
                "glucose": glucose,
                "hba1c": hba1c,
                "cholesterol": cholesterol,
                "triglycerides": triglycerides,
                "hdl": hdl,
                "ldl": ldl,
                "gender": gender,
                "smoking": smoking,
                "physical_activity": physical_activity,
                "stress_level": stress_level,
                "sugar_consumption": sugar_consumption,
                "education_level": education_level,
                "employment_status": employment_status,
                "diabetes": diabetes,
                "family_history": family_history,
                "features": features
            }
            
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                
                st.header("📊 Assessment Results")
                
                # Risk Tier with color coding
                risk_tier = result.get("risk_tier", "Unknown")
                if risk_tier == "Low":
                    st.markdown(f'<div class="risk-low"><h3>🟢 Risk Tier: {risk_tier}</h3></div>', unsafe_allow_html=True)
                elif risk_tier == "Moderate":
                    st.markdown(f'<div class="risk-moderate"><h3>🟡 Risk Tier: {risk_tier}</h3></div>', unsafe_allow_html=True)
                elif risk_tier == "High":
                    st.markdown(f'<div class="risk-high"><h3>🔴 Risk Tier: {risk_tier}</h3></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<h3>Risk Tier: {risk_tier}</h3>', unsafe_allow_html=True)
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Prediction", result.get("prediction", "N/A"))
                with col2:
                    confidence = result.get("confidence", 0) * 100
                    st.metric("Confidence", f"{confidence:.1f}%")
                with col3:
                    st.metric("Normal Probability", f"{result.get('probabilities', {}).get('Normal', 0)*100:.1f}%")
                
                # Recommendation
                st.subheader("💡 Recommendation")
                st.info(result.get("recommendation", "No recommendation available."))
                
                # Draft Message
                with st.expander("📨 Draft Message to Patient"):
                    st.text_area("Message", result.get("draft_message", "No message available."), height=200)
                
            else:
                st.error(f"Error: {response.status_code}")
                st.text(response.text)
                
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to n8n. Please make sure the workflow is active and the URL is correct.")
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out. Please try again.")
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")



st.markdown("---")
st.caption("🫀 Cardiovascular Risk Predictor | Powered by n8n Agentic Workflow")