"""TF-IDF retrieval over document chunks.

A classic sparse-retrieval approach: every chunk is embedded as a
TF-IDF vector (word unigrams + bigrams, English stop words removed) and
a question is scored against all chunks with cosine similarity. No
neural embeddings and no external services — the index is built in
memory at startup in well under a second for this corpus size.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.chunking import Chunk, chunk_document
from src.corpus import load_documents


@dataclass
class SearchResult:
    chunk: Chunk
    score: float


class Retriever:
    def __init__(self, chunks: list[Chunk]):
        if not chunks:
            raise ValueError("Cannot build a retriever over zero chunks")
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        # Index each chunk together with its document name and section
        # heading: headings carry strong topical signal ("Plan prices",
        # "Emails are not syncing") that the body text alone may lack.
        index_texts = [
            f"{c.document.removesuffix('.md').replace('-', ' ')} — {c.section}\n{c.text}"
            for c in chunks
        ]
        self.matrix = self.vectorizer.fit_transform(index_texts)

    @classmethod
    def from_docs_dir(cls, directory: str | Path | None = None) -> "Retriever":
        documents = load_documents(directory)
        chunks: list[Chunk] = []
        for name, markdown in documents.items():
            chunks.extend(chunk_document(name, markdown))
        # Re-number ids globally so they are unique across documents.
        for index, chunk in enumerate(chunks):
            chunk.id = index
        return cls(chunks)

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        """Return up to ``top_k`` chunks ranked by cosine similarity."""
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix)[0]
        ranked_indices = np.argsort(scores)[::-1]
        results: list[SearchResult] = []
        for idx in ranked_indices[:top_k]:
            results.append(
                SearchResult(chunk=self.chunks[int(idx)], score=float(scores[idx]))
            )
        return results
