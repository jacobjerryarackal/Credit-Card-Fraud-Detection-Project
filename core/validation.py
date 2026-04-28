import pandas as pd

def validate_fraud_dataset(df: pd.DataFrame) -> None:
    """Validates the incoming dataset to ensure schema correctness and data quality."""
    # 1. Target column exists
    assert 'is_fraud' in df.columns, "Validation Failed: Target column 'is_fraud' is missing."
    
    # 2. Target has expected values
    unique_targets = set(df['is_fraud'].unique())
    assert unique_targets.issubset({0, 1}), f"Validation Failed: 'is_fraud' contains unexpected values: {unique_targets}"
    
    # 3. Critical features exist
    critical_features = ['amount_usd', 'merchant_category']
    for feature in critical_features:
        assert feature in df.columns, f"Validation Failed: Critical feature '{feature}' is missing."
        
    # 4. Check for massive missing values (e.g., if a column is >90% missing, upstream is broken)
    null_percentages = df.isnull().mean()
    failing_columns = null_percentages[null_percentages > 0.9].index.tolist()
    assert len(failing_columns) == 0, f"Validation Failed: Columns {failing_columns} have >90% missing values."
    
    print(f"Validation passed for {len(df)} rows.")
