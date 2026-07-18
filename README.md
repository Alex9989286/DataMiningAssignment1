# Cardiovascular Disease Risk Prediction System

An end-to-end autonomous agentic AI system for cardiovascular disease risk prediction using data mining, machine learning, and n8n workflow automation.

---

## 📋 Overview

Cardiovascular diseases (CVDs) are the leading cause of death worldwide, accounting for approximately 17.9 million deaths annually. This project addresses this global health challenge by developing an autonomous agentic AI system that:

- Analyzes patient health data using machine learning
- Predicts cardiovascular disease risk (Normal/Abnormal)
- Reasons over predictions using AI agents
- Generates personalized health recommendations
- Automates the entire workflow with minimal human intervention

The system integrates a trained Decision Tree classifier with an n8n workflow and a Google Gemini AI agent to provide end-to-end risk assessment and patient communication.

---

## ✨ Features

| Feature | Description |
|:---|:---|
| Data Mining | Comprehensive EDA with visualizations, correlation analysis, and outlier detection |
| Machine Learning | Decision Tree classifier with 87.94% accuracy |
| Feature Engineering | Automated generation of 36 features from 24 user inputs |
| Model Deployment | FastAPI RESTful API hosted on Render.com |
| Agentic Workflow | n8n orchestration with 4-node pipeline |
| AI Reasoning | Google Gemini AI agent for risk assessment and recommendation generation |
| User Interface | Streamlit web application for easy data input and results visualization |
| Real-time Predictions | Instant risk assessment with confidence scores |

---

## 📊 Dataset

**Source**: Multi-Class Chronic Disease Data Warehouse by Omar Elzeki (Mendeley Data, DOI: 10.17632/6vnkkf5hv3.1)

| Attribute | Value |
|:---|:---|
| Records | 280,985 |
| Original Features | 39 |
| Final Features | 36 |
| Missing Values | None |
| Target Classes | Normal / Abnormal |
| Class Distribution | Abnormal: 62.0%, Normal: 38.0% |

**Feature Categories**: Demographics (age, gender, education), Clinical Measurements (BMI, blood pressure, heart rate), Lab Biomarkers (glucose, HbA1c, cholesterol, triglycerides, HDL, LDL), Lifestyle Factors (smoking, physical activity, stress, sleep, sugar, salt, alcohol), Medical History (family history)

---

## 🏗️ Architecture

### System Architecture

The system follows a 5-layer agentic AI architecture:

```
Webhook → HTTP Request (FastAPI) → AI Agent (Gemini) → Respond to Webhook
  ↓              ↓                        ↓                    ↓
 接收数据      调用预测模型             分析结果+生成建议      返回JSON
```

### Data Flow

| Step | From | To | Description |
|:---|:---|:---|:---|
| 1 | User | Trigger Layer | Patient enters health data via Streamlit (24 input fields) |
| 2 | Trigger Layer | Data Ingestion Layer | Streamlit sends POST request to n8n webhook |
| 3 | Data Ingestion Layer | Prediction Layer | n8n sends 36 features to FastAPI `/predict` on Render |
| 4 | Prediction Layer | AI Agent Layer | Returns prediction with confidence and probabilities |
| 5 | AI Agent Layer | Action Layer | Gemini generates risk tier, recommendation, and draft message |
| 6 | Action Layer | User | Respond to Webhook returns JSON to Streamlit |

### 36-Feature Generation

The 36 features are automatically generated from 24 user inputs using the `build_features()` function:

| User Input | Generated Features |
|:---|:---|
| Age | age, age_level, age_normalized |
| BMI | bmi, bmi_level |
| Systolic BP, Diastolic BP | systolic_bp, diastolic_bp, blood_pressure, high_blood_pressure_No/Yes |
| HDL, Gender | hdl, low_hdl_cholesterol_No/Yes |
| LDL | ldl, high_ldl_cholesterol_No/Yes |
| Family History | family_history_No, family_history_Yes |
| Gender | gender_Female, gender_Male |
| Sleep Hours | sleep_hours |
| Alcohol Intake | alcohol_intake |
| Salt Intake | salt_intake |
| Smoking | smoking |
| Physical Activity | physical_activity |
| Stress Level | stress_level |
| Sugar Consumption | sugar_consumption |
| Education Level | education_level |
| Employment Status | employment_status |
| Fixed Defaults | crp_level=5.0, homocysteine_level=10.0 |

