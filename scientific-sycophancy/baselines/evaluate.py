"""
Evaluate the LLM-as-a-judge experiments on a labelled file (e.g. the training data).
  - simple question: the judgement of each question-answer pair (Yes = sycophantic);
  - reconstruction: sycophantic if the two judgements of the question differ.
Predictions that are Other are left out of the scores (and counted).

Inputs:  the labelled file, results/simple_question_<name>.csv and results/reco_{with,without}_examples_<name>.csv
Output:  results/llm_judge_<name>.csv (one row per experiment)
Run:     python -m baselines.evaluate data/train.csv.gz
"""

import sys
from pathlib import Path
import pandas as pd
from baselines.common import ROOT, scores, sycophancy

input_file = Path(sys.argv[1])
name = input_file.name.split(".")[0]
results_dir = ROOT / "results"
labels = {"Yes": "sycophantic", "No": "non-sycophantic"}

data = pd.read_csv(input_file)

experiments = {}
if (results_dir / f"simple_question_{name}.csv").exists():
    experiments["simple_question"] = pd.read_csv(results_dir / f"simple_question_{name}.csv")["judge"]
for variant in ("with_examples", "without_examples"):
    file = results_dir / f"reco_{variant}_{name}.csv"
    if file.exists():
        reco = pd.read_csv(file)
        reco["pred"] = [sycophancy(j, ji) for j, ji in zip(reco["judge"], reco["judge_inv"])]
        experiments[f"reco_{variant}"] = data[["question"]].merge(reco[["q_given", "pred"]], left_on="question", right_on="q_given", how="left", validate="many_to_one")["pred"]

summary = []
for method, pred in experiments.items():
    valid = pred.isin(["Yes", "No"]).values
    summary.append({"method": method, "n": int(valid.sum()), "n_left_out": int((~valid).sum()), **scores(data["label"][valid], pred[valid].map(labels))})

pd.DataFrame(summary).to_csv(results_dir / f"llm_judge_{name}.csv", index=False)
