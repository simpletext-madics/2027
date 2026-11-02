"""
Sentence-BERT embeddings + logistic regression / linear SVM. Needs a GPU.

Input:  data/train.csv.gz
Output: results/sbert.csv
Run:    python -m baselines.sbert
"""

import numpy as np
import pandas as pd
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from transformers import AutoModel, AutoTokenizer
from baselines.common import N_FOLDS, SEED, load_train, save, scores

model_name = "sentence-transformers/all-mpnet-base-v2"
max_length = 256
classifiers = {
    "sbert_logreg": lambda: LogisticRegression(max_iter=1000),
    "sbert_svm": lambda: LinearSVC(random_state=SEED),
}

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to("cuda").eval()

@torch.no_grad()
def embed(texts: list, batch_size: int = 256) -> np.ndarray:
    out = []
    for i in range(0, len(texts), batch_size):
        batch = tokenizer(texts[i:i + batch_size], padding=True, truncation=True, max_length=max_length, return_tensors="pt").to("cuda")
        tokens = model(**batch).last_hidden_state
        mask = batch["attention_mask"].unsqueeze(-1)
        mean = (tokens * mask).sum(1) / mask.sum(1)
        out.append(torch.nn.functional.normalize(mean, dim=1).cpu().numpy())
    return np.concatenate(out)

train = load_train()

texts = pd.Index(pd.unique(pd.concat([train["question"], train["answer"]])))
emb = embed(texts.tolist())
u, v = emb[texts.get_indexer(train["question"])], emb[texts.get_indexer(train["answer"])]
X = np.hstack([u, v, np.abs(u - v), u * v])

rows = []
for fold in range(N_FOLDS):
    is_val = (train["fold"] == fold).values
    for name, make in classifiers.items():
        clf = make().fit(X[~is_val], train["label"][~is_val])
        rows.append({"classifier": name, "fold": fold, **scores(train["label"][is_val], clf.predict(X[is_val]))})
save(rows, "sbert")
