"""Split markdown documents into retrievable passages (chunks).

Strategy: split each document at its markdown headings so every chunk
belongs to a named section, then break oversized sections into
paragraph groups of at most ``max_chars`` characters. Each chunk keeps
its document name and section heading — that's what makes citations
possible later.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


@dataclass
class Chunk:
    id: int
    document: str
    section: str
    text: str


def _split_long_text(text: str, max_chars: int) -> list[str]:
    """Greedily group paragraphs into pieces of at most ``max_chars``."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    pieces: list[str] = []
    current = ""
    for para in paragraphs:
        if current and len(current) + len(para) + 1 > max_chars:
            pieces.append(current)
            current = para
        else:
            current = f"{current}\n{para}" if current else para
        # A single paragraph longer than the cap becomes its own chunk.
        while len(current) > max_chars:
            pieces.append(current[:max_chars])
            current = current[max_chars:]
    if current:
        pieces.append(current)
    return pieces


def chunk_document(document: str, markdown: str, max_chars: int = 900) -> list[Chunk]:
    """Split one markdown document into section-aware chunks."""
    sections: list[tuple[str, str]] = []
    current_title = "(introduction)"
    buffer: list[str] = []

    def flush() -> None:
        body = "\n".join(buffer).strip()
        if body:
            sections.append((current_title, body))

    for line in markdown.splitlines():
        match = _HEADING.match(line)
        if match:
            flush()
            buffer = []
            current_title = match.group(2).strip()
        else:
            buffer.append(line)
    flush()

    chunks: list[Chunk] = []
    for title, body in sections:
        for piece in _split_long_text(body, max_chars):
            chunks.append(
                Chunk(id=len(chunks), document=document, section=title, text=piece)
            )
    return chunks
