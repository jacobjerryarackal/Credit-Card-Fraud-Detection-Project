import pandas as pd
from zenml import step
from sklearn.pipeline import Pipeline
from typing_extensions import Annotated

@step
def predict_fraud(
    model_pipeline: Pipeline,
    batch_data: pd.DataFrame
) -> Annotated[pd.Series, "fraud_probabilities"]:
    """Uses the identically-trained pipeline to score a new batch of data."""
    
    print(f"Scoring {len(batch_data)} transactions...")
    
    # Predict probabilities for the positive class (fraud)
    probabilities = model_pipeline.predict_proba(batch_data)[:, 1]
    predictions = pd.Series(probabilities, name="fraud_probability")
    
    # Demo output
    high_risk = (predictions > 0.5).sum()
    print(f"🚨 Found {high_risk} high-risk transactions in this batch.")
    
    return predictions
