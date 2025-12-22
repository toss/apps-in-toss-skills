#!/usr/bin/env python3
"""
docs_search.py
----------------
Single CLI to quickly query Toss / Apps-in-Toss llms.txt documents.
It caches the downloaded content and returns snippets ranked by simple keyword/similarity scores.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import requests
from difflib import SequenceMatcher

from core.korean_similarity import has_korean, korean_similarity


SOURCE_URLS = [
    "https://developers-apps-in-toss.toss.im/llms-full.txt",
    "https://tossmini-docs.toss.im/tds-mobile/llms-full.txt",
    "https://tossmini-docs.toss.im/tds-react-native/llms-full.txt",
]

CACHE_DIR = Path(tempfile.gettempdir()) / "apps-in-toss" / "skills" / ".cache"


@dataclass
class Chunk:
    source: str
    heading: str
    text: str


def ensure_cache_dir() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_path(url: str) -> Path:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return CACHE_DIR / f"{digest}.txt"


def fetch(url: str, refresh: bool = False) -> str:
    """
    Fetch text from URL with optional cache refresh.
    Uses cache by default; re-downloads only when refresh=True.
    """
    path = _cache_path(url)
    if path.exists() and not refresh:
        return path.read_text(encoding="utf-8")

    response = requests.get(url, headers={"User-Agent": "Apps-In-Toss-Skills/1.0.0"}, timeout=20)
    response.raise_for_status()
    path.write_bytes(response.content)
    return text


def _split_blocks(text: str) -> Iterable[str]:
    return [block for block in re.split(r"\n\s*\n", text) if block.strip()]


def collect_documents(refresh: bool = False) -> list[tuple[str, str]]:
    """
    Fetch llms-full.txt sources.
    Returns list of (url, text).
    """
    ensure_cache_dir()
    documents: list[tuple[str, str]] = []

    for url in SOURCE_URLS:
        try:
            text = fetch(url, refresh=refresh)
            documents.append((url, text))
        except Exception:
            continue

    return documents


def chunk_text(text: str, source: str) -> List[Chunk]:
    """
    Split text into paragraphs and attach the most recent heading as context.
    """
    heading_stack: list[str] = []
    chunks: list[Chunk] = []

    for block in _split_blocks(text):
        lines = [ln.rstrip() for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue

        headings = [ln for ln in lines if ln.lstrip().startswith("#")]
        if headings:
            heading_stack = [h.lstrip("# ").strip() for h in headings]

        heading_label = " > ".join(heading_stack[-3:]) if heading_stack else ""
        chunk_body = "\n".join(lines)
        chunks.append(Chunk(source=source, heading=heading_label, text=chunk_body))

    return chunks


def score(query: str, text: str) -> float:
    """
    Scoring: keyword overlap (weight 2) + SequenceMatcher similarity.
    """
    q = query.lower()
    t = text.lower()
    tokens = [tok for tok in re.split(r"[^a-z0-9가-힣]+", q) if tok]
    overlap = sum(1 for tok in tokens if tok in t)
    if has_korean(q) or has_korean(t):
        ratio = korean_similarity(q, t[:1500])
    else:
        ratio = SequenceMatcher(None, q, t[:1500]).ratio()
    return overlap * 2 + ratio


def search(query: str, topk: int = 5, refresh: bool = False) -> list[dict]:
    documents = collect_documents(refresh=refresh)

    chunks: list[Chunk] = []
    for url, raw in documents:
        chunks.extend(chunk_text(raw, source=url))

    scored = sorted(
        ((score(query, chunk.text), chunk) for chunk in chunks),
        key=lambda pair: pair[0],
        reverse=True,
    )

    results = []
    for score_value, chunk in scored[:topk]:
        snippet = textwrap.shorten(
            chunk.text.replace("\n", " "), width=380, placeholder=" ..."
        )
        results.append(
            {
                "source": chunk.source,
                "heading": chunk.heading,
                "score": round(score_value, 3),
                "snippet": snippet,
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lightweight llms-full.txt searcher for Toss docs"
    )
    parser.add_argument("-q", "--query", required=True, help="Search query")
    parser.add_argument("-k", "--topk", type=int, default=5, help="Number of results")
    parser.add_argument(
        "--refresh-cache", action="store_true", help="Ignore cache and re-download"
    )
    args = parser.parse_args()

    results = search(args.query, topk=args.topk, refresh=args.refresh_cache)
    for idx, item in enumerate(results, start=1):
        heading = f" - {item['heading']}" if item["heading"] else ""
        print(f"[{idx}] {item['source']}{heading}")
        print(f"score: {item['score']}")
        print(item["snippet"])
        print("-" * 80)


if __name__ == "__main__":
    main()

