import pandas as pd
from zenml import step
from typing_extensions import Annotated

@step
def load_batch_data(file_path: str = "credit_card_fraud_dataset.csv") -> Annotated[pd.DataFrame, "batch_data"]:
    """Loads unlabelled batch data for inference (simulates dropping target)."""
    df = pd.read_csv(file_path)
    
    # In production, inference data doesn't have the target label. We drop it here to simulate that.
    if 'is_fraud' in df.columns:
        df = df.drop(columns=['is_fraud'])
        
    # We sample 100 rows to simulate a micro-batch
    batch = df.sample(100, random_state=42)
    return batch
