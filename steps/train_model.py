import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from zenml import step
import mlflow

from core.preprocessing import get_preprocessor
from core.evaluation import evaluate_classification_metrics

@step(experiment_tracker="mlflow_tracker")
def train_and_evaluate_model(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> Pipeline:
    """Trains a baseline Logistic Regression model and evaluates it, tracking with MLflow."""
    
    # We enable MLflow sklearn autologging to capture parameters instantly
    mlflow.sklearn.autolog()
    
    # 1. Build the full pipeline: Preprocessor + Model
    preprocessor = get_preprocessor()
    
    # We use class_weight='balanced' because fraud is only 0.8% of the data.
    # Without this, Logistic Regression might just predict 0 every time to achieve 99.2% accuracy!
    model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])
    
    # 2. Train the pipeline
    print("Training baseline Logistic Regression pipeline...")
    pipeline.fit(X_train, y_train)
    
    # 3. Evaluate the pipeline on the test set
    print("Evaluating on test set...")
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)[:, 1] # Probabilities for the fraud class (1)
    
    metrics = evaluate_classification_metrics(y_test, y_pred, y_pred_proba)
    
    # 4. Log custom metrics explicitly to MLflow
    for metric_name, metric_value in metrics.items():
        mlflow.log_metric(f"test_{metric_name}", metric_value)
        print(f"Test {metric_name.upper()}: {metric_value:.4f}")
        
    return pipeline
