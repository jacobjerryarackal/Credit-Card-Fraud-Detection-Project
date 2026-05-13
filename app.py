import streamlit as st
import pandas as pd
import joblib
import os

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Premium Fraud Detection System",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom Styling
# -----------------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(180deg, #050816 0%, #0b1020 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: white !important;
}

.stMarkdown, label {
    color: #E5E7EB !important;
}

[data-testid="stSidebar"] {
    background: #0B1120;
}

.stButton > button {
    width: 100%;
    height: 52px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(90deg, #2563EB, #7C3AED);
    color: white;
    font-weight: 700;
    font-size: 16px;
}

.stButton > button:hover {
    opacity: 0.95;
}

.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("⚙ System Overview")
st.sidebar.markdown("---")
st.sidebar.markdown("### Model Details")
st.sidebar.write("**Model:** Random Forest Classifier")
st.sidebar.write("**Pipeline:** ZenML + MLflow")
st.sidebar.write("**Deployment:** Streamlit")
st.sidebar.write("**Use Case:** Real-time Fraud Risk Scoring")

st.sidebar.markdown("---")
st.sidebar.markdown("### Risk Guidelines")
st.sidebar.success("0–30% → Low Risk")
st.sidebar.warning("30–70% → Medium Risk")
st.sidebar.error("70%+ → High Risk")


# -----------------------------
# Header
# -----------------------------
st.title("💳 Enterprise Credit Card Fraud Detection Platform")
st.markdown(
    "AI-powered transaction intelligence system for fraud prevention, risk scoring, and business decision automation."
)

st.markdown("---")


# -----------------------------
# Load Model
# -----------------------------
MODEL_PATH = r"C:\Users\JACOB\AppData\Roaming\zenml\local_stores\fb7f08c2-9d6d-4c4a-b6e9-e364ba90a952\mlruns\218947906238438872\6c41f7c8247b41acb62254b806c426fd\artifacts\model\model.pkl"


@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


model = load_model()

if model is None:
    st.error("Model file not found. Please run the training pipeline first.")
    st.stop()


# -----------------------------
# Input Section
# -----------------------------
st.subheader("📥 Transaction Intelligence Form")

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=500.0)
    transactions_last_1h = st.number_input("Transactions Last 1 Hour", min_value=0, value=1)
    distance_from_home = st.number_input("Distance From Home (km)", min_value=0.0, value=5.0)
    customer_age = st.number_input("Customer Age", min_value=18, value=30)

    merchant_category = st.selectbox(
        "Merchant Category",
        ["retail", "electronics", "travel", "food", "healthcare", "luxury"]
    )

with col2:
    is_foreign_transaction = st.selectbox("Foreign Transaction", [0, 1])
    card_present = st.selectbox("Card Present", [0, 1])
    cvv_match = st.selectbox("CVV Match", [0, 1])
    billing_address_match = st.selectbox("Billing Address Match", [0, 1])

    merchant_country = st.selectbox(
        "Merchant Country",
        ["USA", "India", "UK", "Canada", "Germany", "Singapore"]
    )


# -----------------------------
# Prediction Logic
# -----------------------------
if st.button("🚀 Analyze Transaction Risk"):

    input_data = pd.DataFrame([{
        "hour_of_day": 14,
        "day_of_week": 2,
        "is_weekend": 0,

        "amount_usd": amount,
        "is_foreign_transaction": is_foreign_transaction,
        "distance_from_home_km": distance_from_home,

        "card_present": card_present,
        "chip_used": 0 if card_present == 0 else 1,
        "pin_used": 0 if card_present == 0 else 1,

        "billing_address_match": billing_address_match,
        "cvv_match": cvv_match,

        "transactions_last_1h": transactions_last_1h,
        "transactions_last_24h": max(3, transactions_last_1h + 2),

        "avg_transaction_amount_last_30d": 200,
        "amount_vs_avg_ratio": amount / 200,

        "days_since_last_transaction": 0,

        "customer_age_years": customer_age,
        "account_age_days": 30,

        "is_new_merchant": 1 if is_foreign_transaction == 1 else 0,
        "velocity_flag": 1 if transactions_last_1h > 5 else 0,

        "merchant_category": merchant_category,
        "merchant_country": merchant_country
    }])

    prediction = model.predict(input_data)[0]

    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(input_data)[0][1]
    else:
        probability = 0.0

    if amount > 1000 and is_foreign_transaction == 1:
        risk_level = "MEDIUM"

    if amount > 5000 and is_foreign_transaction == 1 and cvv_match == 0:
        risk_level = "HIGH"
        prediction = 1
        probability = max(probability, 0.85)

    st.markdown("---")
    st.subheader("📊 Fraud Risk Assessment")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("Fraud Probability", f"{probability:.2%}")

    with m2:
        if "risk_level" not in locals():
            if probability > 0.70:
                risk_level = "HIGH"
            elif probability > 0.30:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"
        st.metric("Risk Level", risk_level)

    with m3:
        if prediction == 1:
            action = "BLOCK"
        else:
            action = "ALLOW"
        st.metric("Recommended Action", action)

    if prediction == 1:
        st.error("🚨 Fraudulent Transaction Detected")
        st.warning("Recommended Action: Immediately hold transaction and trigger manual review.")
    else:
        st.success("✅ Legitimate Transaction")
        st.info("Recommended Action: Transaction may proceed normally.")
