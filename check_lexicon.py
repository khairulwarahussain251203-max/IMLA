"""
Sanity-check the vocabulary before you retrain.     python check_lexicon.py

Reports
  * how many canonical words / hand-written variants / final pairs you have
  * hand-written variants claimed by two different words (ambiguous -> dropped from the dataset)
  * hand-written variants that are themselves another canonical word (dropped as well)
  * lexicon words that clash with the reserved unknown-word test list (OOV_WORDS)
  * entries that are not lowercase letters only
Fix anything printed under "PROBLEMS" in ru_norm/lexicon.py or ru_norm/lexicon_more.py.
"""
import sys
from collections import defaultdict

from ru_norm import data_gen as D
from ru_norm.lexicon import LEX_EXTRA, LEX_MORE, LEX_TEXT, OOV_WORDS, parse_lexicon


def count_block(text):
    return len(parse_lexicon(text))


def main(variants_per_word=16):
    lex = parse_lexicon()
    canon = set(lex)
    problems = []

    owners = defaultdict(set)
    for c, vs in lex.items():
        for v in vs:
            owners[v].add(c)
    for v, cs in sorted(owners.items()):
        if len(cs) > 1:
            problems.append(f"variant '{v}' is listed under several words: {sorted(cs)}")
        if v in canon and v not in cs:
            problems.append(f"variant '{v}' of {sorted(cs)} is also a canonical word")

    clash = sorted(canon & set(OOV_WORDS))
    if clash:
        problems.append(f"canonical words that are reserved unknown-test words: {clash}")
    clash_v = sorted(set(owners) & set(OOV_WORDS))
    if clash_v:
        problems.append(f"variants that are reserved unknown-test words: {clash_v}")

    for c, vs in lex.items():
        for w in [c] + vs:
            if not (w.isalpha() and w.islower() and w.isascii()):
                problems.append(f"'{w}' (in {c}) is not lowercase ascii letters only")

    print(f"canonical words : {len(lex)}   (block 1: {count_block(LEX_TEXT)}, "
          f"block 2: {count_block(LEX_EXTRA)}, block 3: {count_block(LEX_MORE)})")
    print(f"hand variants   : {sum(len(v) for v in lex.values())}")
    pairs = D.build_pairs(0, variants_per_word)
    src = pairs.source.value_counts().to_dict()
    print(f"final pairs     : {len(pairs)}  ({src})  with {variants_per_word} variants per word")
    print(f"reserved unknown-test words: {len(set(OOV_WORDS))}")
    if problems:
        print(f"\nPROBLEMS ({len(problems)})")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("\nno problems found")


if __name__ == "__main__":
    main()
