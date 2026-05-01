import pandas as pd
from typing_extensions import Tuple, Annotated
from sklearn.model_selection import train_test_split
from zenml import step

from core.validation import validate_fraud_dataset

@step
def load_and_split_data(
    file_path: str = "data/credit_card_fraud_dataset.csv",
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[
    Annotated[pd.DataFrame, "X_train"],
    Annotated[pd.DataFrame, "X_test"],
    Annotated[pd.Series, "y_train"],
    Annotated[pd.Series, "y_test"],
]:
    """Loads the dataset, validates it, and performs a stratified split."""
    # 1. Load data
    df = pd.read_csv(file_path)
    
    # 2. Validate data
    validate_fraud_dataset(df)
    
    # 3. Chronological Sort (to prevent time-based data leakage)
    df = df.sort_values(by='transaction_datetime')
    
    # 4. Separate features and target
    X = df.drop(columns=['is_fraud'])
    y = df['is_fraud']
    
    # 5. Split chronologically (shuffle=False)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=False
    )
    
    print(f"Dataset split into train ({len(X_train)} rows) and test ({len(X_test)} rows).")
    print(f"Training fraud rate: {y_train.mean():.4f}")
    
    return X_train, X_test, y_train, y_test
