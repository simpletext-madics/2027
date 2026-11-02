"""
LLM as a judge by a simple question: the judge model gets one question-answer pair and is asked directly whether the
answer is sycophantic (Yes/No).

Input:  one CSV file with the columns question and answer, e.g. data/train.csv.gz and  baselines/prompts/simple_question.txt
Output: results/simple_question_<input file name>.csv
Run:    python -m baselines.simple_question data/train.csv.gz
"""

import sys
from pathlib import Path
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
from baselines.common import JUDGE_MODEL, ROOT, SIMPLE_QUESTION_MAX_NEW_TOKENS

input_file = Path(sys.argv[1])
output_file = ROOT / "results" / f"simple_question_{input_file.name.split('.')[0]}.csv"
prompt = open(ROOT / "baselines/prompts/simple_question.txt", encoding="utf-8").read()

model = AutoModelForCausalLM.from_pretrained(JUDGE_MODEL, dtype="auto", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(JUDGE_MODEL)

def reco(question: str, answer: str) -> tuple:
    text = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt.format(question=question, answer=answer)}],
        tokenize=False,
        add_generation_prompt=True,
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generated_ids = model.generate(**model_inputs, max_new_tokens=SIMPLE_QUESTION_MAX_NEW_TOKENS, do_sample=False)
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):]
    content = tokenizer.decode(output_ids, skip_special_tokens=True).strip()
    word = content.strip(" .\"'").capitalize()
    return (word if word in ("Yes", "No") else "Other"), content

df = pd.read_csv(input_file)

rows = []
for row in df.to_dict("records"):
    judge, raw_output = reco(row["question"], row["answer"])
    rows.append({**row, "raw_output": raw_output, "judge": judge})

output_file.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(output_file, index=False)
