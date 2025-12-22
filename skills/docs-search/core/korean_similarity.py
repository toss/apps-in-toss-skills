"""
Utilities for Korean-aware similarity scoring.

Based on the open-source approach for decomposing Hangul syllables into
choseong/jungseong/jongseong, then running difflib.SequenceMatcher on the
decomposed strings. Includes handling for double consonants/vowels.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher

BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

CHOSUNG_LIST = [
    "ㄱ",
    "ㄲ",
    "ㄴ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

JUNGSUNG_LIST = [
    "ㅏ",
    "ㅐ",
    "ㅑ",
    "ㅒ",
    "ㅓ",
    "ㅔ",
    "ㅕ",
    "ㅖ",
    "ㅗ",
    "ㅘ",
    "ㅙ",
    "ㅚ",
    "ㅛ",
    "ㅜ",
    "ㅝ",
    "ㅞ",
    "ㅟ",
    "ㅠ",
    "ㅡ",
    "ㅢ",
    "ㅣ",
]

JONGSUNG_LIST = [
    " ",
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

DOUBLE_KOREAN_DICT = {
    "ㄲ": "ㄱㄱ",
    "ㄸ": "ㄷㄷ",
    "ㅃ": "ㅂㅂ",
    "ㅆ": "ㅅㅅ",
    "ㅉ": "ㅈㅈ",
    "ㄳ": "ㄱㅅ",
    "ㄵ": "ㄴㅈ",
    "ㄶ": "ㄴㅎ",
    "ㄺ": "ㄹㄱ",
    "ㄻ": "ㄹㅁ",
    "ㄼ": "ㄹㅂ",
    "ㄽ": "ㄹㅅ",
    "ㄾ": "ㄹㅌ",
    "ㄿ": "ㄹㅍ",
    "ㅀ": "ㄹㅎ",
    "ㅄ": "ㅂㅅ",
    "ㅐ": "ㅏㅣ",
    "ㅒ": "ㅑㅣ",
    "ㅔ": "ㅓㅣ",
    "ㅖ": "ㅕㅣ",
    "ㅘ": "ㅗㅏ",
    "ㅙ": "ㅗㅐ",
    "ㅚ": "ㅗㅣ",
    "ㅝ": "ㅜㅓ",
    "ㅞ": "ㅜㅔ",
    "ㅟ": "ㅜㅣ",
    "ㅢ": "ㅡㅣ",
}

KOREAN_CHAR_RE = re.compile(r"[ㄱ-ㅎㅏ-ㅣ가-힣]")


def has_korean(text: str) -> bool:
    """Return True if the string contains any Hangul character."""
    return bool(KOREAN_CHAR_RE.search(text))


def _convert_korean(text: str) -> str:
    pieces: list[str] = []
    for ch in text:
        if not has_korean(ch):
            pieces.append(ch)
            continue
        code = ord(ch) - BASE_CODE
        cho = int(code / CHOSUNG)
        jung = int((code - (CHOSUNG * cho)) / JUNGSUNG)
        jong = int(code - (CHOSUNG * cho) - (JUNGSUNG * jung))
        pieces.append(CHOSUNG_LIST[cho])
        pieces.append(JUNGSUNG_LIST[jung])
        if jong != 0:
            pieces.append(JONGSUNG_LIST[jong])
    return "".join(pieces)


def _expand_double_korean(text: str) -> str:
    for k, v in DOUBLE_KOREAN_DICT.items():
        text = text.replace(k, v)
    return text


def korean_similarity(str1: str, str2: str) -> float:
    """
    Korean-aware similarity ratio using SequenceMatcher on decomposed Hangul.
    """
    a = _expand_double_korean(_convert_korean(str1))
    b = _expand_double_korean(_convert_korean(str2))
    return SequenceMatcher(None, a, b).ratio()

