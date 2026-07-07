# ============================================================
# app.py - Cardiovascular Disease Risk Prediction (38 Features)
# 调整所有数值为正常临床范围
# ============================================================

import streamlit as st
import requests

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
    </style>
""", unsafe_allow_html=True)

st.title("🫀 Cardiovascular Disease Risk Prediction")
st.markdown("Move the sliders and select the health metrics below to analyze patient cardiovascular risk.")

# API URL
API_URL = "http://localhost:8000/predict"

# ---- Input Section ----
st.header("📋 Patient Clinical Metrics")

col_num1, col_num2, col_cat = st.columns([1, 1, 1.2], gap="large")

with col_num1:
    st.subheader("🧬 Basic & Vital Metrics")
    
    # 年龄: 正常范围 18-80
    age = st.slider(
        "Age (years)",
        min_value=18, max_value=80, value=50, step=1,
        help="Normal: 18-80 years"
    )
    
    # BMI: 正常范围 15-45
    bmi = st.slider(
        "BMI",
        min_value=15.0, max_value=45.0, value=25.0, step=0.5,
        help="Normal: 18.5-24.9, Overweight: 25-29.9, Obese: 30+"
    )
    
    # 收缩压: 正常范围 90-180
    systolic_bp = st.slider(
        "Systolic BP (mmHg)",
        min_value=90, max_value=180, value=120, step=1,
        help="Normal: <120, Elevated: 120-129, High: 130+"
    )
    
    # 舒张压: 正常范围 60-110
    diastolic_bp = st.slider(
        "Diastolic BP (mmHg)",
        min_value=60, max_value=110, value=80, step=1,
        help="Normal: <80, Elevated: 80-89, High: 90+"
    )
    
    # 心率: 正常范围 50-100
    heart_rate = st.slider(
        "Heart Rate (bpm)",
        min_value=50, max_value=100, value=72, step=1,
        help="Normal: 60-100 bpm"
    )

with col_num2:
    st.subheader("🩸 Blood Lab Results")
    
    # 血糖: 正常范围 70-200
    glucose = st.slider(
        "Glucose (mg/dL)",
        min_value=70, max_value=200, value=95, step=5,
        help="Normal fasting: <100, Prediabetes: 100-125, Diabetes: 126+"
    )
    
    # HbA1c: 正常范围 4.0-9.0
    hba1c = st.slider(
        "HbA1c Level (%)",
        min_value=4.0, max_value=9.0, value=5.5, step=0.1,
        help="Normal: <5.7, Prediabetes: 5.7-6.4, Diabetes: 6.5+"
    )
    
    # 总胆固醇: 正常范围 125-280
    cholesterol = st.slider(
        "Total Cholesterol (mg/dL)",
        min_value=125, max_value=280, value=190, step=5,
        help="Normal: <200, Borderline: 200-239, High: 240+"
    )
    
    # 甘油三酯: 正常范围 50-300
    triglycerides = st.slider(
        "Triglycerides (mg/dL)",
        min_value=50, max_value=300, value=150, step=5,
        help="Normal: <150, Borderline: 150-199, High: 200+"
    )
    
    # HDL: 正常范围 35-80
    hdl = st.slider(
        "HDL Cholesterol (mg/dL)",
        min_value=35, max_value=80, value=55, step=1,
        help="Normal: >40 (Male), >50 (Female)"
    )
    
    # LDL: 正常范围 50-180
    ldl = st.slider(
        "LDL Cholesterol (mg/dL)",
        min_value=50, max_value=180, value=100, step=5,
        help="Optimal: <100, Near optimal: 100-129, High: 160+"
    )

with col_cat:
    st.subheader("📑 Categorical Status & History")
    
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


# ---- Build features ----
def build_features():
    smoking_map = {"Never": 2, "Former": 1, "Current": 0}
    physical_map = {"Low": 0, "Moderate": 1, "High": 2}
    stress_map = {"Low": 0, "Medium": 1, "High": 2}
    sugar_map = {"Low": 0, "Medium": 1, "High": 2}
    education_map = {"Primary": 0, "Secondary": 1, "Tertiary": 2}
    employment_map = {"Unemployed": 0, "Employed": 1, "Retired": 2}
    
    # Age level (auto-calculated)
    if age < 30:
        age_level = 0
    elif age < 50:
        age_level = 1
    elif age < 65:
        age_level = 2
    else:
        age_level = 3
    
    # BMI level (auto-calculated)
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
    
    # 38 features
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

# ---- Predict ----
if st.button("🩺 Predict Cardiovascular Risk", type="primary", use_container_width=True):
    try:
        with st.spinner("Analyzing patient data..."):
            features = build_features()
            
            response = requests.post(API_URL, json={"features": features})
            
            if response.status_code == 200:
                result = response.json()
                
                st.header("📊 Prediction Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if result["prediction"] == "Normal":
                        st.success(f"✅ {result['prediction']}")
                    else:
                        st.error(f"⚠️ {result['prediction']}")
                
                with col2:
                    st.metric("Confidence", f"{result['confidence']*100:.1f}%")
                
                with col3:
                    st.metric("Risk Score", f"{(1 - result['confidence'])*100:.1f}%")
                
                st.subheader("📈 Probability Distribution")
                st.bar_chart({
                    "Class": ["Abnormal", "Normal"],
                    "Probability": [
                        result["probabilities"]["Abnormal"],
                        result["probabilities"]["Normal"]
                    ]
                }, x="Class", y="Probability")
                
                st.subheader("📋 Recommendation")
                if result["prediction"] == "Normal":
                    st.info("🟢 Low cardiovascular risk. Maintain healthy lifestyle.")
                else:
                    st.warning("🔴 Elevated cardiovascular risk. Consult a doctor.")
                
            else:
                st.error(f"Error: {response.status_code}")
                
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Please make sure FastAPI is running.")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")