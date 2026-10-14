"""Load the bundled markdown corpus from the docs directory."""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_DOCS_DIR = Path("docs")


def docs_dir() -> Path:
    """Corpus location; override with the DOCS_DIR environment variable."""
    return Path(os.environ.get("DOCS_DIR", str(DEFAULT_DOCS_DIR)))


def load_documents(directory: str | Path | None = None) -> dict[str, str]:
    """Return {filename: markdown text} for every .md file in the corpus."""
    directory = Path(directory) if directory is not None else docs_dir()
    documents: dict[str, str] = {}
    for path in sorted(directory.glob("*.md")):
        documents[path.name] = path.read_text(encoding="utf-8")
    return documents