---

## 🛠️ Tech Stack

| Category | Technology |
|:---|:---|
| Frontend | Streamlit |
| Backend API | FastAPI, Uvicorn |
| Machine Learning | Scikit-learn (Decision Tree) |
| Workflow Orchestration | n8n |
| AI Agent | Google Gemini |
| Deployment | Render.com |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Model Serialization | Joblib |

**Python Version**: 3.11.11

---

## 📁 Project Structure

```
DataMiningAssignment1/
├── app.py                         # Streamlit frontend
├── main.py                        # FastAPI backend
├── cardiovascular_model.pkl       # Trained Decision Tree model
├── scaler.pkl                     # StandardScaler
├── feature_names_fixed.pkl        # Feature names (36 features)
├── requirements.txt               # Python dependencies
├── .python-version                # Python version specification
├── SWE2304249_SWE402_Assignment.pdf  # Final report
├── SWE2304249_SWE402_n8n.json     # n8n workflow export
└── README.md                      # This file
```

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Alex9989286/DataMiningAssignment1.git
cd DataMiningAssignment1
pip install -r requirements.txt
```

### Run Backend

```bash
python main.py
# API available at: http://localhost:8000
```

### Run Frontend

```bash
streamlit run app.py
# Web app available at: http://localhost:8501
```

### Deployed Version

- **API**: https://dataminingassignment1.onrender.com
- **Health Check**: https://dataminingassignment1.onrender.com/health

---

## 🔗 API Endpoints

| Endpoint | Method | Description |
|:---|:---|:---|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/features` | GET | List of 36 feature names |
| `/predict` | POST | Make a prediction |

### Sample Request

```json
{
  "features": [1, 1, 2, 50, 0.5, 25, 5.5, 95, 190, 7, 150, 0, 0, 100, 0, 5, 10, 120, 80, 0, 1, 72, 55, 100, 2, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
}
```

### Sample Response

```json
{
  "prediction": "Normal",
  "confidence": 0.82,
  "probabilities": {
    "Abnormal": 0.18,
    "Normal": 0.82
  }
}
```

---

## 📊 Results

### Model Performance

| Metric | Value |
|:---|:---|
| Accuracy | 87.94% |
| F1-Score | 82.56% |
| Precision (Abnormal) | 89.99% |
| Recall (Abnormal) | 75.76% |

### Confusion Matrix (Test Set)

| | Predicted Abnormal | Predicted Normal |
|:---|:---|:---|
| Actual Abnormal | 33,097 | 1,723 |
| Actual Normal | 4,946 | 16,431 |

### Top 5 Most Important Features

| Rank | Feature | Importance |
|:---|:---|:---|
| 1 | HbA1c_level | 0.568 |
| 2 | triglycerides | 0.215 |
| 3 | sleep_hours | 0.102 |
| 4 | glucose | 0.019 |
| 5 | cholesterol | 0.018 |

---

## 🔮 Future Improvements

| Improvement | Description |
|:---|:---|
| Temporal Data | Incorporate longitudinal health data for dynamic risk monitoring |
| Multi-Label Classification | Predict individual diseases (diabetes, hypertension, heart disease) separately |
| SHAP Explainability | Add SHAP values to explain model predictions to users |
| Real-Time Monitoring | Support health data from wearable devices |
| Multi-Language Support | Generate draft messages in multiple languages |
| Authentication | Add secure authentication for API access |

---

## 👤 Author

**Alex Ng Jian Sheng** (SWE2304249)  
SWE402 Data Mining, Xiamen University Malaysia  
Lecturer: Teo Bee Guan

---

## 🙏 Acknowledgments

- Dr. Teo Bee Guan for supervision
- World Health Organization for health statistics
- World Heart Federation for CVD information
- Mendeley Data for dataset

