
"""
pun_engine.jp_utils
-------------------
Tiny helpers for Japanese text heuristics without external deps.
"""

def is_japanese(s: str) -> bool:
    for ch in s:
        code = ord(ch)
        if 0x3040 <= code <= 0x30FF:  # Hiragana + Katakana
            return True
        if 0x4E00 <= code <= 0x9FFF:  # CJK Unified Ideographs
            return True
    return False

def to_katakana(s: str) -> str:
    """Convert Hiragana to Katakana; leave other chars as-is."""
    out = []
    for ch in s:
        code = ord(ch)
        # Hiragana range
        if 0x3041 <= code <= 0x3096:
            out.append(chr(code + 0x60))
        else:
            out.append(ch)
    return "".join(out)
