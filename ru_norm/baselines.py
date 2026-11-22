"""
Non-neural normalizers.

All normalizers share one interface:
    normalize_word(w) -> str
    normalize_words(list) -> list
    normalize_text(str) -> str        (tokenise, normalise every token, re-join)
"""
import re
from collections import Counter

from .editdist import levenshtein, norm_distance
from .phonetic import phonetic_key

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str):
    return TOKEN_RE.findall(text.lower())


class Normalizer:
    name = "base"

    def normalize_word(self, w):
        return w

    def normalize_words(self, words):
        return [self.normalize_word(w) for w in words]

    def normalize_text(self, text):
        toks = tokenize(text)
        uniq = sorted(set(toks))
        mapping = dict(zip(uniq, self.normalize_words(uniq)))
        return " ".join(mapping[t] for t in toks)


class Identity(Normalizer):
    name = "raw (no normalization)"


class RuleBased(Normalizer):
    """Baseline 1: hand-written rules (repeated letters, spelling patterns)."""
    name = "rule-based"

    def normalize_word(self, w):
        w = w.lower()
        if not w.isalpha():
            return w
        w = re.sub(r"(.)\1{2,}", r"\1\1", w)          # yaaaar -> yaar
        w = re.sub(r"(?:c?ch+)+", "ch", w)            # chh / cch -> ch
        w = w.replace("ph", "f")
        w = re.sub(r"([^aeiou])\1", r"\1", w)         # doubled consonant -> single
        w = re.sub(r"([aeiou])h$", r"\1", w)          # final vowel+h  (zyadah -> zyada)
        w = re.sub(r"aa$", "a", w)                    # final long a
        w = re.sub(r"ee$", "i", w)                    # final ee -> i
        w = re.sub(r"y$", "i", w)                     # final y  -> i
        w = re.sub(r"ay$", "e", w)                    # final ay -> e
        w = w.replace("kh", "kh").replace("w", "w")
        return w


class VariantTable(Normalizer):
    """Baseline 2: memorised (variant -> canonical) table from the training pairs.
    Perfect on seen variants, useless on anything new."""
    name = "variant lookup table"

    def __init__(self, train_pairs):
        self.table = dict(zip(train_pairs["variant"], train_pairs["canonical"]))

    def normalize_word(self, w):
        return self.table.get(w, w)


class EditDictionary(Normalizer):
    """Baseline 3: nearest canonical word by edit distance.
    Ties are broken by (a) same phonetic key, (b) same first letter, (c) lexicon order.
    Words that are farther than max_rel from every dictionary entry are left unchanged."""
    name = "edit-distance dictionary"

    def __init__(self, canonical_words, max_rel=0.5, label=None):
        self.name = label or f"edit-distance dictionary (max_rel={max_rel:g})"
        self.words = list(canonical_words)
        self.known = set(self.words)
        self.keys = {w: phonetic_key(w) for w in self.words}
        self.max_rel = max_rel
        self.cache = {}

    def normalize_word(self, w):
        if w in self.known or not w.isalpha():
            return w
        if w in self.cache:
            return self.cache[w]
        pk = phonetic_key(w)
        best, best_score = w, None
        for c in self.words:
            d = levenshtein(w, c)
            if d / max(len(w), len(c)) > self.max_rel:
                continue
            score = (d, 0 if self.keys[c] == pk else 1, 0 if c[0] == w[0] else 1)
            if best_score is None or score < best_score:
                best, best_score = c, score
        self.cache[w] = best
        return best
