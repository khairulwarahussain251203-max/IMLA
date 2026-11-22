"""
Interactive demo.   python demo.py             -> type Roman Urdu, see it normalized
                    python demo.py --no-neural    (dictionary / rules only)

The seq2seq model uses the confidence gate tuned by run_all.py: words it does not
recognise (names, unseen words) are left unchanged instead of being forced into a
wrong known word.
"""
import argparse
from pathlib import Path

import pandas as pd

from ru_norm import baselines as B

ROOT = Path(__file__).parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-neural", action="store_true")
    a = ap.parse_args()
    pairs = pd.read_csv(ROOT / "data/pairs.csv", keep_default_na=False, dtype=str)
    lexicon = sorted(pairs.canonical.unique())
    systems = {"rule-based": B.RuleBased(), "dictionary": B.EditDictionary(lexicon, max_rel=0.3)}
    ck = ROOT / "models/seq2seq.pt"
    if not a.no_neural and ck.exists():
        from ru_norm import seq2seq as S
        dev = S.pick_device()
        model, vocab, meta = S.load_checkpoint(ck, dev)
        systems["seq2seq"] = S.NeuralNormalizer(model, vocab, dev, beam=5, min_conf=meta.get("min_conf", 0.5),
                                                known=lexicon)
    else:
        print("(seq2seq model not loaded - run run_all.py first, or torch is missing)")
    print("Type a sentence (empty line to quit)\n")
    while True:
        try:
            s = input("> ").strip()
        except EOFError:
            break
        if not s:
            break
        for name, n in systems.items():
            print(f"  {name:11s}: {n.normalize_text(s)}")


if __name__ == "__main__":
    main()
