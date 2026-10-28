from cwd.textnorm import content_terms, fold, tokens


def test_fold_removes_vietnamese_diacritics():
    """NFR-003 / AC-301.2: accented and unaccented text match."""
    assert fold("Giá trị HỢP ĐỒNG Đà Nẵng") == "gia tri hop dong da nang"
    assert fold("đường") == "duong"


def test_tokens_split_on_non_alphanumerics():
    assert tokens("Hợp đồng số HD-2026/01, giá 2,5 tỷ.") == [
        "hop",
        "dong",
        "so",
        "hd",
        "2026",
        "01",
        "gia",
        "2",
        "5",
        "ty",
    ]


def test_content_terms_drop_stopwords_and_duplicates():
    assert content_terms("Giá trị hợp đồng Alpha là bao nhiêu?") == ["gia", "tri", "hop", "dong", "alpha"]
    assert content_terms("Thời hạn của nó là gì?") == ["thoi", "han"]
    assert content_terms("What is the value of contract Alpha?") == ["value", "contract", "alpha"]
    assert content_terms("là gì?") == []
