"""
Character-level encoder-decoder with Bahdanau (additive) attention.

    noisy word  ->  [BiGRU encoder]  ->  [GRU decoder + attention]  ->  canonical word

Reads the noisy word one character at a time and generates the canonical
spelling one character at a time. Small enough to train on a CPU in a few
minutes (about 2k training pairs, ~0.4M parameters).
"""
import json
import random
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

from .baselines import Normalizer
from .editdist import word_accuracy

PAD, SOS, EOS, UNK = 0, 1, 2, 3
MAX_LEN = 30


# ----------------------------------------------------------------------------
# vocabulary
# ----------------------------------------------------------------------------
class CharVocab:
    def __init__(self, chars=()):
        self.itos = ["<pad>", "<sos>", "<eos>", "<unk>"] + sorted(set(chars))
        self.stoi = {c: i for i, c in enumerate(self.itos)}

    @classmethod
    def build(cls, words):
        return cls({c for w in words for c in w})

    def __len__(self):
        return len(self.itos)

    def encode(self, word):
        return [self.stoi.get(c, UNK) for c in word]

    def decode(self, ids):
        out = []
        for i in ids:
            if i == EOS:
                break
            if i > UNK:
                out.append(self.itos[i])
        return "".join(out)


# ----------------------------------------------------------------------------
# model
# ----------------------------------------------------------------------------
class Encoder(nn.Module):
    def __init__(self, vocab_size, emb, hid, drop):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, emb, padding_idx=PAD)
        self.rnn = nn.GRU(emb, hid, batch_first=True, bidirectional=True)
        self.drop = nn.Dropout(drop)

    def forward(self, src, lens):
        x = self.drop(self.emb(src))
        packed = nn.utils.rnn.pack_padded_sequence(x, lens.cpu(), batch_first=True, enforce_sorted=False)
        out, h = self.rnn(packed)
        out, _ = nn.utils.rnn.pad_packed_sequence(out, batch_first=True, total_length=src.size(1))
        h = torch.cat([h[0], h[1]], dim=1)           # (B, 2H): final fwd + final bwd state
        return out, h


class Attention(nn.Module):
    def __init__(self, enc_dim, dec_dim, att_dim):
        super().__init__()
        self.w_enc = nn.Linear(enc_dim, att_dim, bias=False)
        self.w_dec = nn.Linear(dec_dim, att_dim)
        self.v = nn.Linear(att_dim, 1, bias=False)

    def forward(self, dec_h, enc_out, mask):
        # dec_h (B,D)  enc_out (B,T,E)  mask (B,T) True = real character
        score = self.v(torch.tanh(self.w_enc(enc_out) + self.w_dec(dec_h).unsqueeze(1))).squeeze(2)
        score = score.masked_fill(~mask, -1e9)
        attn = F.softmax(score, dim=1)
        ctx = torch.bmm(attn.unsqueeze(1), enc_out).squeeze(1)
        return ctx, attn


class Decoder(nn.Module):
    def __init__(self, vocab_size, emb, enc_dim, dec_dim, drop):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, emb, padding_idx=PAD)
        self.att = Attention(enc_dim, dec_dim, dec_dim)
        self.cell = nn.GRUCell(emb + enc_dim, dec_dim)
        self.out = nn.Linear(dec_dim + enc_dim + emb, vocab_size)
        self.drop = nn.Dropout(drop)

    def step(self, y, h, enc_out, mask):
        e = self.drop(self.emb(y))
        ctx, attn = self.att(h, enc_out, mask)
        h = self.cell(torch.cat([e, ctx], dim=1), h)
        logits = self.out(torch.cat([h, ctx, e], dim=1))
        return logits, h, attn


