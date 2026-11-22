"""
Dataset construction.

No internet / scraped corpus is needed to run the project end to end:
  * a seed lexicon (lexicon.py) gives canonical words + a few real-world
    variants each,
  * a rule-based spelling-noise generator invents more variants the way
    people really type them (vowel stretching, dropped vowels, extra 'h',
    doubled letters, ph/f, w/v, ...),
  * a template generator makes labelled Roman Urdu product reviews for the
    extrinsic (sentiment) experiment.

To use REAL data, see README ("Using real data").
"""
import random
import re

import pandas as pd

from .editdist import norm_distance
from .lexicon import (NEG_NONGENDER, NOUNS_F, NOUNS_M, OOV_WORDS, POS_NONGENDER,
                      parse_lexicon)

VOWELS = "aeiou"

# ----------------------------------------------------------------------------
# 1. spelling-noise rules
# ----------------------------------------------------------------------------


def _positions(word, chars):
    return [i for i, c in enumerate(word) if c in chars]


def r_stretch_vowel(w, rng):
    pos = _positions(w, VOWELS)
    if not pos:
        return w
    i = rng.choice(pos)
    c = w[i]
    rep = {"a": "aa", "e": "ee", "i": rng.choice(["ee", "ii"]), "o": "oo", "u": rng.choice(["oo", "uu"])}[c]
    return w[:i] + rep + w[i + 1:]


def r_shrink_vowel(w, rng):
    m = list(re.finditer(r"aa|ee|oo|ii", w))
    if not m:
        return w
    x = rng.choice(m)
    return w[:x.start()] + w[x.start()] + w[x.end():]


def r_drop_vowel(w, rng):
    pos = [i for i in _positions(w, VOWELS) if 0 < i < len(w) - 1]
    if not pos:
        return w
    i = rng.choice(pos)
    return w[:i] + w[i + 1:]


def r_skeleton(w, rng):
    """sms style: keep first letter, drop all other vowels (bohat -> bht)."""
    if len(w) < 5:
        return w
    return w[0] + "".join(c for c in w[1:] if c not in VOWELS)


def r_insert_h(w, rng):
    pos = [i for i, c in enumerate(w[:-1]) if c in "cktpdbgj" and w[i + 1] != "h"]
    if not pos:
        return w
    i = rng.choice(pos)
    return w[:i + 1] + "h" + w[i + 1:]


def r_double_consonant(w, rng):
    pos = [i for i, c in enumerate(w) if i > 0 and c not in VOWELS and (i + 1 >= len(w) or w[i + 1] != c)]
    if not pos:
        return w
    i = rng.choice(pos)
    return w[:i] + w[i] + w[i:]


def r_final_vowel(w, rng):
    table = {
        "a": ["aa", "ah", "ay"],
        "i": ["ee", "y", "ii", "ey"],
        "e": ["ay", "ey", "ai"],
        "o": ["oo", "ou"],
    }
    if w[-1] in table:
        return w[:-1] + rng.choice(table[w[-1]])
    return w


def r_swap(w, rng):
    table = [("ai", "ay"), ("ay", "ai"), ("ay", "ey"), ("k", "q"), ("w", "v"), ("v", "w"),
             ("f", "ph"), ("ph", "f"), ("ch", "chh"), ("kh", "k"), ("sh", "s"), ("z", "j"),
             ("j", "z"), ("oo", "u"), ("ee", "i"), ("ei", "ai"), ("th", "t"), ("e", "a")]
    cand = [(a, b) for a, b in table if a in w]
    if not cand:
        return w
    a, b = rng.choice(cand)
    i = rng.choice([m.start() for m in re.finditer(re.escape(a), w)])
    return w[:i] + b + w[i + len(a):]


def r_trail(w, rng):
    return w + w[-1] * rng.choice([1, 2])


