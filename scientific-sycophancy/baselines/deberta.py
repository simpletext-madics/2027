"""
Input:  data/train.csv.gz
Output: results/deberta[_weighted].csv
        results/deberta[_weighted]_log_history.json
        checkpoints/deberta[_weighted]/
Run:    python -m baselines.deberta [--weighted]
"""

import json
import sys
import numpy as np
import torch
from transformers import (AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding, Trainer, TrainingArguments, set_seed)
from baselines.common import LABELS, ROOT, SEED, load_train, save, scores

model_name = "microsoft/deberta-v3-base"
max_length = 256
val_fold = 0
weighted = "--weighted" in sys.argv
name = "deberta_weighted" if weighted else "deberta"

set_seed(SEED)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

class PairDataset(torch.utils.data.Dataset):
    def __init__(self, df):
        self.enc = tokenizer(df["question"].tolist(), df["answer"].tolist(), truncation=True, max_length=max_length)
        self.labels = df["label"].map(LABELS.index).tolist()

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, i):
        return {**{k: v[i] for k, v in self.enc.items()}, "labels": self.labels[i]}

def compute_metrics(eval_pred):
    logits, y = eval_pred
    return scores([LABELS[i] for i in y], [LABELS[i] for i in np.argmax(logits, axis=1)])

train = load_train()
fit, val = train[train["fold"] != val_fold], train[train["fold"] == val_fold]

counts = fit["label"].value_counts()
class_weights = torch.tensor([len(fit) / (2 * counts[label]) for label in LABELS], dtype=torch.float32)

def weighted_loss(outputs, y, num_items_in_batch=None):
    return torch.nn.functional.cross_entropy(outputs.logits.float(), y, weight=class_weights.to(y.device))

args = TrainingArguments(
    output_dir=ROOT / "checkpoints" / name,
    seed=SEED,
    learning_rate=2e-5,
    num_train_epochs=2,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=128,
    warmup_steps=0.1,
    bf16=True,
    eval_strategy="steps",
    eval_steps=2000,
    save_steps=2000,
    save_total_limit=2,
    load_best_model_at_end=True,
    metric_for_best_model="macro_f1",
    logging_steps=200,
    dataloader_num_workers=4,
    report_to="none",
)
trainer = Trainer(
    model=model,
    args=args,
    processing_class=tokenizer,
    data_collator=DataCollatorWithPadding(tokenizer),
    train_dataset=PairDataset(fit),
    eval_dataset=PairDataset(val),
    compute_metrics=compute_metrics,
    compute_loss_func=weighted_loss if weighted else None,
)
trainer.train()

logits = trainer.predict(PairDataset(val)).predictions
save([{"classifier": name, "fold": val_fold, **scores(val["label"], [LABELS[i] for i in np.argmax(logits, axis=1)])}], name)
json.dump(trainer.state.log_history, open(ROOT / "results" / f"{name}_log_history.json", "w"), indent=1)
