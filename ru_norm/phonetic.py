"""
A small phonetic key for Roman Urdu.

Idea: people change vowels, double letters and sprinkle 'h' freely, but the
consonant skeleton of a word stays stable. So  acha / achha / accha / achaa
all map to the same key, and  bohat / bahut / bht  do too.
"""
import re

_SUBS = [("ph", "f"), ("ck", "k"), ("x", "ks"), ("q", "k"), ("w", "v"), ("z", "j")]


def phonetic_key(word: str) -> str:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return ""
    w = re.sub(r"(?:c?ch+)+", "#", w)              # ch / chh / cch / chch -> one unit
    w = re.sub(r"c(?=[eiy])", "s", w)
    w = w.replace("c", "k")
    w = w.replace("#", "ch")
    for a, b in _SUBS:
        w = w.replace(a, b)
    w = re.sub(r"(.)\1+", r"\1", w)                # collapse repeated letters
    w = re.sub(r"([aeiouy])h$", r"\1", w)          # zyadah -> zyada
    starts_with_vowel = w[0] in "aeiou"
    out = []
    for i, c in enumerate(w):
        if c in "aeiou":
            continue
        if c == "y":
            prev_cons = i > 0 and w[i - 1] not in "aeiouy"
            next_vowel = i + 1 < len(w) and w[i + 1] in "aeiou"
            prev_i = i > 0 and w[i - 1] == "i"     # shukriya ~ shukria
            if prev_cons or prev_i or not next_vowel:  # y acting as a vowel/glide
                continue
        out.append(c)
    return ("A" if starts_with_vowel else "") + "".join(out)
