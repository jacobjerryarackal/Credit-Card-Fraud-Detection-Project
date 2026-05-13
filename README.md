# Credit Card Fraud Detection (MLOps MVP)

A production-grade, end-to-end Machine Learning pipeline for detecting credit card fraud using **ZenML**, **MLflow**, **scikit-learn**, and **Streamlit**.

This project demonstrates a full MLOps workflow:

* Model Training Pipeline
* Batch Inference Pipeline
* Experiment Tracking with MLflow
* Interactive Fraud Detection Frontend using Streamlit
* Production-ready deployment structure


---

# 📌 Business Context

The objective is to predict whether a credit card transaction is fraudulent at the time it occurs.

This helps prevent:

* financial loss
* chargebacks
* customer trust issues
* operational fraud investigation costs

Because both errors are expensive:

* **False Positive** → blocking a legitimate customer
* **False Negative** → allowing fraud

The system focuses on balancing:

* Precision
* Recall
* F1 Score
* PR-AUC

for strong fraud detection performance.

---

# 🏗 Architecture

This project contains:

## 1. Training Pipeline

Built using ZenML.

### Steps:

* Data ingestion + validation
* Missing value handling
* Feature engineering
* OneHot Encoding for categorical features
* RobustScaler for numerical outlier handling
* Model training using Random Forest / Logistic Regression
* Evaluation using Precision, Recall, F1, ROC-AUC
* MLflow experiment tracking
* Model artifact saving (`model.pkl`)

---

## 2. Batch Inference Pipeline

### Steps:

* Load latest trained model
* Load fresh batch transaction data
* Score fraud probability
* Detect high-risk transactions
* Trigger fraud alerts

---

## 3. Streamlit Frontend

### Features:

* Premium fraud detection dashboard
* Manual transaction testing
* Fraud probability scoring
* Risk level classification
* Recommended action (ALLOW / REVIEW / BLOCK)
* Business rule + ML hybrid fraud detection

---

# ⚙ Tech Stack

* **ZenML** → Pipeline orchestration
* **MLflow** → Experiment tracking
* **scikit-learn** → ML model training
* **Pandas** → Data processing
* **Streamlit** → Frontend deployment
* **Python 3.9+**

---

# 📦 ZenML Version Used

```bash
ZenML Version: 0.57.1
```

This version is stable for this project setup.

Using multiple ZenML versions may cause configuration issues.

---

# 🚀 Complete Setup Guide

---

## Step 1 — Activate Virtual Environment

```bash
venv\Scripts\activate
```

You must activate the virtual environment before running anything.

---

## Step 2 — Install Dependencies

```bash
pip install -e .
pip install zenml==0.57.1 mlflow evidently xgboost lightgbm pandas scikit-learn streamlit
```

---

## Step 3 — Initialize ZenML (Only Once)

```bash
zenml init
```

This only needs to be done once per project.

Do NOT repeat every time.

---

## Step 4 — Run Training Pipeline

```bash
python run_pipeline.py
```

This will:

* train the model
* log metrics
* save model artifact
* create MLflow runs
* generate `model.pkl`

---

## Step 5 — Run Batch Inference Pipeline

```bash
python run_inference.py
```

This will:

* fetch latest trained model
* score new transactions
* detect fraud risk
* generate fraud alerts

---

## Step 6 — View MLflow Dashboard

Use the exact command shown after pipeline execution.

Example:

```bash
mlflow ui --backend-store-uri "file:C:\Users\YOUR_USERNAME\AppData\Roaming\zenml\local_stores\...\mlruns"
```

Then open:

```text
http://127.0.0.1:5000
```

This shows:

* model metrics
* confusion matrix
* ROC curve
* PR curve
* model.pkl
* experiment history


---

## Step 7 — Run Streamlit Frontend

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

This launches the fraud detection application UI.

---

# 📁 Important Deployment Setup

Keep your trained model inside project root:

```text
credit-card-fraud-detection/
├── app.py
├── model.pkl
```

and use:

```python
MODEL_PATH = "model.pkl"
```

---

# 📂 Project Structure

```text
credit-card-fraud-detection/
│
├── core/                  # Validation, preprocessing, evaluation
├── steps/                 # ZenML step definitions
├── pipelines/             # ZenML pipeline definitions
├── data/                  # Dataset
├── app.py                 # Streamlit frontend
├── model.pkl              # Trained model artifact
├── run_pipeline.py        # Training pipeline entrypoint
├── run_inference.py       # Batch inference entrypoint
├── README.md
├── pyproject.toml
└── .gitignore
```

---

# 🎯 Project Value

This project demonstrates:

* End-to-end ML system design
* MLOps workflow understanding
* Production deployment thinking
* Experiment tracking
* Fraud detection business reasoning
* Real-world model serving

This makes it much stronger than a normal ML notebook project.

---

# 👨‍💻 Author

**Jacob Jerry Arackal**

Generative AI Engineer | MLOps | Full Stack Development | Production AI Systems

---

# ⭐ Final Note

This is not just a machine learning model.

It is a deployable fraud detection system built with production thinking.

