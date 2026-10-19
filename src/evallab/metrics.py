
def recall_at_k(
    retrieved_passage_ids: list[str],
    relevant_passage_ids: list[str],
    k: int,
) -> float:
    if not relevant_passage_ids:
        return 0.0

    retrieved = set(retrieved_passage_ids[:k])
    relevant = set(relevant_passage_ids)

    return len(retrieved & relevant) / len(relevant)


def precision_at_k(
    retrieved_passage_ids: list[str],
    relevant_passage_ids: list[str],
    k: int,
) -> float:
    if k <= 0:
        raise ValueError("k must be greater than zero")

    retrieved = retrieved_passage_ids[:k]
    relevant = set(relevant_passage_ids)

    return sum(passage_id in relevant for passage_id in retrieved) / k


def reciprocal_rank(
    retrieved_passage_ids: list[str],
    relevant_passage_ids: list[str],
) -> float:
    relevant = set(relevant_passage_ids)

    for rank, passage_id in enumerate(retrieved_passage_ids, start=1):
        if passage_id in relevant:
            return 1.0 / rank

    return 0.0


def abstention_correct(
    abstained: bool,
    should_abstain: bool,
) -> float:
    return float(abstained == should_abstain)
