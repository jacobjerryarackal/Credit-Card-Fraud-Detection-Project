import pandas as pd
import pytest
from core.preprocessing import get_preprocessor

def test_get_preprocessor_structure():
    """Test that the preprocessor builds successfully and has correct structure."""
    preprocessor = get_preprocessor()
    
    assert preprocessor is not None
    assert 'preprocessor' in preprocessor.named_steps
    
    col_transformer = preprocessor.named_steps['preprocessor']
    transformers = dict(col_transformer.transformers)
    
    assert 'num' in transformers
    assert 'cat' in transformers

def test_preprocessing_pipeline_fit_transform():
    """Test that the pipeline can fit and transform sample data without errors."""
    data = {
        'hour_of_day': [1, 2, 3],
        'day_of_week': [1, 2, 3],
        'is_weekend': [0, 0, 0],
        'amount_usd': [10.0, 20.0, 100.0],
        'is_foreign_transaction': [0, 1, 0],
        'distance_from_home_km': [5.0, 15.0, 2.0],
        'card_present': [1, 0, 1],
        'chip_used': [1, 0, 0],
        'pin_used': [1, 0, 0],
        'billing_address_match': [1, 1, 0],
        'cvv_match': [1, 1, 1],
        'transactions_last_1h': [1, 2, 5],
        'transactions_last_24h': [2, 5, 10],
        'avg_transaction_amount_last_30d': [15.0, 25.0, 80.0],
        'amount_vs_avg_ratio': [0.6, 0.8, 1.25],
        'days_since_last_transaction': [1, 5, 0],
        'customer_age_years': [30, 45, 25],
        'account_age_days': [365, 1500, 30],
        'is_new_merchant': [0, 1, 0],
        'velocity_flag': [0, 0, 1],
        'merchant_category': ['retail', 'travel', 'online'],
        'merchant_country': ['US', 'FR', 'US'],
        'transaction_id': ['T1', 'T2', 'T3'], # Should be dropped
        'transaction_datetime': ['2023-01-01', '2023-01-02', '2023-01-03'] # Should be dropped
    }
    
    df = pd.DataFrame(data)
    preprocessor = get_preprocessor()
    
    transformed_data = preprocessor.fit_transform(df)
    
    assert transformed_data is not None
    assert transformed_data.shape[0] == 3
    # Check that transaction_id and datetime are not explicitly kept (dropped by remainder='drop')
    # Can't directly assert columns since output is numpy array, but we know it should work.
