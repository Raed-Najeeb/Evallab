
# EvalLab: Evaluation Framework for Evidence-Grounded AI Systems

## Objective

Build an AI research assistant and a separate evaluation framework
to measure its quality, diagnose failures, and assess whether
engineering changes genuinely improve performance.

The primary learning objective is AI evaluation engineering.

## System Under Test

The research assistant will:

- Retrieve relevant passages from AI/ML research papers.
- Generate answers grounded in retrieved evidence.
- Provide citations linked to source passages.
- Abstain when sufficient evidence is unavailable.
- Handle conflicting evidence explicitly.

## Evaluation Framework

The framework will progressively measure:

- Retrieval quality
- Factual correctness
- Evidence support
- Citation quality
- Abstention reliability
- Failure categories and regression across versions

## Development Principles

- Implement incrementally and verify each component.
- Keep the evaluation framework separate from the system under test.
- Use reference annotations to evaluate system outputs.
- Report individual metrics rather than relying only on one aggregate score.
- Make experiments reproducible.
- Validate automated evaluators before trusting their judgments.

## Current Status

Phase 1: Problem definition and system design.
