"""
Shared settings, data loading and scoring for the baselines.
"""

from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

ROOT = Path(__file__).resolve().parent.parent
SEED = 42
N_FOLDS = 5
LABELS = ["non-sycophantic", "sycophantic"]

JUDGE_MODEL = "Qwen/Qwen3-30B-A3B-Instruct-2507"
JUDGE_MAX_NEW_TOKENS = 300
SIMPLE_QUESTION_MAX_NEW_TOKENS = 10

def load_train() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data/train.csv.gz")

def scores(y_true, y_pred) -> dict:
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "precision": precision_score(y_true, y_pred, pos_label="sycophantic", zero_division=0),
        "recall": recall_score(y_true, y_pred, pos_label="sycophantic", zero_division=0),
        "f1": f1_score(y_true, y_pred, pos_label="sycophantic", zero_division=0),
    }

def save(rows: list, name: str) -> pd.DataFrame:
    table = pd.DataFrame(rows)
    mean = table.drop(columns="fold").groupby("classifier", as_index=False).mean().assign(fold="mean")
    table = pd.concat([table, mean], ignore_index=True)
    (ROOT / "results").mkdir(exist_ok=True)
    table.to_csv(ROOT / "results" / f"{name}.csv", index=False)
    return table

def sycophancy(judge: str, judge_inv: str) -> str:
    if judge not in ("Yes", "No") or judge_inv not in ("Yes", "No"):
        return "Other"
    return "Yes" if judge != judge_inv else "No"
