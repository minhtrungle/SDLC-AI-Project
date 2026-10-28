import type { Citation } from "@/api/types";

export type AnswerPart = { kind: "text"; text: string } | { kind: "cite"; citation: Citation };

/**
 * Split an answer into plain text and [n] citation markers that map to a known citation.
 * Markers without a citation stay as text, so nothing is ever rendered as HTML (XSS guard).
 */
export function splitAnswer(answer: string, citations: Citation[]): AnswerPart[] {
  const byIndex = new Map(citations.map((c) => [c.index, c]));
  const parts: AnswerPart[] = [];
  for (const piece of answer.split(/(\[\d+\])/)) {
    if (!piece) continue;
    const match = /^\[(\d+)\]$/.exec(piece);
    const citation = match ? byIndex.get(Number(match[1])) : undefined;
    parts.push(citation ? { kind: "cite", citation } : { kind: "text", text: piece });
  }
  return parts;
}
