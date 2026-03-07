"""
density_analyzer.py
--------------------
Computes the optimal HybridChunker max_tokens from the document's
actual word density — no hardcoded document type labels.

Formula
-------
  avg_words_per_page  →  base_tokens  →  clamped to [MIN, MAX]

  base_tokens = avg_words_per_page × TOKENS_PER_WORD

  TOKENS_PER_WORD ≈ 1.35 for English prose
                  ≈ 1.6  for legal/technical text (more subwords)

Intuition:
  Dense doc  (450 w/p legal code)  → base = 607  → clamped to MAX 512
  Medium doc (300 w/p report)      → base = 405  → 405
  Sparse doc (150 w/p textbook)    → base = 202  → clamped to MIN 256

This means:
  - Dense docs  → smaller chunks  → more precise retrieval
  - Sparse docs → larger chunks   → preserves paragraph context
  - Your embedding model limit is always respected

Dataclass returned also carries has_toc / is_dense flags so
the pipeline can log useful diagnostics without complex classification.
"""
from __future__ import annotations
from dataclasses import dataclass


# ── Tunable constants ────────────────────────────────────────────────────────
TOKENS_PER_WORD  = 1.35     # average English token/word ratio
MIN_TOKENS       = 256      # never go below — too granular
MAX_TOKENS       = 512      # your embedding model's limit
DENSE_THRESHOLD  = 350      # words/page above this → "dense" doc


@dataclass
class DensityProfile:
    avg_words_per_page: float
    total_words:        int
    page_count:         int
    max_tokens:         int        # → pass to HybridChunker
    is_dense:           bool       # True if avg > DENSE_THRESHOLD
    has_toc:            bool


class DensityAnalyzer:

    def analyze(self, loader_result: dict) -> DensityProfile:
        """
        Args:
            loader_result: dict from PDFLoader.load()

        Returns:
            DensityProfile with computed max_tokens
        """
        avg_wpg     = loader_result["avg_words_per_page"]
        total_words = loader_result["total_words"]
        page_count  = loader_result["page_count"]
        toc         = loader_result.get("toc", [])

        # Compute raw target
        raw_tokens = avg_wpg * TOKENS_PER_WORD

        # Clamp to model limits
        max_tokens = int(min(max(raw_tokens, MIN_TOKENS), MAX_TOKENS))

        return DensityProfile(
            avg_words_per_page = round(avg_wpg, 1),
            total_words        = total_words,
            page_count         = page_count,
            max_tokens         = max_tokens,
            is_dense           = avg_wpg > DENSE_THRESHOLD,
            has_toc            = len(toc) > 2,
        )