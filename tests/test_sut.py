
from evallab.schemas import EvaluationCase, Passage
from evallab.sut import SimpleSUT


def test_sut_retrieves_matching_passage_and_cites_it():
    corpus = [
        Passage(
            passage_id="doc1/p1",
            text="Dense retrieval represents documents as vectors.",
        ),
        Passage(
            passage_id="doc2/p1",
            text="Cooking pasta requires boiling water.",
        ),
    ]
    sut = SimpleSUT(corpus)
    case = EvaluationCase(
        question_id="eval001",
        question="How does dense retrieval represent documents?",
        relevant_passage_ids=["doc1/p1"],
        should_abstain=False,
    )

    response = sut.answer(case)

    assert "doc1/p1" in response.retrieved_passage_ids
    assert response.citations == ["doc1/p1"]
    assert response.abstained is False


def test_sut_abstains_when_no_passage_matches():
    corpus = [
        Passage(
            passage_id="doc1/p1",
            text="Cooking pasta requires boiling water.",
        )
    ]
    sut = SimpleSUT(corpus)
    case = EvaluationCase(
        question_id="eval002",
        question="How do black holes evaporate?",
        relevant_passage_ids=[],
        should_abstain=True,
    )

    response = sut.answer(case)

    assert response.retrieved_passage_ids == []
    assert response.abstained is True
    assert response.citations == []
