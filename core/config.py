# core/config.py
from typing import List

# Default feature definitions separated from logic

DEFAULT_NUMERIC_FEATURES: List[str] = [
    'hour_of_day', 'day_of_week', 'is_weekend', 'amount_usd', 
    'is_foreign_transaction', 'distance_from_home_km', 'card_present', 
    'chip_used', 'pin_used', 'billing_address_match', 'cvv_match', 
    'transactions_last_1h', 'transactions_last_24h', 
    'avg_transaction_amount_last_30d', 'amount_vs_avg_ratio', 
    'days_since_last_transaction', 'customer_age_years', 'account_age_days', 
    'is_new_merchant', 'velocity_flag'
]

DEFAULT_CATEGORICAL_FEATURES: List[str] = [
    'merchant_category', 'merchant_country'
]