RULES = [(r_stretch_vowel, 3), (r_shrink_vowel, 2), (r_drop_vowel, 3), (r_skeleton, 1),
         (r_insert_h, 2), (r_double_consonant, 2), (r_final_vowel, 3), (r_swap, 3), (r_trail, 1)]
_RULE_FUNCS = [f for f, wt in RULES for _ in range(wt)]


def generate_variant(word: str, rng: random.Random) -> str:
    """Apply 1-2 random noise rules; may return the word unchanged (caller checks)."""
    out = word
    for _ in range(rng.choice([1, 1, 2])):
        out = rng.choice(_RULE_FUNCS)(out, rng)
    return out


# ----------------------------------------------------------------------------
# 2. variant pools and (variant -> canonical) pairs
# ----------------------------------------------------------------------------


def build_variant_pools(seed=0, target=16):
    """{canonical: [(variant, 'hand'|'generated'), ...]} with up to `target` variants."""
    rng = random.Random(seed)
    lex = parse_lexicon()
    pools = {}
    for canon, hand in lex.items():
        seen = {canon}
        pool = []
        for v in hand:
            if v not in seen:
                seen.add(v)
                pool.append((v, "hand"))
        tries = 0
        goal = max(target, len(pool))
        while len(pool) < goal and tries < 200:
            tries += 1
            v = generate_variant(canon, rng)
            if v in seen or not v.isalpha() or not (2 <= len(v) <= 24):
                continue
            if norm_distance(v, canon) > 0.5:          # keep noise realistic
                continue
            seen.add(v)
            pool.append((v, "generated"))
        pools[canon] = pool
    return pools


def build_pairs(seed=0, target=16) -> pd.DataFrame:
    """DataFrame[variant, canonical, source]; ambiguous variant strings are dropped."""
    pools = build_variant_pools(seed, target)
    canon_set = set(pools)
    owners = {}
    for canon, pool in pools.items():
        for v, _ in pool:
            owners.setdefault(v, set()).add(canon)
    rows = []
    for canon, pool in pools.items():
        for v, src in pool:
            if len(owners[v]) > 1 or v in canon_set:   # ambiguous or equals another canonical word
                continue
            rows.append((v, canon, src))
    return pd.DataFrame(rows, columns=["variant", "canonical", "source"])


def sentiment_words():
    """Every word the review templates can emit (kept in the training word split)."""
    toks = set()
    for t in _POS_T + _NEG_T:
        toks.update(w for w in t.split() if not w.startswith("{"))
    toks.update(POS_NONGENDER + NEG_NONGENDER + NOUNS_M + NOUNS_F)
    toks.update(_GENDERED["pos"] + _GENDERED["neg_adj"])
    return toks


def make_splits(pairs: pd.DataFrame, seed=0, unseen_word_frac=0.15, test_var_frac=0.2, val_frac=0.1,
                force_train_words=()):
    """
    Three evaluation regimes:
      train          : variants of seen words (+ identity pairs canonical->canonical)
      val            : held-out variants of seen words (model selection)
      test_variants  : held-out variants of seen words   ("unseen variants")
      test_words     : ALL variants of words never seen in training ("unseen words", hardest)
    """
    rng = random.Random(seed)
    canon = sorted(pairs["canonical"].unique())
    force = set(force_train_words)
    free = [c for c in canon if c not in force]
    rng.shuffle(free)
    n_unseen = int(round(unseen_word_frac * len(canon)))
    unseen = set(free[:n_unseen])
    train_words = [c for c in canon if c not in unseen]

    tr, va, te = [], [], []
    for c, g in pairs[pairs.canonical.isin(train_words)].groupby("canonical"):
        rows = list(g[["variant", "canonical"]].itertuples(index=False, name=None))
        rng.shuffle(rows)
        n = len(rows)
        n_te = max(1, round(test_var_frac * n)) if n >= 4 else 0
        n_va = max(1, round(val_frac * n)) if n >= 6 else 0
        te += rows[:n_te]
        va += rows[n_te:n_te + n_va]
        tr += rows[n_te + n_va:]
    tr += [(c, c) for c in train_words]            # identity pairs: standard form stays standard
    cols = ["variant", "canonical"]
    out = {
        "train": pd.DataFrame(tr, columns=cols),
        "val": pd.DataFrame(va, columns=cols),
        "test_variants": pd.DataFrame(te, columns=cols),
        "test_words": pairs[pairs.canonical.isin(unseen)][cols].reset_index(drop=True),
        "train_words": train_words,
        "unseen_words": sorted(unseen),
    }
    return out


