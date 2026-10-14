"""FastAPI service for documentation Q&A over the bundled corpus.

    uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src import qa as qa_module
from src.retriever import Retriever

app = FastAPI(
    title="Docs Q&A (TF-IDF RAG)",
    description="Extractive question answering over the Lumen Desk sample docs.",
    version="1.0.0",
)

# Index is built once at startup from the docs directory.
RETRIEVER = Retriever.from_docs_dir()


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Natural-language question")
    top_k: int = Field(3, ge=1, le=10, description="Maximum passages to return")


@app.get("/health")
def health() -> dict:
    documents = sorted({chunk.document for chunk in RETRIEVER.chunks})
    return {
        "status": "ok",
        "documents": documents,
        "document_count": len(documents),
        "chunks_indexed": len(RETRIEVER.chunks),
    }


@app.post("/ask")
def ask(request: AskRequest) -> dict:
    return qa_module.answer_question(RETRIEVER, request.question, top_k=request.top_k)
