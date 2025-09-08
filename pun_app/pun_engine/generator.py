
"""
pun_engine.generator
--------------------
Core pun generation logic for Japanese and English.
- Japanese puns: lightweight, template- & phonetic-variant based (no API keys).
- English puns: uses Datamuse (keyless) for rhymes/near rhymes to spice up output.
Also fetches (optional) summaries from Wikipedia REST (keyless) for context.
"""

from typing import List, Dict, Optional, Tuple
import re
import csv
import os
import requests
from .jp_utils import to_katakana, is_japanese

DATAMUSE_ENDPOINT = "https://api.datamuse.com/words"
WIKI_SUMMARY_ENDPOINT = "https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"

def fetch_wikipedia_summary(term: str, lang: str = "ja") -> Optional[str]:
    """Fetch a short summary for `term` from Wikipedia REST API (no key).
    Returns the summary string or None.
    """
    try:
        url = WIKI_SUMMARY_ENDPOINT.format(lang=lang, title=term)
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            # 'extract' key contains the summary in REST API
            return data.get("extract")
    except Exception:
        pass
    return None

def datamuse_rhymes(word: str, max_items: int = 10) -> List[str]:
    """Get rhyming words from Datamuse (no key). For English only."""
    try:
        params = {"rel_rhy": word, "max": str(max_items)}
        resp = requests.get(DATAMUSE_ENDPOINT, params=params, timeout=5)
        if resp.status_code == 200:
            items = resp.json()
            return [x.get("word") for x in items if x.get("word")]
    except Exception:
        pass
    return []

# --- Simple CSV "DB" (Bonus +3) ---
def ensure_csv(path: str, header: List[str]) -> None:
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)

def append_csv(path: str, row: List[str]) -> None:
    ensure_csv(path, [])
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)

def read_csv(path: str) -> List[List[str]]:
    if not os.path.exists(path):
        return []
    with open(path, "r", newline="", encoding="utf-8") as f:
        return list(csv.reader(f))

# --- Japanese pun heuristics ---
TEMPLATES_JA = [
    "{w}だけに、{w}だね！",
    "{w}と言ったら…{w}（言っちゃったね）",
    "{w}が気になって、{w}しか勝たん！",
    "ここはひとつ、{w}（わ）らっとく？",
    "{w}って、{w}っと（わっと）笑える！",
]

# Swaps like カ→蚊 are too semantic; we keep light phonetic play:
# provide small set of near-sound wordplay endings
ENDING_PLAY = ["だね", "だよね", "じゃん", "じゃあるまいか", "してみたかったんだ"]

def jp_puns(word: str, n: int = 5) -> List[str]:
    """Generate lightweight Japanese puns for an input word using templates & sound play."""
    if not word:
        return []
    base = to_katakana(word)
    outs = set()
    # Template-based
    for t in TEMPLATES_JA:
        outs.add(t.format(w=base))
    # Simple reduplication / chiasmus
    outs.add(f"{base}って言ってた？言ってたって{base}！")
    outs.add(f"{base}の話？話の{base}！（はなしのはじまり）")
    # Endings
    for e in ENDING_PLAY:
        outs.add(f"{base}…{e}？{base}だけに！")
    # Truncate to n
    return list(outs)[:max(1, n)]

# --- English pun helpers using Datamuse ---
def en_puns(word: str, n: int = 5) -> List[str]:
    rhymes = datamuse_rhymes(word, max_items=20)
    outs = []
    if rhymes:
        for r in rhymes[:n]:
            outs.append(f"I was going to pun about '{word}', but it might {r}.")
    # fallbacks
    while len(outs) < n:
        outs.append(f"'{word}'? Sounds like fun—pun intended.")
    return outs[:n]

def make_puns(word: str, lang_hint: Optional[str] = None, n: int = 5) -> Dict[str, List[str]]:
    """Main entry: choose JA or EN strategies based on characters or hint."""
    if lang_hint == "ja" or (lang_hint is None and is_japanese(word)):
        puns = jp_puns(word, n=n)
        summary = fetch_wikipedia_summary(word, lang="ja")
    else:
        puns = en_puns(word, n=n)
        summary = fetch_wikipedia_summary(word, lang="en")
    return {"puns": puns, "summary": summary}

