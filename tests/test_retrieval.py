"""Retrieval tests: known questions must rank the right document first."""

import pytest

from src import qa as qa_module
from src.chunking import chunk_document
from src.corpus import load_documents
from src.retriever import Retriever


@pytest.fixture(scope="module")
def retriever() -> Retriever:
    return Retriever.from_docs_dir()


# (question, expected top document)
KNOWN_QUESTIONS = [
    ("How much does the Pro plan cost per user per month?", "billing-and-plans.md"),
    ("How do I enable two-factor authentication?", "security-and-privacy.md"),
    ("Does Lumen Desk integrate with Slack?", "integrations.md"),
    ("How do I invite my team members and create a workspace?", "getting-started.md"),
    ("Why are my emails not syncing into the inbox?", "troubleshooting.md"),
    ("What is the refund policy if I cancel my plan?", "billing-and-plans.md"),
]


def test_corpus_loads_all_documents():
    documents = load_documents()
    assert len(documents) == 6
    assert all(text.strip() for text in documents.values())


def test_chunking_produces_cited_passages():
    documents = load_documents()
    chunks = []
    for name, markdown in documents.items():
        chunks.extend(chunk_document(name, markdown))
    assert len(chunks) >= 20  # 6 docs, several sections each
    for chunk in chunks:
        assert chunk.document in documents
        assert chunk.section
        assert chunk.text


@pytest.mark.parametrize("question, expected_doc", KNOWN_QUESTIONS)
def test_top_result_is_the_right_document(retriever, question, expected_doc):
    results = retriever.search(question, top_k=3)
    assert results, "search returned nothing"
    assert results[0].chunk.document == expected_doc, (
        question,
        [(r.chunk.document, round(r.score, 3)) for r in results],
    )
    assert results[0].score > 0.1


def test_scores_are_sorted_descending(retriever):
    results = retriever.search("billing invoice refund plan price", top_k=5)
    scores = [r.score for r in results]
    assert scores == sorted(scores, reverse=True)


def test_off_topic_question_gets_no_answer(retriever):
    result = qa_module.answer_question(
        retriever, "What is the airspeed velocity of an unladen swallow?"
    )
    assert result["answer"] is None
    assert result["passages"] == []


def test_answer_carries_citations(retriever):
    result = qa_module.answer_question(retriever, "How much does the Pro plan cost?")
    assert result["answer"] is not None
    assert result["citations"][0]["document"] == "billing-and-plans.md"
    assert "$29" in result["answer"]
