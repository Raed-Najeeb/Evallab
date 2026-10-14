
import pytest
from pydantic import ValidationError
from evallab.schemas import (
    Claim,
    Citation,
    RetrievedPassage,
    SUTRequest,
)

from evallab.schemas import Claim, SUTRequest


def test_valid_request():
    request = SUTRequest(
        question_id="q001",
        question="What is retrieval-augmented generation?",
    )

    assert request.question_id == "q001"
    assert request.question == "What is retrieval-augmented generation?"


def test_request_rejects_empty_question():
    with pytest.raises(ValidationError):
        SUTRequest(
            question_id="q001",
            question="",
        )


def test_request_rejects_unexpected_fields():
    with pytest.raises(ValidationError):
        SUTRequest(
            question_id="q001",
            question="What is RAG?",
            queston="This is a typo",
        )


def test_valid_claim():
    claim = Claim(
        claim_id="c001",
        text="RAG combines retrieval with generation.",
    )

    assert claim.claim_id == "c001"
    assert "retrieval" in claim.text


def test_claim_rejects_empty_text():
    with pytest.raises(ValidationError):
        Claim(
            claim_id="c001",
            text="",
        )

def test_request_accepts_question_at_maximum_length():
    request = SUTRequest(
        question_id="q001",
        question="a" * 2000,
    )

    assert len(request.question) == 2000


def test_request_rejects_question_over_maximum_length():
    with pytest.raises(ValidationError):
        SUTRequest(
            question_id="q001",
            question="a" * 2001,
        )

def test_valid_citation():
    citation = Citation(
        document_id="paper001",
        passage_id="p003",
        claim_ids=["c001"],
    )

    assert citation.passage_id == "p003"
    assert citation.claim_ids == ["c001"]


def test_valid_retrieved_passage():
    passage = RetrievedPassage(
        document_id="paper001",
        passage_id="p003",
        text="RAG retrieves external evidence before generation.",
        rank=1,
    )

    assert passage.rank == 1
    assert "evidence" in passage.text


def test_retrieved_passage_rejects_invalid_rank():
    with pytest.raises(ValidationError):
        RetrievedPassage(
            document_id="paper001",
            passage_id="p003",
            text="Example passage.",
            rank=0,
        )