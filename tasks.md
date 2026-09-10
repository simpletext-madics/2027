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

## Task 3: Research Area Classification

Task 3 is a new task that asks for the _classification of scientific articles by research area._

The task promotes the development of automatic methods for classifying scientific articles using a given taxonomy.  This greatly extends the scope of traditional subject classification and can accelerate the adoption of consistent metadata across collections (arXiv, Openaire, MADOC), as well as facilitate consistent reporting and monitoring of research output and impact.  In 2026, we focus on the [DFG subject classification](https://www.dfg.de/resource/blob/331950/fachsystematik-2024-2028-en.pdf)  as the target classification.

### Data 

For datasets, we will use scientific publications crawled from arXiv. arXiv has provided open access to scholarly articles across disciplines such as physics, computer science, mathematics, and economics. The collected dataset is further annotated by DFG subject classification.

### Evaluation

LLMs might produce some “near misses” with their results when, for instance, a research area like “Computer Science & Engineering” might be predicted as just “Computer Science”. To overcome these challenges, we used several approaches to determine the actual matches:

- *Exact Match (EM)*: a binary measure comparing the output of the model directly with the ground truth.
- *String Distance (SD)*: a normalized Levenshtein distance between the prediction and reference.
- *Embedding Distance (ED)*: a semantic similarity measure based on the BERT-embeddings of the prediction and reference.

The evaluation will focus on EM-accuracy as the main overall performance measure.

## Task 4: SimpleText Revisited

We encourage revisiting tasks from earlier years of the CLEF SimpleText Track.  The [Codabench of CLEF 2025 SimpleText Task 1](https://www.codabench.org/competitions/8400/) and the [Codabench of CLEF 2025 SimpleText Task 2](https://www.codabench.org/competitions/8327/) are still operational, and participants are invited to report on experiments on all tasks from earlier years in their CLEF 2026 paper submissions. 
