"""
Graphical demo of the Roman Urdu normalizer.

    python gui.py              start the app and open it in your browser
    python gui.py --no-neural  rule-based + dictionary only (no torch needed)
    python gui.py --port 9000 --no-browser

It is a small local web app (Python standard library + the files in gui/), so there is
nothing extra to install. Everything runs on your own machine; nothing is sent anywhere.
"""
import argparse
import json
import re
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

from ru_norm import baselines as B
from ru_norm import data_gen as D
from ru_norm.editdist import norm_distance
from ru_norm.lexicon import NEG_NONGENDER, POS_NONGENDER
from ru_norm.phonetic import phonetic_key

ROOT = Path(__file__).parent
APP_NAME = "Imla"          # change this to rename the app in the window
TOKEN = re.compile(r"[A-Za-z]+|[0-9]+|[^A-Za-z0-9]+")
DICT_MAX_REL = 0.4
# words the demo sentiment classifiers can actually judge (the vocabulary of the synthetic reviews)
SENTIMENT_CUES = set(POS_NONGENDER + NEG_NONGENDER + ["acha", "achi", "bura", "buri", "mehnga", "mehngi", "shukriya",
                                                        "pasand", "wasool", "zaya", "udaas", "khush", "zaroor", "wapas"])


class Engine:
    def __init__(self, use_neural=True):
        pairs_path = ROOT / "data/pairs.csv"
        if not pairs_path.exists():
            raise SystemExit("data/pairs.csv not found - run `python run_all.py` first.")
        self.pairs = pd.read_csv(pairs_path, keep_default_na=False, dtype=str)
        self.lexicon = sorted(self.pairs.canonical.unique())
        self.known = set(self.lexicon)
        self.variant_table = dict(zip(self.pairs.variant, self.pairs.canonical))
        by = {}
        for v, c, src in self.pairs[["variant", "canonical", "source"]].itertuples(index=False, name=None):
            by.setdefault(c, []).append((src != "hand", v))      # hand-written spellings first
        self.by_canon = {c: [v for _, v in sorted(x)] for c, x in by.items()}
        self.rule = B.RuleBased()
        self.dictionary = B.EditDictionary(self.lexicon, max_rel=DICT_MAX_REL)
        self.nn, self.min_conf, self.model_note = None, 0.0, ""
        if use_neural:
            self._load_neural()
        self._train_sentiment()

    # -------------------------------------------------------------------------
    def _load_neural(self):
        ck = ROOT / "models/seq2seq.pt"
        if not ck.exists():
            self.model_note = "models/seq2seq.pt not found - run python run_all.py to train it"
            return
        try:
            from ru_norm import seq2seq as S
        except ImportError:
            self.model_note = "torch is not installed (pip install torch)"
            return
        dev = S.pick_device()
        model, vocab, meta = S.load_checkpoint(ck, dev)
        self.min_conf = float(meta.get("min_conf", 0.5))
        self.nn = S.NeuralNormalizer(model, vocab, dev, beam=5)
        self.model_note = f"seq2seq loaded, confidence gate {self.min_conf:.2f}"

    # -------------------------------------------------------------------------
    def _neural_word(self, w, use_lookup, raw):
        """Final seq2seq decision for one lower-case word -> (output, source, confidence)."""
        pred, conf = raw[w]
        if w in self.known:
            return w, "vocab", 1.0
        if use_lookup and w in self.variant_table:
            return self.variant_table[w], "lookup", 1.0
        if conf < self.min_conf:
            return w, "kept", conf
        return pred, "model", conf

    def normalize(self, text, use_lookup=True):
        segs = TOKEN.findall(text)
        words = sorted({s.lower() for s in segs if s[0].isalpha()})
        rule = dict(zip(words, self.rule.normalize_words(words)))
        dic = dict(zip(words, self.dictionary.normalize_words(words)))
        raw = dict(zip(words, self.nn.raw(words))) if self.nn else {}
        toks, nn_out = [], {}
        for s in segs:
            if not s[0].isalpha():
                toks.append({"t": s})
                continue
            w = s.lower()
            item = {"t": s, "w": w, "rule": rule[w], "dict": dic[w]}
            if self.nn:
                out, src, conf = self._neural_word(w, use_lookup, raw)
                item.update({"nn": out, "src": src, "conf": round(conf, 3)})
                nn_out[w] = out
            toks.append(item)
        best = nn_out if self.nn else dic
        n_words = sum(1 for t in toks if "w" in t)
        res = {
            "tokens": toks,
            "has_nn": self.nn is not None,
            "stats": {"words": n_words,
                      "changed": sum(1 for t in toks if "w" in t and best[t["w"]] != t["w"]),
                      "distinct_before": len(words),
                      "distinct_after": len(set(best.values()))},
            "sentiment": self.sentiment(text, " ".join(best[t["w"]] for t in toks if "w" in t)),
        }
        return res

    # -------------------------------------------------------------------------
    def variants(self, word, limit=14):
        """Known spellings of the standard form that `word` maps to (for the spelling-cluster view)."""
        w = word.lower().strip()
        if w in self.known:
            canon = w
        elif w in self.variant_table:
            canon = self.variant_table[w]
        else:
            t = [x for x in self.normalize(w)["tokens"] if "w" in x]
            canon = (t[0].get("nn") or t[0]["dict"]) if t else w
        allv = self.by_canon.get(canon, [])
        return {"word": w, "canonical": canon, "total": len(allv), "variants": allv[:limit], "known": canon in self.by_canon}

    def candidates(self, word, use_lookup=True):
        w = word.lower()
        out = {"word": w, "phonetic": phonetic_key(w), "in_vocab": w in self.known}
        if self.nn:
            cands = [{"text": c, "score": round(s, 3), "in_vocab": c in self.known} for c, s in self.nn.nbest(w, 5)]
            out["kind"] = "seq2seq beam search (5 best)"
        else:
            ranked = sorted(self.lexicon, key=lambda c: (norm_distance(w, c), c))[:5]
            cands = [{"text": c, "score": round(1 - norm_distance(w, c), 3), "in_vocab": True} for c in ranked]
            out["kind"] = "nearest vocabulary words by edit distance"
        out["candidates"] = cands
        if w in self.variant_table:
            out["lookup"] = self.variant_table[w]
        return out

    # -------------------------------------------------------------------------
    def _train_sentiment(self):
        """Two small classifiers on synthetic product reviews, mirroring the extrinsic experiment:
        one trained/applied on raw text, one trained/applied on normalized text."""
        pools = D.pools_from_pairs(self.pairs)
        df = D.make_sentiment(800, pools, seed=42, noise_p=0.8)
        self.norm_label = "seq2seq" if self.nn else "dictionary"

        def mk():
            return make_pipeline(TfidfVectorizer(ngram_range=(1, 2), token_pattern=r"[a-z0-9]+"),
                                 LogisticRegression(C=10, max_iter=2000))
        self.clf_raw = mk().fit([t.lower() for t in df.text], df.label)
        self.clf_norm = mk().fit([self._norm_text(t) for t in df.text], df.label)

    def _norm_text(self, text):
        words = [t.lower() for t in TOKEN.findall(text) if t[0].isalpha()]
        uniq = sorted(set(words))
        if self.nn:
            raw = dict(zip(uniq, self.nn.raw(uniq)))
            m = {w: self._neural_word(w, True, raw)[0] for w in uniq}
        else:
            m = dict(zip(uniq, self.dictionary.normalize_words(uniq)))
        return " ".join(m[w] for w in words)

    @staticmethod
    def _score(clf, text, has_cue):
        vocab = clf.named_steps["tfidfvectorizer"].vocabulary_
        toks = re.findall(r"[a-z0-9]+", text.lower())
        covered = sum(1 for t in toks if t in vocab) / max(len(toks), 1)
        p = float(clf.predict_proba([text.lower()])[0][1])
        if not has_cue:
            label = "No sentiment words found"
        elif abs(p - 0.5) < 0.12:
            label = "Unsure"
        else:
            label = "Positive" if p >= 0.5 else "Negative"
        return {"p_pos": round(p, 3), "label": label, "coverage": round(covered, 3), "has_cue": has_cue}

    def sentiment(self, raw_text, norm_text):
        has_cue = any(t in SENTIMENT_CUES for t in re.findall(r"[a-z0-9]+", norm_text.lower()))
        return {"raw": self._score(self.clf_raw, raw_text, has_cue),
                "norm": self._score(self.clf_norm, norm_text, has_cue),
                "normalizer": self.norm_label}

    # -------------------------------------------------------------------------
    def results(self):
        out = {}
        rd = ROOT / "results"
        if (rd / "intrinsic.csv").exists():
            d = pd.read_csv(rd / "intrinsic.csv")
            out["intrinsic"] = d[d.subset == "all"].to_dict("records")
        if (rd / "extrinsic.csv").exists():
            out["extrinsic"] = pd.read_csv(rd / "extrinsic.csv").to_dict("records")
        if (rd / "clustering.json").exists():
            out["clustering"] = json.loads((rd / "clustering.json").read_text())
        return out

    def info(self):
        return {"app": APP_NAME, "vocab": len(self.lexicon), "neural": self.nn is not None,
                "note": self.model_note, "min_conf": self.min_conf, "pairs": int(len(self.pairs))}


