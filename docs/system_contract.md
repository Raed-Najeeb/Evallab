
# System Under Test: Input/Output Contract

## 1. Purpose

The system answers questions about AI/ML research papers using
retrieved evidence. It should provide citations, abstain when
evidence is insufficient, and handle conflicting evidence explicitly.

## 2. Input

Each request contains:

- `question_id`: a unique identifier for the question.
- `question`: the user's research question.

## 3. Output

Each response contains:

- `question_id`: the identifier of the original question.
- `answer`: the generated answer.
- `abstained`: whether the system abstained.
- `citations`: references to supporting source passages.
- `retrieved_passages`: passages returned by retrieval, including
  their document IDs, passage IDs, text, and ranking information.

## 4. Evidence Traceability

Every retrieved passage must have a stable document ID and passage ID.
Every citation must be resolvable to an actual source passage.

## 5. Required Behaviors

- Answer when the corpus provides sufficient evidence.
- Abstain when the corpus does not provide sufficient evidence.
- Identify material conflicts in the available evidence.
- Avoid presenting unsupported claims as established facts.

## 6. Evaluation Requirements

The output must preserve enough information to evaluate retrieval,
factual correctness, evidence support, citation validity, and abstention.

## 7. Open Decisions

- Exact JSON schema and validation rules.
- How claims will be represented and matched to citations.
- How conflicting evidence will be represented.
- How abstention reasons will be recorded.


## 8. Citation Requirements

Citation evaluation must distinguish:

- **Citation validity:** Whether a citation resolves to an existing
  document and passage.
- **Citation support:** Whether the cited passage supports the
  specific claim associated with that citation.

A valid citation is not automatically a supporting citation.
Both properties must be evaluated separately.


## 9. Response Structure

The response will contain the following top-level fields:

- `question_id`: identifier of the input question.
- `answer`: complete answer text shown to the user.
- `abstained`: boolean indicating whether the system abstained.
- `abstention_reason`: explanation of why the system abstained, or null.
- `claims`: list of atomic factual claims made in the answer.
- `citations`: list of citation records linked to claims.
- `retrieved_passages`: ordered list of passages returned by retrieval.

Each claim must have a stable claim ID and its claim text.

Each citation must identify the document and passage it references,
and the claim or claims it is intended to support.

Each retrieved passage must include its document ID, passage ID,
text, and retrieval rank.

The schema must allow an answer to contain multiple claims and
multiple citations, including claims with no citations.

## 10. Abstention and Conflict Handling

Abstention must be represented explicitly rather than inferred only
from the answer text.

A response must distinguish between:

- Insufficient evidence in the corpus.
- Conflicting evidence in the corpus.
- Other failures that prevent a reliable answer.

Conflicting evidence must not automatically be treated as
unanswerable. The system should identify material conflicts when
the available sources disagree.
