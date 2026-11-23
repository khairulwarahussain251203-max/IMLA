# Imla (املا): Roman Urdu Text Normalization

## Quick start (Windows PowerShell)
```powershell
cd IMLA
pip install -r requirements.txt
python check_lexicon.py     # optional: checks the 1,391-word vocabulary
python run_all.py           # trains the seq2seq model (slower now), writes models/ and results/
python gui.py               # opens the Imla app at http://127.0.0.1:8765
```
`data/` and `results/` already hold a baseline-only run on the new vocabulary, so `python gui.py --no-neural`
works immediately (dictionary mode). Run `python run_all.py` once to train the model and unlock seq2seq mode.
`python run_all.py --variants-per-word 10` trains faster.

Maps messy Roman Urdu spellings to one standard form (*acha / achha / accha / acchaa -> acha*).

```
roman_urdu_normalizer/
  run_all.py            one command runs everything
  check_lexicon.py      checks the vocabulary for clashes before you retrain
  demo.py               type a sentence in the terminal, see it normalized
  gui.py + gui/         graphical app (opens in your browser) for presentations
  proposal.md           problem, research gap, spelling convention, evaluation plan
  ru_norm/
    lexicon.py          first two vocabulary blocks (~450 words) + the reserved unknown-word test list
    lexicon_more.py     third block, ~940 more words (verbs, food, tech, religion, sports, code-mixed English ...)
    data_gen.py         noise generator, (variant -> canonical) pairs, splits, synthetic reviews
    phonetic.py         consonant-skeleton phonetic key
    editdist.py         Levenshtein, word accuracy, CER
    cluster.py          clustering pipeline: raw corpus -> clusters to review -> pairs.csv
    baselines.py        rule-based, variant lookup table, edit-distance dictionary
    seq2seq.py          char-level BiGRU encoder + attention GRU decoder + confidence gate (PyTorch)
    experiments.py      calibration, intrinsic + extrinsic evaluation, plots
  data/                 generated pairs, splits, clustering demo output
  results/              CSV tables + PNG charts
  models/               seq2seq.pt appears here after training
```

## Run
```bash
pip install -r requirements.txt
python run_all.py                  # trains the seq2seq model (CPU is fine) and evaluates everything
python run_all.py --skip-neural    # baselines + experiments only, no torch needed
python run_all.py --skip-train     # reuse models/seq2seq.pt (the gate is re-tuned each run)
python demo.py
```
Training uses about 4k pairs and ~0.4M parameters; expect roughly 5 to 8 minutes on a laptop CPU
(`--epochs 60` with early stopping).

## Vocabulary
About 1,390 canonical words in three blocks (`lexicon.py`: core words and first extension, `lexicon_more.py`:
second extension). Coverage: pronouns, postpositions and connectors; verb stems and the common inflected forms
(*karunga, jayegi, dekhte, milegi*); adjectives and adverbs; body, health, family and people; home, food and
drink; places and travel; time and numbers; school and work; social media, tech and shopping; money; feelings
and abstract nouns; religion and culture; sports; and code-mixed English (*problem, thankyou, awesome*).
Each word has 2 to 4 hand-written variants plus up to 16 generated ones (about 20,000 pairs in total).

The 118 words in `OOV_WORDS` (*mausam, bijli, hospital ...*) are deliberately **not** in the vocabulary.
They are the "unknown word, must stay unchanged" test set, so do not add them to the lexicon.

Run `python check_lexicon.py` after editing the lexicon. It reports ambiguous variants, variants that are
also canonical words, clashes with the reserved unknown-word list and the final pair counts.

**After changing the vocabulary you must rerun `python run_all.py`** so `data/`, `models/seq2seq.pt` and
`results/` match the new lexicon (the GUI reads its vocabulary from `data/pairs.csv`). With about 13k training
pairs, CPU training takes longer than before. `--variants-per-word 10` makes it roughly 35% faster.

## Confidence gate (leaves unknown words alone)
A plain seq2seq model always produces *something*, so a word outside its vocabulary such as *kitab*
(before it was added) could come out as *khtab*. The gate fixes this in two steps:
1. a word that is already a standard vocabulary word is returned unchanged;
2. otherwise the model's confidence in its own output is checked, and if it is below a threshold the
   original word is returned.

The threshold is tuned on validation data only (objective: word accuracy on held-out variants plus
the share of unknown words left untouched). The dictionary baseline's distance threshold is tuned the
same way, and a loose setting (0.5) is also reported to show the trade-off.

