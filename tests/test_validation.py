import pandas as pd
import pytest
from core.validation import validate_fraud_dataset

def test_validate_fraud_dataset_success():
    """Test validation passes on well-formed data."""
    data = {
        'is_fraud': [0, 1, 0],
        'amount_usd': [10.0, 20.0, 30.0],
        'merchant_category': ['retail', 'online', 'travel']
    }
    df = pd.DataFrame(data)
    
    # Should not raise any assertion errors
    validate_fraud_dataset(df)

def test_validate_fraud_dataset_missing_target():
    """Test validation fails when target is missing."""
    data = {
        'amount_usd': [10.0, 20.0, 30.0],
        'merchant_category': ['retail', 'online', 'travel']
    }
    df = pd.DataFrame(data)
    
    with pytest.raises(AssertionError, match="Target column 'is_fraud' is missing."):
        validate_fraud_dataset(df)

def test_validate_fraud_dataset_invalid_target():
    """Test validation fails when target has invalid values."""
    data = {
        'is_fraud': [0, 1, 2], # 2 is invalid
        'amount_usd': [10.0, 20.0, 30.0],
        'merchant_category': ['retail', 'online', 'travel']
    }
    df = pd.DataFrame(data)
    
    with pytest.raises(AssertionError, match="contains unexpected values"):
        validate_fraud_dataset(df)
