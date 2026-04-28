# Problem Statement: Credit Card Fraud Detection

## Business Context
Predict which credit card transactions are fraudulent at the time they occur, so the system can block them or flag them for manual review. This will prevent direct financial loss and chargeback fees without excessively frustrating legitimate customers with false declines.

## ML Formulation
- **Problem type**: Binary classification
- **Target variable**: `is_fraud` (1 if fraudulent, 0 if legitimate)
- **Primary metric**: F1-Score / PR-AUC — because we need to explicitly balance the cost of false positives (declining good customers) and false negatives (allowing fraud) on a highly imbalanced dataset.
- **Guardrail metrics**: Precision, Recall, and Inference Latency.
- **Current baseline**: None. The first simple model we build (e.g., Logistic Regression or a Decision Tree) will become our baseline.

## Data Summary
- **Rows**: 50,001
- **Features**: 24 (mixed types including transaction amount, merchant category, time, location distance, etc.)
- **Label availability**: Yes (`is_fraud`)
- **Known issues**: Likely high class imbalance (which we'll verify during EDA).

## Constraints
- **Latency**: Real-time or near real-time (needed to block transactions at the point of sale).
- **Interpretability**: Helpful for fraud analysts during manual review of flagged transactions.

## Framework
- **Orchestration**: ZenML

## Success Criteria
The model is in production when a reliable pipeline automatically ingests data, trains a model that establishes a strong F1-score baseline, and is deployed as an endpoint that can be queried for real-time predictions.