# =============================================================================
class Handler(BaseHTTPRequestHandler):
    engine: Engine = None
    lock = threading.Lock()

    def log_message(self, *a):          # keep the console quiet
        pass

    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path in ("/", "/index.html"):
            html = (ROOT / "gui/index.html").read_text(encoding="utf-8").replace("{{APP_NAME}}", APP_NAME)
            return self._send(200, html, "text/html")
        if u.path == "/api/info":
            return self._send(200, json.dumps(self.engine.info()))
        if u.path == "/api/results":
            return self._send(200, json.dumps(self.engine.results()))
        if u.path == "/api/variants":
            q = parse_qs(u.query).get("word", [""])[0][:40]
            with self.lock:
                return self._send(200, json.dumps(self.engine.variants(q)))
        self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(n) or b"{}")
            with self.lock:
                if self.path == "/api/normalize":
                    text = str(body.get("text", ""))[:2000]
                    return self._send(200, json.dumps(self.engine.normalize(text, bool(body.get("lookup", True)))))
                if self.path == "/api/candidates":
                    return self._send(200, json.dumps(self.engine.candidates(str(body.get("word", ""))[:40])))
            self._send(404, json.dumps({"error": "not found"}))
        except Exception as e:           # show the error in the UI instead of crashing the server
            self._send(500, json.dumps({"error": f"{type(e).__name__}: {e}"}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-neural", action="store_true")
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args()
    print("Loading (training the small sentiment demo models takes a few seconds)...")
    Handler.engine = Engine(use_neural=not a.no_neural)
    server = None
    for port in range(a.port, a.port + 20):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
            break
        except OSError:
            continue
    if server is None:
        raise SystemExit("no free port found")
    url = f"http://127.0.0.1:{port}"
    print(f"{APP_NAME} is running at {url}   (press Ctrl+C to stop)")
    if Handler.engine.model_note:
        print("note:", Handler.engine.model_note)
    if not a.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")


if __name__ == "__main__":
    main()