class Seq2Seq(nn.Module):
    def __init__(self, vocab_size, emb=64, hid=128, drop=0.2):
        super().__init__()
        self.cfg = dict(vocab_size=vocab_size, emb=emb, hid=hid, drop=drop)
        self.enc = Encoder(vocab_size, emb, hid, drop)
        self.bridge = nn.Linear(2 * hid, hid)
        self.dec = Decoder(vocab_size, emb, 2 * hid, hid, drop)

    def encode(self, src, lens):
        enc_out, h = self.enc(src, lens)
        return enc_out, torch.tanh(self.bridge(h)), (src != PAD)

    def forward(self, src, lens, tgt, teacher_forcing=1.0):
        """tgt: (B,T) = <sos> c1 c2 ... <eos> <pad>*   -> logits (B,T-1,V)"""
        enc_out, h, mask = self.encode(src, lens)
        y = tgt[:, 0]
        all_logits = []
        for t in range(1, tgt.size(1)):
            logits, h, _ = self.dec.step(y, h, enc_out, mask)
            all_logits.append(logits)
            y = tgt[:, t] if random.random() < teacher_forcing else logits.argmax(1)
        return torch.stack(all_logits, dim=1)

    @torch.no_grad()
    def greedy(self, src, lens, max_len=MAX_LEN):
        enc_out, h, mask = self.encode(src, lens)
        y = torch.full((src.size(0),), SOS, dtype=torch.long, device=src.device)
        out = []
        for _ in range(max_len):
            logits, h, _ = self.dec.step(y, h, enc_out, mask)
            y = logits.argmax(1)
            out.append(y)
        return torch.stack(out, dim=1)               # (B, max_len)

    @torch.no_grad()
    def greedy_scored(self, src, lens, max_len=MAX_LEN):
        """Greedy decoding that also returns a confidence per word:
        exp(mean log-prob of the generated characters incl. <eos>)  -> value in (0, 1]."""
        enc_out, h, mask = self.encode(src, lens)
        y = torch.full((src.size(0),), SOS, dtype=torch.long, device=src.device)
        ids, lps = [], []
        for _ in range(max_len):
            logits, h, _ = self.dec.step(y, h, enc_out, mask)
            lp = F.log_softmax(logits, dim=1)
            y = lp.argmax(1)
            ids.append(y)
            lps.append(lp.gather(1, y.unsqueeze(1)).squeeze(1))
        ids = torch.stack(ids, dim=1).cpu().tolist()
        lps = torch.stack(lps, dim=1).cpu().tolist()
        confs = []
        for row_ids, row_lp in zip(ids, lps):
            n = row_ids.index(EOS) + 1 if EOS in row_ids else len(row_ids)
            confs.append(float(torch.tensor(sum(row_lp[:n]) / n).exp()))
        return ids, confs

    @torch.no_grad()
    def beam(self, src, lens, k=5, max_len=MAX_LEN):
        """Beam search for ONE word (batch size 1). Returns [(token_ids, norm_logprob), ...] best first."""
        enc_out, h, mask = self.encode(src, lens)
        beams = [(0.0, [SOS], h)]
        done = []
        for _ in range(max_len):
            cand = []
            for score, seq, hh in beams:
                y = torch.tensor([seq[-1]], device=src.device)
                logits, h2, _ = self.dec.step(y, hh, enc_out, mask)
                lp = F.log_softmax(logits, dim=1)[0]
                top = lp.topk(k)
                for v, i in zip(top.values.tolist(), top.indices.tolist()):
                    cand.append((score + v, seq + [i], h2))
            cand.sort(key=lambda x: x[0], reverse=True)
            beams = []
            for sc, seq, hh in cand[:k]:
                if seq[-1] == EOS:
                    done.append((sc / (len(seq) - 1), seq[1:]))
                else:
                    beams.append((sc, seq, hh))
            if not beams:
                break
        if not done:
            done = [(sc / len(seq), seq[1:]) for sc, seq, _ in beams]
        done.sort(key=lambda x: x[0], reverse=True)
        return [(seq, sc) for sc, seq in done]


# ----------------------------------------------------------------------------
# data helpers
# ----------------------------------------------------------------------------
def _pad(seqs):
    m = max(len(s) for s in seqs)
    return torch.tensor([s + [PAD] * (m - len(s)) for s in seqs], dtype=torch.long)


def make_batch(vocab, pairs, device):
    src = [vocab.encode(v) for v, _ in pairs]
    tgt = [[SOS] + vocab.encode(c) + [EOS] for _, c in pairs]
    lens = torch.tensor([len(s) for s in src], dtype=torch.long)
    return _pad(src).to(device), lens, _pad(tgt).to(device)


def encode_words(vocab, words, device):
    src = [vocab.encode(w) or [UNK] for w in words]
    lens = torch.tensor([len(s) for s in src], dtype=torch.long)
    return _pad(src).to(device), lens


