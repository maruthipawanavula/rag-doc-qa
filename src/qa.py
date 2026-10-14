"""Answer composition for the RAG pipeline.

This is *extractive* question answering, not generation: the "answer"
is the best-matching passage from the corpus, returned verbatim together
with citations (document + section + score) for every passage used.
If nothing in the corpus is relevant enough, the composer says so
instead of inventing an answer.
"""

from __future__ import annotations

from src.retriever import Retriever

# Below this cosine score, a passage is treated as not relevant.
MIN_SCORE = 0.05


def answer_question(retriever: Retriever, question: str, top_k: int = 3) -> dict:
    results = retriever.search(question, top_k=top_k)
    relevant = [r for r in results if r.score >= MIN_SCORE]

    if not relevant:
        return {
            "question": question,
            "answer": None,
            "message": "No passage in the documentation is relevant to that question.",
            "passages": [],
            "citations": [],
        }

    passages = [
        {
            "document": r.chunk.document,
            "section": r.chunk.section,
            "text": r.chunk.text,
            "score": round(r.score, 4),
        }
        for r in relevant
    ]
    return {
        "question": question,
        "answer": relevant[0].chunk.text,
        "message": "Answer is the best-matching passage, quoted verbatim from the docs.",
        "passages": passages,
        "citations": [
            {"document": p["document"], "section": p["section"], "score": p["score"]}
            for p in passages
        ],
    }
