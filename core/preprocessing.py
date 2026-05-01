from typing import List, Optional
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder

from core.config import DEFAULT_NUMERIC_FEATURES, DEFAULT_CATEGORICAL_FEATURES

def get_preprocessor(numeric_features: Optional[List[str]] = None, 
                     categorical_features: Optional[List[str]] = None) -> Pipeline:
    """Builds the scikit-learn preprocessing pipeline."""
    
    # Defaults based on our config
    if numeric_features is None:
        numeric_features = DEFAULT_NUMERIC_FEATURES
        
    if categorical_features is None:
        categorical_features = DEFAULT_CATEGORICAL_FEATURES

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
