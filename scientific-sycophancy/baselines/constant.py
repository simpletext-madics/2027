"""
Constant baselines: always predict sycophantic and always predict non-sycophantic, scored on each validation fold.
Input:  data/train.csv.gz
Output: results/constant.csv
Run:    python -m baselines.constant
"""

from baselines.common import LABELS, N_FOLDS, load_train, save, scores

train = load_train()

rows = []
for fold in range(N_FOLDS):
    val = train[train["fold"] == fold]
    for label in LABELS:
        rows.append({"classifier": f"always_{label}", "fold": fold, **scores(val["label"], [label] * len(val))})
save(rows, "constant")
