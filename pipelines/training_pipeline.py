from zenml import pipeline
from steps.load_data import load_and_split_data
from steps.train_model import train_and_evaluate_model

@pipeline
def fraud_detection_training_pipeline():
    """Defines the full MLOps pipeline for training the fraud model."""
    
    # 1. Load, validate, and split the data
    X_train, X_test, y_train, y_test = load_and_split_data()
    
    # 2. Preprocess, train, evaluate, and track the model
    pipeline_model = train_and_evaluate_model(
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test
    )
