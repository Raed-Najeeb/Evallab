
import pytest

from evallab.metrics import (
    abstention_correct,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_recall_at_k():
    assert recall_at_k(
        ["p1", "p2"],
        ["p1"],
        2,
    ) == 1.0


def test_precision_at_k():
    assert precision_at_k(
        ["p1", "p2"],
        ["p1"],
        2,
    ) == 0.5


def test_reciprocal_rank():
    assert reciprocal_rank(
        ["p2", "p1"],
        ["p1"],
    ) == 0.5


def test_reciprocal_rank_returns_zero_when_no_relevant_passage_is_retrieved():
    assert reciprocal_rank(
        ["p2", "p3"],
        ["p1"],
    ) == 0.0


def test_recall_returns_zero_for_empty_relevant_set():
    assert recall_at_k(
        ["p1", "p2"],
        [],
        2,
    ) == 0.0


def test_precision_rejects_non_positive_k():
    with pytest.raises(ValueError):
        precision_at_k(["p1"], ["p1"], 0)


def test_abstention_correct():
    assert abstention_correct(True, True) == 1.0
    assert abstention_correct(False, True) == 0.0
