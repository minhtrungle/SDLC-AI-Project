"""CMP-06 Vietnamese text normalisation — the single folding function for indexing and queries (ADR-004)."""

import re
import unicodedata

_TOKEN = re.compile(r"[a-z0-9]+")

# Function words in folded form (Vietnamese and English); they carry no topical meaning.
STOPWORDS = frozenset(
    """
    la gi bao nhieu cua va cac nhung co khong the nao o dau cho voi trong tren duoi duoc mot nay
    kia ay no toi ban minh chung ta ho hay xin vui long ai khi sao vi nhu ra ve den tu theo thi ma
    neu da dang se roi nua cung rat qua hon nhat moi tat ca lam bang cai con nhe a oi u vay day do
    what which who whom whose when where why how is are was were be been the a an of to in on for
    and or does do did with by at from as it its this that these those there their about into tell
    me please
    """.split()  # noqa: SIM905 — readable word list
)


def fold(text: str) -> str:
    """Lowercase, strip combining marks, map đ→d. 'Đà Nẵng' -> 'da nang'."""
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return stripped.replace("đ", "d").replace("Đ", "D").lower()


def tokens(text: str) -> list[str]:
    return _TOKEN.findall(fold(text))


def content_terms(text: str) -> list[str]:
    """Distinct non-stopword tokens in order of first appearance."""
    seen: dict[str, None] = {}
    for t in tokens(text):
        if t not in STOPWORDS and t not in seen:
            seen[t] = None
    return list(seen)
