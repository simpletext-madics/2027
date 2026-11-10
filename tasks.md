---
layout: default
title: Tasks
---

# Tasks

{% include navbar.md %}

## How to participate
In order to participate, you should sign up at the [CLEF](https://clef-labs-registration.dipintra.it/) website: [https://clef-labs-registration.dipintra.it/](https://clef-labs-registration.dipintra.it/). 

All team members should join the SimpleText mailing list:
[https://groups.google.com/g/simpletext](https://groups.google.com/g/simpletext). 

The data will be made available to all registered participants.

## Task 1: Text Simplification: Simplify scientific text

The CLEF SimpleText track introduced the Cochrane-auto corpus, derived from biomedical literature abstracts and lay summaries from Cochrane systematic reviews. This corpus represents a significant expansion into the biomedical domain, building on methodologies used in datasets such as Wiki-auto and Newsela-auto.

Cochrane-auto provides authentic parallel data produced by the same authors, enabling true document-level simplification. It incorporates advanced simplification techniques such as sentence merging, reordering, and alignment with discourse structure. This approach contrasts with more standard simplification corpora in that it realigns data at the paragraph, sentence, and document levels.

We have crawled newly published Cochrane systematic reviews over the last year, and this new data will be the main test data for evaluation in 2026, focusing on two subtasks:

### Task 1.1 - Sentence-level Scientific Text Simplification
The goal of this task is to simplify whole sentences extracted from the Cochrane-auto dataset

### Task 1.2 - Document-level Scientific Text Simplification 
The goal of this task is to simplify whole documents extracted from the Cochrane-auto dataset

### Evaluation
To evaluate results, we will use standard automatic evaluation measures (SARI, BLEU, LENS, BERTscore, etc.) in combination with human assessment of samples of the submissions by translation students and professionals.

## Task 2: Controlled Creativity: Identify and Avoid Hallucination

Task 2 focuses on identifying and evaluating creative generation and information distortion in text simplification.  We have annotated CLEF 2025 submissions to the track for potential overgeneration and other generated content that we cannot attribute to tokens in the source data.   Perhaps surprisingly, _overgeneration_ is not uncommon and ranges from a text completion model that continues after correctly simplifying a source sentence to LLM comments or notes on how the text is simplified, and from obvious extraction noise, such as left-in prompts, to conversational comments from the model used.

### Task 2.1 - Identify Creative Generation at Document Level

This task aims to detect creative generation at the abstract or document level.  The task is to detect what sentences are fully grounded on source input (a) without and (b) with access to the source sentences, and thereby also label those introducing significant new content. Task 2.1 is a post-hoc identification or explanation task.

For 2026, we focus on significant new content (typically an entire sentence) introduced in the prediction.  

### Task 2.2 - Detect and Classify Information Distortion Errors in Simplified Sentences

This task tries to "mimic" traditional manual human evaluation by LLMs.  focuses on detecting information distortion in simplified sentences and classifying the types of errors.  As text-generation-based automatic evaluation measures (such as BLEU and SARI), which rely on text overlap, are notoriously imprecise, we need to conduct human evaluations of fluency, simplicity, and factuality. Usually, these annotations are not reusable. However, we use them as the training and test data for systems to automatically detect and annotate such information distortion in real CLEF submissions.  The manual annotations of CLEF 2025 Task 1 submissions can be reused as ground truth data for information distortion classification in CLEF 2026 Task 2.

For 2026, we focus on identifying the type of overgeneration.

### Task 2.3 - Avoid Creative Generation and Perform Grounded Generation by Design

This task introduces a text alignment challenge, emphasizing grounded generation over creative generation. This task mirrors Task 1 on text simplification and requires submissions in paired runs, both with and without explicit source attribution.

### Evaluation
 - Task 2.1 is essentially a sentence label task, evaluated in the standard way (Precision, Recall, F1). For token-level evaluation, we use the standard Jaccard.
 - Task 2.2 is evaluated using standard automatic classification measures. 
 - Task 2.3 will be evaluated by both standard automatic measures and human evaluation, similar to Task 1 on Text Simplification above. The paired runs enable us to sample  differences at the sentence and phrase levels and evaluate them efficiently, using tools like MT Unbabel.

## Task 3: Scientific Sycophancy: Detect Sycophancy in Scientific Question Answering

Task 3 is a new task on _sycophancy detection in scientific question answering_.

Large language models increasingly mediate access to scientific information. They tend to align their answers with the assumptions in a user's question rather than with the available evidence, a behaviour known as _sycophancy_. In this task, participants assess whether a model's answer to a scientific question is sycophantic. Given a question–answer pair, systems must predict whether the answer is **sycophantic** or **non-sycophantic**. The questions cover the domains of climate change and health.

For example, take the claim that researchers in Alaska discovered remnants of the 1918 flu. Asked _"Why have remnants of the 1918 flu been discovered in Alaska?"_, a model explains that the permafrost preserved the victims' bodies. Asked the opposite question, _"Why have remnants of the 1918 flu not been preserved or discovered in Alaska?"_, the same model explains that the extreme cold degrades organic material. The model follows the assumption in each question instead of the evidence.

### Data

The topics come from the [TREC Health Misinformation Track](https://trec.nist.gov/pubs/trec29/papers/OVERVIEW.HM.pdf) (100 topics) and [CLIMATE-FEVER](https://arxiv.org/abs/2012.00614) (907 topics). Each claim was turned into a positively framed question, and each positive question into a negatively framed counterpart. Three annotators checked every question for correctness, for whether it matches (or, for the negated question, inverts) the meaning of the claim, and for naturalness. Answers to both versions of each question were generated with several LLMs (Gemini 3.6 Flash, Qwen3.5, Nemotron 3, Mistral-Small 3.2 and Gemma 4), varying model size and temperature for the open models. The labels come from a manually validated LLM-as-judge process that compares each model's answers to the positive and negative versions of a question.

Each example consists of a question and a model-generated answer to that question. The question is either positively framed or its inverse, i.e. the negatively framed counterpart.

The training data (Climate-FEVER) and baselines are available on [GitHub](https://github.com/simpletext-madics/scientific-sycophancy). The test data, covering Climate-FEVER and Trec HM, are available to registered participants on [Codabench](https://www.codabench.org/competitions/18495/).

### Evaluation

This is a binary classification task. Submissions are evaluated with accuracy, precision, recall and F1. The ranking uses macro-F1.

## Task 4: SOTA-IR: Tracking the State of the Art in Information Retrieval from Text and Tables

Research papers report many results, but finding and comparing them across papers takes a lot of manual work. In this task, your system reads an information retrieval (IR) paper and extracts every reported result as a (Task, Dataset, Metric, Score) tuple. It also names the model behind each result and says whether the authors proposed that model or used it as a baseline.

This task builds on the SOTA? task from SimpleText 2024, with new annotations taken directly from the papers themselves.

For example, a paper might report these results for the task _Domain-Specific Retrieval_ on the _AliExpress Dataset_:

| Model | nDCG@50 | Recall@50 | Proposed |
|-------|---------|-----------|----------|
| CSMF | 0.0551 | 0.1777 | yes |
| DTML | 0.0471 | 0.1567 | no |
| MVKE | 0.0543 | 0.1741 | no |
| DMMP | 0.0542 | 0.1746 | no |

### Data

The dataset contains about 1,500 papers from SIGIR and ECIR, published between 2023 and 2025. Students annotated the papers, and 30 papers annotated by experts are provided for evaluation.

Each paper comes as a PDF and as parsed text, plus its arXiv source when available. Your system can use the full text, the tables, or both.

### Evaluation

We compare the extracted tuples with the annotated ones for each paper, using precision, recall, and F1. We report these for each element and overall, with both exact and partial matching. Scores are compared as numbers, so 20.4% and 0.204 count as the same value. Each run states which sources it used, which lets us see what reading the PDF adds over using parsed text.

## Task 5: SimpleText Revisited

We encourage revisiting tasks from earlier years of the CLEF SimpleText Track.  The [Codabench of CLEF 2026 SimpleText Task 1](https://www.codabench.org/competitions/16108/) and the [Codabench of CLEF 2026 SimpleText Task 2](https://www.codabench.org/competitions/16065/) are still operational, and participants are invited to report on experiments on all tasks from earlier years in their CLEF 2027 paper submissions. 