import subprocess
from pipelines.training_pipeline import fraud_detection_training_pipeline

def setup_zenml_stack():
    """Ensures the ZenML stack has MLflow configured for our local run."""
    print("Setting up ZenML stack with MLflow...")
    
    # 1. Register MLflow experiment tracker (ignore errors if it already exists)
    subprocess.run(
        ["zenml", "experiment-tracker", "register", "mlflow_tracker", "--flavor=mlflow"],
        capture_output=True
    )
    
    # 2. Register a new stack that includes the default local orchestrator, artifact store, and MLflow
    subprocess.run(
        ["zenml", "stack", "register", "fraud_stack", 
         "-a", "default", 
         "-o", "default", 
         "-e", "mlflow_tracker"],
        capture_output=True
    )
    
    # 3. Set our custom stack as the active stack
    subprocess.run(["zenml", "stack", "set", "fraud_stack"], capture_output=True)
    print("ZenML stack 'fraud_stack' is active.\n")

if __name__ == "__main__":
    print("Starting Fraud Detection Training Pipeline...")
    
    setup_zenml_stack()
    
    # Execute the pipeline
    fraud_detection_training_pipeline()
    
    print("\n✅ Pipeline execution completed successfully!")
    print("To view your experiment results, run this command in your terminal: mlflow ui")
