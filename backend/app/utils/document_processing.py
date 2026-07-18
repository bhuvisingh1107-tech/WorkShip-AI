"""Deterministic text preparation helpers for future document retrieval workflows."""

import re
from math import ceil
from typing import Any

WORDS_PER_MINUTE = 200
_HEADING_PATTERN = re.compile(r"(?m)^#{1,6}\s+(.+?)\s*$")
_SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+")
_TOKEN_PATTERN = re.compile(r"[a-z0-9]{3,}")
_STOP_WORDS = {
    "about", "after", "against", "and", "are", "for", "from", "into", "its",
    "that", "the", "this", "with", "workship", "technologies",
}


def clean_text(text: str) -> str:
    """Remove control characters while preserving meaningful line boundaries."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return "".join(
        character for character in normalized if character == "\n" or character == "\t" or character.isprintable()
    )


def normalize_whitespace(text: str) -> str:
    """Normalize indentation and whitespace without flattening document paragraphs."""

    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def estimate_reading_time(text: str) -> int:
    """Estimate reading time in minutes using a deterministic 200 words-per-minute rate."""

    word_count = len(re.findall(r"\b\w+\b", text))
    return ceil(word_count / WORDS_PER_MINUTE) if word_count else 0


def split_into_sections(text: str) -> list[dict[str, Any]]:
    """Split Markdown-style headings into stable section records for future chunking."""

    matches = list(_HEADING_PATTERN.finditer(text))
    if not matches:
        return _section("Document", text)

    sections: list[dict[str, Any]] = []
    intro = text[: matches[0].start()].strip()
    if intro:
        sections.extend(_section("Introduction", intro))
    for index, match in enumerate(matches):
        content_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.extend(_section(match.group(1).strip(), text[match.end() : content_end].strip()))
    return sections


def extract_metadata(
    text: str,
    *,
    title: str,
    category: str | None,
    source: str | None,
) -> dict[str, Any]:
    """Return deterministic metadata and retrieval tags derived from document content."""

    sections = split_into_sections(text)
    tag_candidates = [category or "", source or "", title]
    tag_candidates.extend(section["heading"] for section in sections)
    tags = sorted(
        {
            token
            for candidate in tag_candidates
            for token in _TOKEN_PATTERN.findall(candidate.lower())
            if token not in _STOP_WORDS
        }
    )
    return {
        "word_count": len(re.findall(r"\b\w+\b", text)),
        "character_count": len(text),
        "section_count": len(sections),
        "reading_time_minutes": estimate_reading_time(text),
        "headings": [section["heading"] for section in sections],
        "tags": tags,
    }


def generate_document_summary(text: str, max_sentences: int = 2, max_length: int = 500) -> str:
    """Create an extractive summary from the first complete sentences of content."""

    summary_source = re.sub(r"(?m)^#{1,6}\s+.*$", "", text)
    sentences = [
        sentence.strip()
        for sentence in _SENTENCE_PATTERN.split(summary_source)
        if sentence.strip()
    ]
    summary = " ".join(sentences[:max_sentences])
    if len(summary) <= max_length:
        return summary
    truncated = summary[: max_length - 1].rsplit(" ", 1)[0]
    return f"{truncated}…"


def _section(heading: str, content: str) -> list[dict[str, Any]]:
    if not content:
        return []
    return [
        {
            "heading": heading,
            "content": content,
            "word_count": len(re.findall(r"\b\w+\b", content)),
        }
    ]
