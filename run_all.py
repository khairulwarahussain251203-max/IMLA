"""
Run the whole project:  python run_all.py                 (needs torch for the neural model)
                        python run_all.py --skip-neural   (baselines only, no torch needed)

Steps
  1. build the (variant -> canonical) dataset + splits            -> data/
  2. demo the clustering pipeline on a raw synthetic corpus        -> data/clusters_for_review.csv
  3. baselines (the dictionary's distance threshold is tuned on validation data)
  4. train / load the character-level seq2seq model                -> models/seq2seq.pt
     and tune its confidence gate on validation data
  5. intrinsic evaluation: unseen variants, unseen words, unknown words that must stay unchanged
  6. extrinsic evaluation (sentiment classifier on raw vs normalized text)
"""
import argparse
import json
from pathlib import Path

import pandas as pd

from ru_norm import baselines as B
from ru_norm import cluster as C
from ru_norm import data_gen as D
from ru_norm import experiments as E

ROOT = Path(__file__).parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--variants-per-word", type=int, default=16)
    ap.add_argument("--pairs", help="your own pairs CSV (columns: variant,canonical) instead of the synthetic one")
    ap.add_argument("--sentiment-csv", help="your own labelled data (columns: text,label) for the extrinsic test")
    ap.add_argument("--skip-neural", action="store_true")
    ap.add_argument("--skip-train", action="store_true", help="load models/seq2seq.pt instead of training")
    ap.add_argument("--epochs", type=int, default=60)
    ap.add_argument("--device", default="auto")
    a = ap.parse_args()

    for d in ("data", "results", "models"):
        (ROOT / d).mkdir(exist_ok=True)

    # 1 -- dataset ------------------------------------------------------------------------
    synthetic = a.pairs is None
    if synthetic:
        pairs = D.build_pairs(a.seed, a.variants_per_word)
        force = D.sentiment_words()
    else:
        pairs = pd.read_csv(a.pairs)
        if "source" not in pairs:
            pairs["source"] = "user"
        force = ()
    sp = D.make_splits(pairs, a.seed, force_train_words=force)
    sp.update(D.make_oov_splits(pairs, a.seed))
    pairs.to_csv(ROOT / "data/pairs.csv", index=False)
    for k in ("train", "val", "test_variants", "test_words", "val_oov", "test_oov"):
        sp[k].to_csv(ROOT / f"data/split_{k}.csv", index=False)
    print(f"[data] {len(pairs)} pairs, {pairs.canonical.nunique()} canonical words | "
          f"train {len(sp['train'])}  val {len(sp['val'])}  test_variants {len(sp['test_variants'])}  "
          f"test_words(unseen words) {len(sp['test_words'])}  test_oov(unknown words) {len(sp['test_oov'])}")

    # 2 -- clustering demo ----------------------------------------------------------------------
    pools = D.pools_from_pairs(pairs)
    if synthetic:
        corpus = D.make_sentiment(4000, pools, seed=a.seed + 11, noise_p=0.8)
        corpus.text.to_csv(ROOT / "data/raw_corpus_demo.txt", index=False, header=False)
        counts = C.count_tokens(corpus.text)
        clusters = C.cluster_tokens(counts, min_count=2)
        C.write_review_csv(clusters, counts, ROOT / "data/clusters_for_review.csv")
        m = C.evaluate_clusters(clusters, counts, dict(zip(pairs.variant, pairs.canonical)))
        (ROOT / "results/clustering.json").write_text(json.dumps(m, indent=1))
        print(f"[cluster] {len(counts)} distinct tokens -> {m['n_clusters']} clusters | purity {m['purity']:.3f} | "
              f"suggested canonical correct for {m['suggested_ok']:.3f} of token mass")

    # 3 -- baselines -----------------------------------------------------------------------------
    max_rel, info = E.calibrate_dictionary(sp["train_words"], sp["val"], sp["val_oov"])
    print(f"[dictionary] tuned max relative edit distance = {max_rel}  (val acc {info['val_acc']:.3f}, "
          f"unknown words kept {info['val_oov_kept']:.3f})")
    systems = [B.Identity(), B.RuleBased(), B.VariantTable(sp["train"]),
               B.EditDictionary(sp["train_words"], max_rel=max_rel, label="edit-distance dictionary (tuned)")]
    if abs(max_rel - 0.5) > 1e-9:   # loose setting too, so the accuracy / safety trade-off is visible
        systems.append(B.EditDictionary(sp["train_words"], max_rel=0.5, label="edit-distance dictionary (loose 0.5)"))

    # 4 -- neural model --------------------------------------------------------------------------
    if not a.skip_neural:
        try:
            from ru_norm import seq2seq as S
        except ImportError:
            print("[seq2seq] torch is not installed -> pip install torch  (continuing with baselines only)")
            S = None
        if S is not None:
            ckpt = ROOT / "models/seq2seq.pt"
            dev = S.pick_device(a.device)
            if a.skip_train and ckpt.exists():
                model, vocab, _ = S.load_checkpoint(ckpt, dev)
            else:
                model, vocab, _ = S.train_model(list(map(tuple, sp["train"].values)),
                                                list(map(tuple, sp["val"].values)),
                                                ckpt, epochs=a.epochs, seed=a.seed, device=a.device)
            known = set(sp["train_words"])
            ungated = S.NeuralNormalizer(model, vocab, dev, beam=1)
            thr, info = E.calibrate_gate(ungated, sp["val"], sp["val_oov"], known)
            print(f"[seq2seq] confidence gate tuned on validation data: min_conf = {thr:.2f}  "
                  f"(val acc {info['val_acc']:.3f}, unknown words kept {info['val_oov_kept']:.3f})")
            S.save_checkpoint(ckpt, model, vocab, {"min_conf": thr, "calibration": info})
            systems += [ungated,
                        S.NeuralNormalizer(model, vocab, dev, beam=1, min_conf=thr, known=known),
                        S.NeuralNormalizer(model, vocab, dev, beam=5, min_conf=thr, known=known)]

    # 5 -- intrinsic -----------------------------------------------------------------------------
    intr = E.intrinsic_table(systems, sp, pairs)
    intr.round(4).to_csv(ROOT / "results/intrinsic.csv", index=False)
    E.plot_intrinsic(intr, ROOT / "results/intrinsic.png")
    print("\n=== INTRINSIC (word accuracy / CER) ===")
    print("test_oov = unknown words that must stay unchanged, so its word_acc is the share left untouched")
    print(intr[intr.subset == "all"].pivot(index="system", columns="test_set", values=["word_acc", "CER"]).round(3)
          .reindex([s.name for s in systems]).to_string())

    # 6 -- extrinsic -----------------------------------------------------------------------------
    if a.sentiment_csv:
        ex = E.extrinsic_csv(systems, pd.read_csv(a.sentiment_csv))
    else:
        ex = E.extrinsic_synthetic(systems + [E.Oracle(pairs)], pools)
    ex.round(4).to_csv(ROOT / "results/extrinsic_runs.csv", index=False)
    summ = E.summarize_extrinsic(ex)
    summ.round(4).to_csv(ROOT / "results/extrinsic.csv", index=False)
    E.plot_extrinsic(summ, ROOT / "results/extrinsic.png")
    print("\n=== EXTRINSIC (sentiment accuracy, mean over 5 seeds) ===")
    print(summ.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
