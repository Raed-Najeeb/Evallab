
from evallab.schemas import EvaluationCase, Passage, SUTResponse


class SimpleSUT:
    def __init__(self, corpus: list[Passage]):
        self.corpus = corpus

    def answer(self, case: EvaluationCase) -> SUTResponse:
        question_words = set(case.question.lower().split())

        scored_passages = []

        for passage in self.corpus:
            passage_words = set(passage.text.lower().split())
            score = len(question_words & passage_words)

            if score > 0:
                scored_passages.append((score, passage))

        scored_passages.sort(key=lambda item: item[0], reverse=True)
        retrieved = [passage for _, passage in scored_passages[:2]]

        if not retrieved:
            return SUTResponse(
                answer="I don't have enough evidence to answer that question.",
                retrieved_passage_ids=[],
                citations=[],
                abstained=True,
            )

        return SUTResponse(
            answer=retrieved[0].text,
            retrieved_passage_ids=[p.passage_id for p in retrieved],
            citations=[retrieved[0].passage_id],
            abstained=False,
        )
