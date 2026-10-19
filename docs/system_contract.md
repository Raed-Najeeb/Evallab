# System Contract

## Purpose

EvalLab evaluates an AI system that answers questions using a fixed collection of documents.

## System Under Test (SUT)

The SUT must:
- Accept a question.
- Retrieve relevant passages from the available corpus.
- Generate an answer using the retrieved evidence.
- Abstain when the available evidence is insufficient.
- Provide citations that identify the passages supporting its answer.

## Evaluation Framework

The evaluation framework must:
- Use a predefined evaluation dataset.
- Evaluate retrieval quality and answer behavior.
- Check whether the SUT abstains appropriately.
- Calculate metrics consistently across evaluation runs.
- Produce a structured evaluation report.

## Boundaries

- The SUT must not access the evaluation reference answers or expected labels.
- The evaluation framework owns the reference answers, relevance judgments, and expected abstention labels.
- Evaluation results must be calculated independently of the SUT's own claims about its performance.

## Citation Requirements

- Each factual answer must cite the passage or passages supporting its claims.
- Citations must refer to valid passage identifiers in the corpus.
- A citation's presence alone does not prove that the cited passage supports the claim.
- Answers must not present unsupported claims as established facts.
- When evidence is insufficient, the SUT must abstain rather than invent an answer.