def pick_device(name="auto"):
    if name != "auto":
        return torch.device(name)
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ----------------------------------------------------------------------------
# normalizer wrapper + training
# ----------------------------------------------------------------------------
class NeuralNormalizer(Normalizer):
    """
    Wraps a trained Seq2Seq so it can be used like the baselines.

    Confidence gating (fixes the "kitab -> khtab" problem):
      * a word in `known` (the standard vocabulary) is returned unchanged
      * otherwise the model proposes a normalization together with a confidence;
        if confidence < min_conf the ORIGINAL word is returned, because the model is
        probably looking at a word it does not know and would only damage it.
    min_conf = 0 and known = None switches gating off.
    """

    def __init__(self, model, vocab, device, beam=1, batch_size=256, min_conf=0.0, known=None, label=None):
        self.model, self.vocab, self.device = model.to(device).eval(), vocab, device
        self.beam, self.batch_size = beam, batch_size
        self.min_conf, self.known = min_conf, set(known or [])
        self.raw_cache = {}                           # word -> (prediction, confidence)
        decode = "greedy" if beam <= 1 else f"beam {beam}"
        gate = ", gated" if (min_conf > 0 or self.known) else ""
        self.name = label or f"seq2seq ({decode}{gate})"

    def _ok(self, w):
        return w.isalpha() and 0 < len(w) <= MAX_LEN - 2

    def raw(self, words):
        """[(prediction, confidence)] with no gating applied."""
        todo = sorted({w for w in words if w not in self.raw_cache and self._ok(w)})
        if self.beam <= 1:
            for i in range(0, len(todo), self.batch_size):
                chunk = todo[i:i + self.batch_size]
                src, lens = encode_words(self.vocab, chunk, self.device)
                ids, confs = self.model.greedy_scored(src, lens)
                for w, row, c in zip(chunk, ids, confs):
                    self.raw_cache[w] = (self.vocab.decode(row) or w, c)
        else:
            for w in todo:
                src, lens = encode_words(self.vocab, [w], self.device)
                seq, sc = self.model.beam(src, lens, k=self.beam)[0]
                self.raw_cache[w] = (self.vocab.decode(seq) or w, float(torch.tensor(sc).exp()))
        return [self.raw_cache.get(w, (w, 1.0)) for w in words]

    def normalize_words(self, words):
        out = []
        for w, (pred, conf) in zip(words, self.raw(words)):
            if w in self.known or not self._ok(w) or conf < self.min_conf:
                out.append(w)
            else:
                out.append(pred)
        return out

    def normalize_word(self, w):
        return self.normalize_words([w])[0]

    def nbest(self, w, k=5):
        """Top-k candidate canonical forms with a confidence score (for the demo / GUI)."""
        src, lens = encode_words(self.vocab, [w], self.device)
        return [(self.vocab.decode(seq), float(torch.tensor(sc).exp())) for seq, sc in
                self.model.beam(src, lens, k=k)[:k]]


def save_checkpoint(path, model, vocab, meta=None):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    torch.save({"state": model.state_dict(), "cfg": model.cfg, "chars": vocab.itos[4:], "meta": meta or {}}, path)


def load_checkpoint(path, device="cpu"):
    ck = torch.load(path, map_location=device, weights_only=False)
    model = Seq2Seq(**ck["cfg"])
    model.load_state_dict(ck["state"])
    return model.to(device).eval(), CharVocab(ck["chars"]), ck.get("meta", {})


def train_model(train_pairs, val_pairs, out_path, epochs=60, batch_size=64, lr=2e-3, emb=64, hid=128,
                drop=0.2, seed=0, device="auto", patience=12, log=print):
    """train_pairs / val_pairs: lists of (noisy, canonical). Returns (model, vocab, history)."""
    random.seed(seed)
    torch.manual_seed(seed)
    dev = pick_device(device)
    vocab = CharVocab.build([w for pair in train_pairs for w in pair])
    model = Seq2Seq(len(vocab), emb, hid, drop).to(dev)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, factor=0.5, patience=3)
    n_par = sum(p.numel() for p in model.parameters())
    log(f"[seq2seq] device={dev}  params={n_par:,}  train={len(train_pairs)}  val={len(val_pairs)}")

    val_words = [v for v, _ in val_pairs]
    val_gold = [c for _, c in val_pairs]
    best_acc, best_state, bad, history = -1.0, None, 0, []
    t0 = time.time()
    for ep in range(1, epochs + 1):
        model.train()
        order = list(train_pairs)
        random.shuffle(order)
        tf = max(0.5, 1.0 - ep / epochs)             # slowly reduce teacher forcing
        total, nb = 0.0, 0
        for i in range(0, len(order), batch_size):
            src, lens, tgt = make_batch(vocab, order[i:i + batch_size], dev)
            logits = model(src, lens, tgt, teacher_forcing=tf)
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), tgt[:, 1:].reshape(-1), ignore_index=PAD)
            opt.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            total += loss.item()
            nb += 1
        model.eval()
        norm = NeuralNormalizer(model, vocab, dev)
        val_acc = word_accuracy(norm.normalize_words(val_words), val_gold) if val_pairs else 0.0
        sched.step(total / nb)
        history.append({"epoch": ep, "loss": total / nb, "val_word_acc": val_acc})
        if ep == 1 or ep % 5 == 0:
            log(f"[seq2seq] epoch {ep:3d}  loss {total / nb:.4f}  val word-acc {val_acc:.3f}  ({time.time() - t0:.0f}s)")
        if val_acc > best_acc:
            best_acc, bad = val_acc, 0
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        else:
            bad += 1
            if bad >= patience:
                log(f"[seq2seq] early stop at epoch {ep} (best val acc {best_acc:.3f})")
                break
    model.load_state_dict(best_state)
    model.eval()
    save_checkpoint(out_path, model, vocab, {"best_val_word_acc": best_acc, "epochs_run": len(history)})
    Path(out_path).with_suffix(".history.json").write_text(json.dumps(history, indent=1))
    log(f"[seq2seq] saved {out_path}  (best val word-acc {best_acc:.3f})")
    return model, vocab, history
