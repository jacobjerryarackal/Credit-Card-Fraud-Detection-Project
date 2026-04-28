from zenml import pipeline, step
from zenml.client import Client
from sklearn.pipeline import Pipeline
from steps.predict import predict_fraud
from steps.load_batch import load_batch_data

@step
def load_latest_model() -> Pipeline:
    """Loads the model pipeline from the latest successful training run."""
    client = Client()
    # Get the latest run of the training pipeline
    pipeline_model = client.get_pipeline("fraud_detection_training_pipeline")
    latest_run = pipeline_model.last_run
    
    # Extract the exact sklearn pipeline artifact that was output by the train step
    model_artifact = latest_run.steps["train_and_evaluate_model"].outputs["output"]
    return model_artifact.load()

@pipeline
def fraud_detection_inference_pipeline():
    """Defines the batch inference pipeline."""
    # 1. Load latest trained model (including preprocessing)
    model = load_latest_model()
    
    # 2. Load incoming batch data
    batch_data = load_batch_data()
    
    # 3. Predict fraud probabilities
    predictions = predict_fraud(model_pipeline=model, batch_data=batch_data)