## Graphical app (Imla)
```bash
python gui.py              # opens http://127.0.0.1:8765 in your browser
python gui.py --no-neural  # rule-based + dictionary only (no torch needed)
```
A local web app (Python standard library plus `gui/index.html`); nothing leaves your computer.
* **Live demo:** output updates as you type, misspelled words morph into the standard form; example chips included.
* **Spelling cluster:** click a word to see its known spellings converge on the standard form, with the model's top guesses.
* **System comparison:** rule-based vs dictionary vs seq2seq, with a note when the model protects an unknown word.
* **Why normalize:** sentiment on raw vs normalized text, plus the headline accuracy from `results/`.
* **Share card:** saves a before/after PNG for posts. **Results tab:** evaluation bar charts. Light/dark theme.
* To rename the app, change `APP_NAME` at the top of `gui.py`.

## What each evaluation measures
* **`test_variants`:** new spellings of words seen in training.
* **`test_words`:** spellings of words never seen in training (a dictionary cannot know them).
* **`test_oov`:** everyday words that are not in the vocabulary. The correct output is the word itself,
  so `word_acc` here means the share of unknown words left untouched.
* **Extrinsic:** sentiment accuracy using TF-IDF + logistic regression on raw vs normalized text
  (5 random seeds, 200 train / 600 test reviews). "oracle" = gold normalization, the upper bound.

## Results of the baselines (seed 0, earlier 425-word run; rerun for current numbers)
| system | unseen variants | unknown words kept | sentiment acc |
|---|---|---|---|
| raw | 0.000 | 1.000 | 0.706 |
| rule-based | 0.238 | 0.898 | 0.799 |
| variant lookup table | 0.000 | 1.000 | 0.934 |
| edit-distance dictionary (tuned) | 0.620 | 0.831 | 0.898 |
| edit-distance dictionary (loose 0.5) | 0.926 | 0.136 | 0.987 |
| oracle | - | - | 1.000 |

The dictionary shows the trade-off: a loose threshold fixes most variants but mangles 86% of unknown
words; a tight threshold protects unknown words but misses many variants. The seq2seq rows are written
to `results/intrinsic.csv` and `results/extrinsic.csv` when you run `python run_all.py`, so use your own
numbers in the report.

**Read these numbers carefully.** The synthetic variants come from edit-style rules, which is what an
edit-distance dictionary is good at, so its loose-setting score is optimistic (0.908 on the
hand-written variants vs 0.930 on generated ones). On unseen words a dictionary cannot work at all.

## Using real data (recommended for the final report)
1. Put real Roman Urdu text (reviews, tweets, comments), one per line, in a file.
2. `python -m ru_norm.cluster --input my_corpus.txt --out data/clusters_for_review.csv`
3. Open the CSV, fill `approved_canonical` where the suggestion is wrong or the cluster mixes words.
4. `python -m ru_norm.cluster --to-pairs data/clusters_for_review.csv --pairs-out data/my_pairs.csv`
5. `python run_all.py --pairs data/my_pairs.csv --sentiment-csv my_labelled.csv`  (`text,label` columns, label 0/1)

To add vocabulary to the built-in set, append lines like `kitab: kitaab ketab` to `LEX_MORE` in
`ru_norm/lexicon_more.py`, run `python check_lexicon.py`, then rerun `python run_all.py`.

## Known limitations
* Vocabulary is ~1,390 words, not tens of thousands; extend `lexicon_more.py` or use the clustering route above.
* Words are normalized in isolation (no sentence context); ambiguous strings are dropped from the dataset.
* Synthetic sentiment reviews are template-based; the extrinsic gain on real text will be smaller.

<img width="1330" height="646" alt="image" src="https://github.com/user-attachments/assets/3e21d3dd-0475-43e3-bb61-502b43db08b3" />
<img width="1328" height="406" alt="image" src="https://github.com/user-attachments/assets/8db0f8b2-f10d-414a-bc73-66031c1d21fb" />
<img width="1248" height="561" alt="image" src="https://github.com/user-attachments/assets/0fbd3d97-f68a-4537-bd70-fb6ef8a4e631" />
<img width="757" height="585" alt="image" src="https://github.com/user-attachments/assets/90a6a8a6-4df1-49c3-9bd3-233efc1e9df7" />
<img width="1305" height="508" alt="image" src="https://github.com/user-attachments/assets/95d0a3a2-8436-4f86-a5fa-40b35fe29e1c" />

