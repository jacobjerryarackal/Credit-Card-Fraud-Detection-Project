from typing import List, Optional
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder

def get_preprocessor(numeric_features: Optional[List[str]] = None, 
                     categorical_features: Optional[List[str]] = None) -> Pipeline:
    """Builds the scikit-learn preprocessing pipeline."""
    
    # Defaults based on our EDA
    if numeric_features is None:
        numeric_features = [
            'hour_of_day', 'day_of_week', 'is_weekend', 'amount_usd', 
            'is_foreign_transaction', 'distance_from_home_km', 'card_present', 
            'chip_used', 'pin_used', 'billing_address_match', 'cvv_match', 
            'transactions_last_1h', 'transactions_last_24h', 
            'avg_transaction_amount_last_30d', 'amount_vs_avg_ratio', 
            'days_since_last_transaction', 'customer_age_years', 'account_age_days', 
            'is_new_merchant', 'velocity_flag'
        ]
        
    if categorical_features is None:
        categorical_features = ['merchant_category', 'merchant_country']

    # Numeric pipeline: Impute missing with median, then scale robustly
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', RobustScaler())
    ])

    # Categorical pipeline: Impute missing with mode, then one-hot encode
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Combine them using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='drop'  # This automatically drops transaction_id and transaction_datetime
    )

    return Pipeline(steps=[('preprocessor', preprocessor)])
