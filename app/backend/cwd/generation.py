"""CMP-07 Answer Generator — ModelGateway with a local extractive default (ADR-003)."""

import re
from dataclasses import dataclass
from typing import Protocol

from cwd.retrieval import RetrievedChunk
from cwd.textnorm import content_terms, tokens

ANSWER_PREFIX = "Theo tài liệu đã tải lên:"
MAX_SENTENCES = 4
_SENTENCE = re.compile(r"(?<=[.!?;…])\s+")


class GeneratorUnavailable(Exception):
    """The answer service failed or timed out; never fall back to a guessed answer (ADR-003 §4)."""


@dataclass(frozen=True)
class GeneratedAnswer:
    text: str
    used_indices: list[int]


class AnswerGenerator(Protocol):
    mode: str

    def generate(self, question: str, chunks: list[RetrievedChunk]) -> GeneratedAnswer: ...


class LocalExtractiveGenerator:
    """Quotes the best-matching sentence of each retrieved chunk, numbered [n] by chunk position.

    It never interprets document text, so instructions embedded in a PDF cannot steer it (AC-303.2).
    """

    mode = "local"

    def generate(self, question, chunks):
        terms = set(content_terms(question))
        lines, used, seen = [], [], set()
        for index, chunk in enumerate(chunks, start=1):
            best, best_score = None, 0.0
            for sentence in _SENTENCE.split(chunk.text):
                present = set(tokens(sentence))
                score = len(terms & present) / (len(terms) or 1)
                if score > best_score:
                    best, best_score = sentence.strip(), score
            if best is None or best in seen:
                continue
            seen.add(best)
            lines.append(f"- {best} [{index}]")
            used.append(index)
            if len(used) == MAX_SENTENCES:
                break
        if not lines:
            return GeneratedAnswer("", [])
        return GeneratedAnswer(ANSWER_PREFIX + "\n" + "\n".join(lines), used)


def build_generator(settings) -> AnswerGenerator:
    """External AI only when explicitly allowed AND configured; local otherwise (FR-003)."""
    if settings.allow_external_ai and settings.anthropic_api_key:
        from cwd.generation_external import AnthropicGenerator  # noqa: PLC0415 — optional dependency

        return AnthropicGenerator(settings)
    return LocalExtractiveGenerator()
