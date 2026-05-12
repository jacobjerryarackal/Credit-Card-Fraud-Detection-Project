from zenml import pipeline, step
from zenml.client import Client
from sklearn.pipeline import Pipeline
from steps.predict import predict_fraud
from steps.load_batch import load_batch_data

@step
def load_latest_model() -> Pipeline:
    """Loads the model pipeline from the latest successful training run."""
    client = Client()
    
    try:
        # Get the latest run of the training pipeline
        pipeline_model = client.get_pipeline("fraud_detection_training_pipeline")
        
        if not pipeline_model.runs:
            raise RuntimeError("The training pipeline has no runs.")
            
        latest_run = pipeline_model.last_run
        
        if latest_run.status != "completed":
            print(f"Warning: The latest run status is '{latest_run.status}'. Expected 'completed'.")
            
        # Extract the exact sklearn pipeline artifact that was output by the train step
        model_artifact = latest_run.steps["train_and_evaluate_model"].outputs["output"]
        return model_artifact.load()
        
    except KeyError as e:
        raise RuntimeError(f"Error loading model artifact. Make sure the training pipeline ran successfully. Details: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to load latest model. Have you run 'python run_pipeline.py' yet? Details: {e}")

@pipeline
def fraud_detection_inference_pipeline():
    """Defines the batch inference pipeline."""
    # 1. Load latest trained model (including preprocessing)
    model = load_latest_model()
    
    # 2. Load incoming batch data
    batch_data = load_batch_data()
    
    # 3. Predict fraud probabilities
    predictions = predict_fraud(model_pipeline=model, batch_data=batch_data)
