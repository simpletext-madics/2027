"""
TF-IDF + logistic regression / linear SVM.

Input:  data/train.csv.gz
Output: results/tfidf.csv
Run:    python -m baselines.tfidf
"""

import pandas as pd
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from baselines.common import N_FOLDS, SEED, load_train, save, scores

classifiers = {
    "tfidf_logreg": lambda: LogisticRegression(max_iter=1000),
    "tfidf_svm": lambda: LinearSVC(random_state=SEED),
}

def features(fit: pd.DataFrame, *transform: pd.DataFrame) -> list:
    q_vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True).fit(fit["question"])
    a_vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True).fit(fit["answer"])
    return [hstack([q_vec.transform(df["question"]), a_vec.transform(df["answer"])]).tocsr() for df in (fit, *transform)]

train = load_train()

rows = []
for fold in range(N_FOLDS):
    fit, val = train[train["fold"] != fold], train[train["fold"] == fold]
    X_fit, X_val = features(fit, val)
    for name, make in classifiers.items():
        clf = make().fit(X_fit, fit["label"])
        rows.append({"classifier": name, "fold": fold, **scores(val["label"], clf.predict(X_val))})
save(rows, "tfidf")