def make_oov_splits(pairs: pd.DataFrame, seed=0):
    """
    Words that are NOT in the lexicon and must be left unchanged (gold = the word itself).
      val_oov  : used to calibrate the seq2seq confidence threshold
      test_oov : used for the final "does it leave unknown words alone?" test
    """
    taken = set(pairs["canonical"]) | set(pairs["variant"])
    words = sorted({w for w in OOV_WORDS if w not in taken})
    rng = random.Random(seed + 7)
    rng.shuffle(words)
    half = len(words) // 2
    mk = lambda ws: pd.DataFrame({"variant": ws, "canonical": ws})
    return {"val_oov": mk(words[:half]), "test_oov": mk(words[half:])}


# ----------------------------------------------------------------------------
# 3. synthetic labelled reviews (extrinsic experiment)
# ----------------------------------------------------------------------------

_POS_T = [
    "{n} bohat {pa} hai",
    "{n} {pa} hai shukriya",
    "bohat {pa} {n} hai mujhe pasand aya",
    "{n} dekh kar dil khush ho gaya",
    "{pa2} {n} paisa wasool",
    "{n} {na} nahi hai bilkul theek hai",
    "{n} {pa} hai zaroor lena",
]
_NEG_T = [
    "{n} bohat {na} hai",
    "{n} bilkul {na} hai paisa zaya",
    "mujhe {n} pasand nahi aya",
    "{n} {pa} nahi hai",
    "{n} {na} hai wapas karna hai",
    "aisi {n} ki umeed nahi thi bohat {na}",
    "{n} dekh kar dil udaas ho gaya",
]
_GENDERED = {  # (masculine, feminine)
    "pos": ("acha", "achi"),
    "neg_adj": ("bura", "buri"),
}


def _fill(template, rng):
    noun = rng.choice(NOUNS_M + NOUNS_F)
    fem = noun in NOUNS_F
    pa = rng.choice(POS_NONGENDER + [_GENDERED["pos"][fem]])
    pa2 = rng.choice(POS_NONGENDER)
    na = rng.choice(NEG_NONGENDER + [_GENDERED["neg_adj"][fem]])
    return template.format(n=noun, pa=pa, pa2=pa2, na=na)


def clean_review(rng):
    """-> (canonical text, label)  label 1 = positive, 0 = negative"""
    if rng.random() < 0.5:
        return _fill(rng.choice(_POS_T), rng), 1
    return _fill(rng.choice(_NEG_T), rng), 0


def add_noise(text, pools, rng, p=0.8):
    """Replace each known word with a random spelling variant w.p. p."""
    out = []
    for tok in text.split():
        if tok in pools and pools[tok] and rng.random() < p:
            out.append(rng.choice(pools[tok]))
        else:
            out.append(tok)
    return " ".join(out)


def make_sentiment(n, pools, seed=0, noise_p=0.8) -> pd.DataFrame:
    """pools: {canonical: [variant, ...]} (plain strings). Returns text, clean, label."""
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        clean, y = clean_review(rng)
        rows.append((add_noise(clean, pools, rng, noise_p), clean, y))
    return pd.DataFrame(rows, columns=["text", "clean", "label"])


def pools_from_pairs(pairs: pd.DataFrame):
    pools = {}
    for v, c in pairs[["variant", "canonical"]].itertuples(index=False, name=None):
        pools.setdefault(c, []).append(v)
    return pools
