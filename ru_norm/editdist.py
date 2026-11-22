"""Edit-distance helpers (pure python, no dependencies)."""


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def norm_distance(a: str, b: str) -> float:
    """Levenshtein distance divided by the longer word length (0..1)."""
    return levenshtein(a, b) / max(len(a), len(b), 1)


def word_accuracy(preds, golds) -> float:
    return sum(p == g for p, g in zip(preds, golds)) / max(len(golds), 1)


def char_error_rate(preds, golds) -> float:
    """Corpus-level CER: total edit distance / total reference characters."""
    dist = sum(levenshtein(p, g) for p, g in zip(preds, golds))
    return dist / max(sum(len(g) for g in golds), 1)
