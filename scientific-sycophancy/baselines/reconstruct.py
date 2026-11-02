"""
LLM as a judge by reconstruction: the judge model is given a question and generates, in one answer, the answer, its
judgement, the inverse question, the inverse answer and the inverse judgement.

Input:  one CSV file with the column question, e.g. data/train.csv.gz and baselines/prompts/<variant>.txt
Output: results/reco_<variant>_<input file name>.csv
Run:    python -m baselines.reconstruct <with_examples|without_examples> data/train.csv.gz
"""

import json
import sys
from pathlib import Path
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
from baselines.common import JUDGE_MAX_NEW_TOKENS, JUDGE_MODEL, ROOT

variant = sys.argv[1]
input_file = Path(sys.argv[2])
prompt = open(ROOT / "baselines/prompts" / f"{variant}.txt", encoding="utf-8").read()
output_file = ROOT / "results" / f"reco_{variant}_{input_file.name.split('.')[0]}.csv"

model = AutoModelForCausalLM.from_pretrained(JUDGE_MODEL, dtype="auto", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(JUDGE_MODEL)

def parse(content: str) -> list:
    try:
        result = json.loads(content)
        if isinstance(result, list) and len(result) == 5:
            return result
    except json.JSONDecodeError:
        pass
    return [content, "Other", None, None, "Other"]

def reconstruct(question: str) -> list:
    text = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt.format(question=question)}],
        tokenize=False,
        add_generation_prompt=True,
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generated_ids = model.generate(**model_inputs, max_new_tokens=JUDGE_MAX_NEW_TOKENS, do_sample=False)
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):]
    return parse(tokenizer.decode(output_ids, skip_special_tokens=True).strip())

questions = pd.read_csv(input_file)["question"].unique()

rows = []
for question in questions:
    a_generated, judge, q_inv_generated, a_inv_generated, judge_inv = reconstruct(question)
    rows.append({
        "q_given": question,
        "a_generated": a_generated,
        "judge": judge,
        "q_inv_generated": q_inv_generated,
        "a_inv_generated": a_inv_generated,
        "judge_inv": judge_inv,
    })

output_file.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(output_file, index=False)
