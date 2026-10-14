# RAG Doc Q&A (TF-IDF Retrieval)

A small **retrieval-augmented generation (RAG)** system over a bundled
set of product documents — with one honest twist: there is **no LLM and
no external API**. Retrieval is classic TF-IDF + cosine similarity, and
answers are **extractive**: the best-matching passage is quoted verbatim
together with citations, instead of being generated. No API keys, no
network calls, fully reproducible offline.

By Maruthi Pawan Avula.

## Why build RAG this way?

Most "doc Q&A" demos hide everything behind an LLM API key. This
project implements the retrieval half of RAG — the half that decides
*which* text an answer is grounded in — from first principles:

1. **Load** markdown documents (`src/corpus.py`).
2. **Chunk** them into section-aware passages (`src/chunking.py`).
3. **Index** chunks as TF-IDF vectors (`src/retriever.py`).
4. **Retrieve** the top-k passages for a question by cosine similarity.
5. **Compose** an answer from the best passage, with citations
   (`src/qa.py`). Below a relevance threshold the system answers
   "no relevant passage" instead of making something up — the same
   grounding discipline an LLM-based system needs.

Swapping TF-IDF for a neural embedding model, or the extractive composer
for an LLM, only changes steps 3 and 5; the pipeline shape stays the same.

## Corpus

Six short documents about **Lumen Desk**, a fictional shared-inbox
product (invented for this project): overview, getting started, billing
and plans, integrations, security and privacy, troubleshooting. The
chunker produces **29 passages**, each tagged with its document and
section heading so answers can cite their source.

## An honest engineering note

The first version indexed chunk body text only — and misranked real
questions: *"Why are my emails not syncing?"* matched a getting-started
passage instead of the troubleshooting section whose **heading** is
almost the question verbatim. The fix is a standard retrieval technique,
now implemented and covered by tests: index each chunk together with its
document name and section heading. After the fix, all six known-answer
probe questions in the test suite rank the correct document first.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # runtime deps
pip install -r requirements-dev.txt    # + pytest / httpx for tests

uvicorn app.main:app --port 8000       # serves the API
pytest                                 # 16 tests
```

### Sample requests

```bash
curl localhost:8000/health
# {"status":"ok","documents":["billing-and-plans.md", ...],
#  "document_count":6,"chunks_indexed":29}

curl -X POST localhost:8000/ask -H 'Content-Type: application/json' \
  -d '{"question":"How do I enable two-factor authentication?"}'
# {"question": "...",
#  "answer": "Every user can enable two-factor authentication from ...",
#  "passages": [{"document":"security-and-privacy.md",
#                "section":"Two-factor authentication (2FA)",
#                "text":"...", "score":0.506}],
#  "citations":[{"document":"security-and-privacy.md",
#                "section":"Two-factor authentication (2FA)","score":0.506}]}

curl -X POST localhost:8000/ask -H 'Content-Type: application/json' \
  -d '{"question":"What is the airspeed velocity of an unladen swallow?"}'
# {"answer": null, "passages": [], "citations": [], "message": "No passage ..."}
```

The corpus directory can be overridden with the `DOCS_DIR` environment
variable; `top_k` (1–10) controls how many passages are returned.

## Docker

```bash
docker build -t rag-doc-qa .
docker run -p 8000:8000 rag-doc-qa
```

## Project layout

```
docs/               the bundled corpus (6 markdown documents)
src/corpus.py       loads the markdown corpus
src/chunking.py     heading-aware chunking (passages keep section names)
src/retriever.py    TF-IDF index + cosine-similarity search
src/qa.py           extractive answer composer with citations + threshold
app/main.py         FastAPI app: /health, /ask
tests/              retrieval-ranking tests + API tests (TestClient)
```

## Limitations (stated plainly)

- TF-IDF matches words, not meaning: a question phrased with synonyms
  the docs don't use will rank poorly. Dense embeddings fix that; they
  also add a model download and a heavier runtime.
- Answers are verbatim passages, so they can include markdown syntax
  and may start or end mid-thought at chunk boundaries.
- The corpus is tiny and fictional — this demonstrates the pipeline,
  not a production knowledge base.

## Verification status

Actually executed in the build environment (Python 3.12, scikit-learn
1.9.x, FastAPI 0.143.x): all 16 pytest tests passing, plus a live
`uvicorn` boot checked with `curl` against `/health` and `/ask`. The
Dockerfile is written to standard practice but was **not** built in the
build environment (no Docker daemon available there); its steps mirror
the verified local commands exactly.
