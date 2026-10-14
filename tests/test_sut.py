from evallab.schemas import SUTRequest
from evallab.sut import answer_question


def test_answer_question_returns_evidence_and_citations():
    response = answer_question(
        SUTRequest(
            question_id="q001",
            question="How does retrieval-augmented generation use external evidence?",
        )
    )

    assert response.question_id == "q001"
    assert not response.abstained
    assert response.retrieved_passages
    assert response.claims
    assert response.citations

    retrieved_ids = {
        (passage.document_id, passage.passage_id)
        for passage in response.retrieved_passages
    }

    for citation in response.citations:
        assert (citation.document_id, citation.passage_id) in retrieved_ids


def test_answer_question_abstains_when_nothing_matches():
    response = answer_question(
        SUTRequest(
            question_id="q002",
            question="What is the history of ancient Roman architecture?",
        )
    )

    assert response.abstained
    assert response.abstention_reason == "insufficient_evidence"
    assert response.retrieved_passages == []
    assert response.citations == []