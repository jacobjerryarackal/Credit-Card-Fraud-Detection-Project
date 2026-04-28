# Architecture: Credit Card Fraud Detection

## MLOps Pipeline Overview
1. Data Ingestion → 2. Data Validation → 3. Feature Engineering → 4. Model Training → 5. Model Evaluation → 6. Model Registry → 7. Deployment

## Data Plan
- **Ingestion**: Load static `credit_card_fraud_dataset.csv` directly from local disk via a ZenML pipeline step.
- **Versioning**: Rely on ZenML's built-in artifact tracking (hashes and versions the dataset each run).
- **Validation**: Strict schema enforcement (e.g., target is exactly 0/1, no unexpected missing values in critical columns).
- **Storage**: Local filesystem.

## Feature Engineering Plan
- **Numeric Features**: `RobustScaler` (handles extreme transaction amount outliers better than standard scaling).
- **Categorical Features**: One-Hot Encoding.
- **Missing Values**: Median imputation (numerics), Mode imputation (categoricals).
- **Feature Selection**: Drop `transaction_id` and `transaction_datetime`.
- **Bundling**: All transformations wrapped in a single `sklearn.Pipeline` with the model to completely prevent training-serving skew.
- **Feature Store**: Not needed for MVP.

## Training & Evaluation Plan
- **Baseline Model**: Logistic Regression.
- **Candidate Models**: LightGBM or XGBoost (if the baseline is insufficient).
- **Experiment Tracking**: MLflow (logs hyperparameters, metrics, and models).
- **Evaluation Strategy**: Stratified 80/20 train-test split to preserve severe class imbalance.
- **Metrics**: F1-Score, PR-AUC, Precision, Recall.

## Deployment Plan
- **Type**: Batch inference pipeline (scores bulk transactions).
- **Promotion**: Manual review, then tag as "Production" in MLflow.
- **Strategy**: Direct replacement (batch pipeline pulls whatever is tagged "Production").
- **Rollback**: Manually revert the MLflow tag to the previous version.

## Monitoring & Drift Plan
- **Data Drift Detection**: Evidently AI (e.g., Wasserstein distance on `amount_usd`).
- **Performance Monitoring**: Track the overall fraud flag rate over time.
- **Alerting**: Alert triggered if critical feature drift is detected.
- **Retraining Trigger**: Manual kickoff based on the alert.

## Versioning & Governance
- **Registry**: MLflow Model Registry.
- **Promotion Workflow**: Dev pipeline → Manual Review → "Production" tag.
- **Audit Trail**: ZenML automatically links the model version to the exact data, code, and parameters that produced it.

## ZenML Stack Specification
| Component | Choice | Why |
|-----------|--------|-----|
| **Orchestrator** | `local` | Runs pipelines directly on machine. |
| **Artifact Store**| `local` | Stores artifacts in a local directory. |
| **Experiment Tracker** | `mlflow` | Logs hyperparameters, metrics, and models. |
| **Data Validator**| `evidently` | Runs statistical drift tests. |
| **Model Registry**| `mlflow` | Stores models and production tags. |

## Pipeline Decomposition
- **Training pipeline**: Ingest → Validate → Split → Preprocess & Train → Evaluate → Register
- **Inference pipeline**: Load Prod Model & Data → Predict → Output Results
- **Drift detection pipeline**: Compare inference batch distribution vs training baseline

## Project Structure
```text
credit-card-fraud-detection/
├── core/               # Pure Python logic — NO framework imports
│   ├── __init__.py
│   ├── preprocessing.py  # Scaler, encoder, pipeline building
│   ├── validation.py     # Data quality checks
│   └── evaluation.py     # Metric computation
├── steps/              # Framework steps — import from core/
├── pipelines/          # Framework pipelines
└── tests/              # Tests import from core/
```

## MVP Scope
1. Set up project structure and register the local ZenML stack.
2. Build data ingestion and validation core logic.
3. Build the training pipeline with `sklearn.Pipeline` preprocessing and MLflow.
4. Establish Logistic Regression baseline.
5. Build batch inference pipeline.

## Deferred Components
- Real-time HTTP API deployment (e.g., BentoML)
- Fully automated retraining triggers
- Remote orchestration (cloud execution)
