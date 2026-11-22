"""
Step 1 of the project: build the (variant -> standard) dataset.

    raw Roman Urdu text  ->  token counts  ->  cluster look-alike spellings
                         ->  CSV with a SUGGESTED canonical form per cluster
                         ->  human fixes the `approved_canonical` column
                         ->  pairs.csv  (variant, canonical)

Clustering = union-find over two kinds of evidence
  (a) same phonetic key (consonant skeleton) and small edit distance
  (b) very small edit distance, same first letter, similar length

CLI
  python -m ru_norm.cluster --input corpus.txt --out data/clusters_for_review.csv
  python -m ru_norm.cluster --to-pairs data/clusters_for_review.csv --pairs-out data/pairs.csv
"""
import argparse
import csv
import re
from collections import Counter, defaultdict

from .editdist import norm_distance
from .phonetic import phonetic_key

_TOKEN = re.compile(r"[a-z]+")


def count_tokens(lines):
    c = Counter()
    for line in lines:
        c.update(_TOKEN.findall(line.lower()))
    return c


class _UF:
    def __init__(self, items):
        self.p = {i: i for i in items}

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def cluster_tokens(counts, min_count=2, block_thr=0.5, fuzzy_thr=0.25, min_len_fuzzy=4):
    words = [w for w, c in counts.items() if c >= min_count and len(w) >= 2]
    uf = _UF(words)

    # (a) phonetic blocks
    blocks = defaultdict(list)
    for w in words:
        blocks[phonetic_key(w)].append(w)
    for ws in blocks.values():
        for i in range(len(ws)):
            for j in range(i + 1, len(ws)):
                if norm_distance(ws[i], ws[j]) <= block_thr:
                    uf.union(ws[i], ws[j])

    # (b) cross-block fuzzy merge for longer words (bucket by first letter)
    by_first = defaultdict(list)
    for w in words:
        if len(w) >= min_len_fuzzy:
            by_first[w[0]].append(w)
    for ws in by_first.values():
        ws.sort(key=len)
        for i in range(len(ws)):
            for j in range(i + 1, len(ws)):
                if len(ws[j]) - len(ws[i]) > 2:
                    break
                if norm_distance(ws[i], ws[j]) <= fuzzy_thr:
                    uf.union(ws[i], ws[j])

    groups = defaultdict(list)
    for w in words:
        groups[uf.find(w)].append(w)
    clusters = []
    for members in groups.values():
        members.sort(key=lambda w: (-counts[w], len(w), w))
        clusters.append({
            "suggested": members[0],                  # most frequent, then shortest
            "members": members,
            "total": sum(counts[w] for w in members),
        })
    clusters.sort(key=lambda c: -c["total"])
    for i, c in enumerate(clusters):
        c["id"] = i
    return clusters


def write_review_csv(clusters, counts, path, min_members=2):
    """Only clusters with >=2 spellings need human attention."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cluster_id", "suggested_canonical", "approved_canonical", "n_variants", "total_count", "variants"])
        for c in clusters:
            if len(c["members"]) < min_members:
                continue
            w.writerow([c["id"], c["suggested"], "", len(c["members"]), c["total"],
                        ";".join(f"{m}:{counts[m]}" for m in c["members"])])


def review_csv_to_pairs(csv_path, pairs_path):
    """approved_canonical (if filled) overrides suggested_canonical."""
    n = 0
    with open(csv_path, encoding="utf-8") as f, open(pairs_path, "w", newline="", encoding="utf-8") as g:
        w = csv.writer(g)
        w.writerow(["variant", "canonical", "source"])
        for row in csv.DictReader(f):
            canon = (row["approved_canonical"] or row["suggested_canonical"]).strip()
            for item in row["variants"].split(";"):
                v = item.rsplit(":", 1)[0]
                if v and v != canon:
                    w.writerow([v, canon, "clustered"])
                    n += 1
    return n


def evaluate_clusters(clusters, counts, gold_map):
    """
    Only possible when gold labels exist (our synthetic data).
      purity         : share of token mass that belongs to the majority gold word of its cluster
      suggested_ok   : share of token mass whose cluster-suggested canonical is exactly the gold canonical
                       (strict: the most frequent spelling is not always the standard one, which is why a
                       human review step exists)
    """
    tot = pure = ok = 0
    for c in clusters:
        mass = Counter()
        for m in c["members"]:
            mass[gold_map.get(m, m)] += counts[m]
        pure += mass.most_common(1)[0][1]
        tot += sum(mass.values())
        ok += mass.get(c["suggested"], 0)
    return {"purity": pure / max(tot, 1), "suggested_ok": ok / max(tot, 1), "n_clusters": len(clusters)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="plain-text file, one comment/review per line")
    ap.add_argument("--out", default="data/clusters_for_review.csv")
    ap.add_argument("--min-count", type=int, default=2)
    ap.add_argument("--to-pairs", help="reviewed clusters CSV -> pairs CSV")
    ap.add_argument("--pairs-out", default="data/pairs_from_clusters.csv")
    a = ap.parse_args()
    if a.to_pairs:
        print(f"wrote {review_csv_to_pairs(a.to_pairs, a.pairs_out)} pairs to {a.pairs_out}")
        return
    with open(a.input, encoding="utf-8") as f:
        counts = count_tokens(f)
    clusters = cluster_tokens(counts, min_count=a.min_count)
    write_review_csv(clusters, counts, a.out)
    print(f"{len(counts)} distinct tokens -> {len(clusters)} clusters; review file: {a.out}")


if __name__ == "__main__":
    main()
