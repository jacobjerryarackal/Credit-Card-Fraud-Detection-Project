from typing import Dict
import numpy as np
import pandas as pd
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    roc_auc_score,
)

def evaluate_classification_metrics(y_true: pd.Series, y_pred: np.ndarray, y_pred_proba: np.ndarray) -> Dict[str, float]:
    """Calculates comprehensive classification metrics focusing on the minority (fraud) class."""
    metrics = {
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1_score": f1_score(y_true, y_pred, zero_division=0),
        "pr_auc": average_precision_score(y_true, y_pred_proba),
        "roc_auc": roc_auc_score(y_true, y_pred_proba),
    }
    return metrics
