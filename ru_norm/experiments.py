"""Intrinsic and extrinsic evaluation + plots."""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

from .baselines import EditDictionary, Normalizer
from .data_gen import make_sentiment
from .editdist import char_error_rate, word_accuracy


class Oracle(Normalizer):
    """Upper bound for the extrinsic test: uses the gold variant->canonical map."""
    name = "oracle (gold normalization)"

    def __init__(self, pairs):
        self.table = dict(zip(pairs["variant"], pairs["canonical"]))

    def normalize_word(self, w):
        return self.table.get(w, w)


# ----------------------------------------------------------------------------
# calibration on validation data (never on the test sets)
#   objective = word accuracy on held-out variants  +  share of unknown words left untouched
# ----------------------------------------------------------------------------
def calibrate_dictionary(train_words, val, val_oov, grid=(0.25, 0.3, 0.34, 0.4, 0.45, 0.5, 0.55, 0.6)):
    best = None
    for mr in grid:
        d = EditDictionary(train_words, max_rel=mr)
        acc = word_accuracy(d.normalize_words(list(val.variant)), list(val.canonical))
        pres = word_accuracy(d.normalize_words(list(val_oov.variant)), list(val_oov.canonical))
        if best is None or acc + pres > best[0] + 1e-9:
            best = (acc + pres, mr, acc, pres)
    return best[1], {"val_acc": best[2], "val_oov_kept": best[3]}


def calibrate_gate(raw_norm, val, val_oov, known=(), grid=None):
    """Pick the seq2seq confidence threshold. raw_norm = an UNGATED NeuralNormalizer."""
    grid = list(np.arange(0.0, 0.96, 0.05)) if grid is None else grid
    known = set(known)
    wv, gv = list(val.variant), list(val.canonical)
    wo = list(val_oov.variant)
    rv, ro = raw_norm.raw(wv), raw_norm.raw(wo)
    best = None
    for thr in grid:
        pv = [w if (w in known or c < thr) else p for w, (p, c) in zip(wv, rv)]
        po = [w if (w in known or c < thr) else p for w, (p, c) in zip(wo, ro)]
        acc, pres = word_accuracy(pv, gv), word_accuracy(po, wo)
        if best is None or acc + pres > best[0] + 1e-9:
            best = (acc + pres, float(thr), acc, pres)
    return best[1], {"val_acc": best[2], "val_oov_kept": best[3]}


# ----------------------------------------------------------------------------
# intrinsic
# ----------------------------------------------------------------------------
def intrinsic_table(normalizers, splits, pairs, test_sets=("test_variants", "test_words", "test_oov")):
    src = dict(zip(pairs["variant"], pairs["source"])) if "source" in pairs else {}
    rows = []
    for norm in normalizers:
        for ts in test_sets:
            d = splits[ts]
            if len(d) == 0:
                continue
            preds = norm.normalize_words(list(d["variant"]))
            gold = list(d["canonical"])
            rows.append({"system": norm.name, "test_set": ts, "subset": "all", "n": len(d),
                         "word_acc": word_accuracy(preds, gold), "CER": char_error_rate(preds, gold)})
            if src and ts == "test_variants":
                tag = d["variant"].map(src)
                for s in sorted(tag.dropna().unique()):
                    m = (tag == s).values
                    p = [x for x, k in zip(preds, m) if k]
                    g = [x for x, k in zip(gold, m) if k]
                    rows.append({"system": norm.name, "test_set": ts, "subset": f"{s} variants", "n": int(m.sum()),
                                 "word_acc": word_accuracy(p, g), "CER": char_error_rate(p, g)})
    return pd.DataFrame(rows)


def plot_intrinsic(df, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    d = df[df.subset == "all"]
    sets = list(d.test_set.unique())
    systems = list(dict.fromkeys(d.system))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, metric in zip(axes, ["word_acc", "CER"]):
        w = 0.8 / len(sets)
        for k, ts in enumerate(sets):
            vals = [d[(d.system == s) & (d.test_set == ts)][metric].mean() for s in systems]
            ax.bar(np.arange(len(systems)) + k * w, vals, w, label=ts)
        ax.set_xticks(np.arange(len(systems)) + w * (len(sets) - 1) / 2)
        ax.set_xticklabels(systems, rotation=25, ha="right", fontsize=8)
        ax.set_title("word accuracy (higher is better)" if metric == "word_acc" else "character error rate (lower is better)")
        ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(path, dpi=140)
    plt.close()


# ----------------------------------------------------------------------------
# extrinsic: does normalization help a downstream classifier?
# ----------------------------------------------------------------------------
def _fit_eval(train_txt, y_tr, test_txt, y_te):
    vec = TfidfVectorizer(ngram_range=(1, 2), token_pattern=r"[a-z0-9]+")
    Xtr = vec.fit_transform(train_txt)
    clf = LogisticRegression(C=10, max_iter=2000).fit(Xtr, y_tr)
    pred = clf.predict(vec.transform(test_txt))
    return accuracy_score(y_te, pred), f1_score(y_te, pred, average="macro"), Xtr.shape[1]


def extrinsic_synthetic(normalizers, pools, n_train=200, n_test=600, seeds=(0, 1, 2, 3, 4), noise_p=0.8):
    rows = []
    for seed in seeds:
        tr = make_sentiment(n_train, pools, seed=1000 + seed, noise_p=noise_p)
        te = make_sentiment(n_test, pools, seed=2000 + seed, noise_p=noise_p)
        for norm in normalizers:
            a, f, nfeat = _fit_eval([norm.normalize_text(t) for t in tr.text], tr.label,
                                    [norm.normalize_text(t) for t in te.text], te.label)
            rows.append({"seed": seed, "system": norm.name, "accuracy": a, "macro_f1": f, "n_features": nfeat})
    return pd.DataFrame(rows)


def extrinsic_csv(normalizers, df, seeds=(0, 1, 2, 3, 4), test_size=0.3):
    """df has columns text,label (real data supplied by the user)."""
    rows = []
    for seed in seeds:
        tr, te = train_test_split(df, test_size=test_size, random_state=seed, stratify=df.label)
        for norm in normalizers:
            a, f, nfeat = _fit_eval([norm.normalize_text(t) for t in tr.text], tr.label,
                                    [norm.normalize_text(t) for t in te.text], te.label)
            rows.append({"seed": seed, "system": norm.name, "accuracy": a, "macro_f1": f, "n_features": nfeat})
    return pd.DataFrame(rows)


def summarize_extrinsic(df):
    g = df.groupby("system", sort=False).agg(acc_mean=("accuracy", "mean"), acc_std=("accuracy", "std"),
                                              f1_mean=("macro_f1", "mean"), vocab_size=("n_features", "mean"))
    return g.reset_index()


def plot_extrinsic(summary, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.bar(summary.system, summary.acc_mean, yerr=summary.acc_std.fillna(0), capsize=3, color="#4c78a8")
    ax.set_ylim(max(0.0, summary.acc_mean.min() - 0.1), 1.0)
    ax.set_ylabel("sentiment accuracy")
    ax.set_title("Downstream sentiment accuracy by normalizer (mean ± std over seeds)")
    plt.xticks(rotation=25, ha="right", fontsize=8)
    plt.tight_layout()
    plt.savefig(path, dpi=140)
    plt.close()
