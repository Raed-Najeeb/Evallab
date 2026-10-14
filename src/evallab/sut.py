import json
import re
from pathlib import Path

from evallab.schemas import (
    Citation,
    Claim,
    RetrievedPassage,
    SUTRequest,
    SUTResponse,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CORPUS_PATH = PROJECT_ROOT / "data" / "sample_corpus.json"


def load_corpus() -> list[dict]:
    with CORPUS_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"\b[a-zA-Z0-9]+\b", text.lower()))


def retrieve_passages(
    question: str,
    corpus: list[dict],
    top_k: int = 2,
) -> list[dict]:
    question_terms = tokenize(question)

    # Ignore common words that provide little retrieval value.
    stop_words = {"a", "an", "and", "are", "is", "of", "the", "to", "what", "how"}
    question_terms -= stop_words

    scored = []

    for passage in corpus:
        passage_terms = tokenize(passage["text"])
        overlap = question_terms & passage_terms

        if overlap:
            scored.append((len(overlap), passage))

    # Higher keyword overlap first; stable IDs break ties deterministically.
    scored.sort(
        key=lambda item: (
            -item[0],
            item[1]["document_id"],
            item[1]["passage_id"],
        )
    )

    return [passage for _, passage in scored[:top_k]]


def answer_question(request: SUTRequest) -> SUTResponse:
    corpus = load_corpus()
    matches = retrieve_passages(request.question, corpus)

    retrieved = [
        RetrievedPassage(
            document_id=passage["document_id"],
            passage_id=passage["passage_id"],
            text=passage["text"],
            rank=rank,
        )
        for rank, passage in enumerate(matches, start=1)
    ]

    if not retrieved:
        return SUTResponse(
            question_id=request.question_id,
            answer="I could not find relevant evidence in the available corpus.",
            abstained=True,
            abstention_reason="insufficient_evidence",
            claims=[],
            citations=[],
            retrieved_passages=[],
        )

    claims = []
    citations = []

    for index, passage in enumerate(retrieved, start=1):
        claim_id = f"c{index:03d}"

        claims.append(
            Claim(
                claim_id=claim_id,
                text=passage.text,
            )
        )

        citations.append(
            Citation(
                document_id=passage.document_id,
                passage_id=passage.passage_id,
                claim_ids=[claim_id],
            )
        )

    answer = " ".join(claim.text for claim in claims)

    return SUTResponse(
        question_id=request.question_id,
        answer=answer,
        abstained=False,
        abstention_reason=None,
        claims=claims,
        citations=citations,
        retrieved_passages=retrieved,
    )