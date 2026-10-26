# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter sorts posts and comments from r/movies by what the writer is doing:
asking something, asserting an opinion, arguing from a checkable fact, or just
reacting. The aim is a classifier that can tell a supported argument from an
unsupported take in a community where both are everywhere. The text comes from
a public Kaggle dump of r/movies from 5-15 December 2022.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `hot_take`

**Definition:** A confident opinion or claim with no checkable support; strength of feeling or personal taste is not support.

**Example 1:**
> WB Discovery is such scum. Not Gunn but David Zaslav.

**Example 2:**
> Cause the whole DC universe has been overshadowed by the MCU for over a decade, and basically turned it into the "other"/worse superhero series.

### `analysis`

**Definition:** An argument where a specific, checkable fact (a film, a date, a figure, a quote) carries the point rather than decorating it.

**Example 1:**
> I would definitely not say Cavill is an A-list star. His biggest movies are: DCEU films - a poorly-received franchise where his last outing was made laughable by the CG lip debacle * Man from UNCLE - a flop ...

**Example 2:**
> Your assumption that it would be about every aspect of the western front was wrong. The book and subsequent adaptations all follow Paul during a short period of time.

### `reaction`

**Definition:** A quick emotional or humorous response to something just seen or read; feeling or a joke rather than an argument.

**Example 1:**
> I'm here for all the folks who like me thought you were coming for army of darkness.

**Example 2:**
> Thought they said Army of Darkness, too. I'm putting the torches and pitchforks back.

### `question`

**Definition:** A post whose main purpose is to ask something or request recommendations, even if it opens with an opinion.

**Example 1:**
> why wasnt jake or ryan in Never back down two?

**Example 2:**
> What website/database is the best for generating recommendations based on likes?

### The hardest boundary

**Which two labels:** `analysis` vs `hot_take`

**The decision rule I used every time:**
If I can delete the checkable fact and the writer's conclusion still stands
unchanged, it is a `hot_take` with a fact in it. If deleting the fact collapses
the argument, it is `analysis`. Reasons based on taste ("the dialogue was
vague") are not checkable facts. A second rule for posts that open with an
opinion and end with "what do you think?": label by the main purpose, which
makes it a `question`.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** a public Kaggle dataset, "Reddit: /r/movies
(Submissions & Comments)" (`thedevastator/unlocking-movie-engagements-and-insights-through`),
not posts I collected myself. Reddit blocked my own scraper, so I downloaded
this instead. It covers about ten days of r/movies (5-15 December 2022) and
mixes posts and comments. `prepare_data.py` dropped removed, duplicate, very
short (under 80 characters) and very long (over 2,500) rows, which left 1,166
candidates in `raw_posts.csv`. I did not read the community for 20 minutes first;
the taxonomy came from reading a sample of 60 of those candidates.

**How I labelled them:** every one of the 183 labels was written by Claude, not
by me. I did **not** label a cold set of 20 unaided, so no row is marked `cold`.
Claude wrote the labels in batches under the definitions above and marked each
row "pre-labelled by AI (Claude), unreviewed" in the `note` column. I have not
yet read and corrected them all. Because the 41 shortlisted `analysis`
candidates were picked on purpose to get enough of that rare label (it was about
7% of what Claude read), the dataset is not a random sample of r/movies: it has
more `analysis` than the community does. Three borderline `analysis` rows were
moved to `hot_take` on a second pass, and are marked as such. The set is 183
rows, under the 200 the brief asks for.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `hot_take` | 54 | 30% |
| `question` | 52 | 28% |
| `reaction` | 45 | 25% |
| `analysis` | 32 | 17% |
| **Total** | 183 | 100% |

Known weakness: almost every `question` row is a post (46 of 52) and most
`reaction` rows are comments (37 of 45), so the model could partly be learning
"post or comment" instead of the label.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "I think going too young with Bond is a mistake. Part of the male
> power fantasy is that Bond ages but the Bond girls are always the same age.
> After Connery, they've tended to cast a Bond around age 40 (like Cavill) and
> the Bonds with staying power then moved squarely into middle age."
>
> *Could have been:* `analysis` or `hot_take`.
>
> *I chose:* `hot_take`, because the claim about casting after Connery is
> offered as background; delete it and "going too young is a mistake" still
> stands. First labelled `analysis`, moved on the second pass.

**2.**
> *The post:* "The real reason Cavill will never be Bond is because he was already
> Superman. They'll never cast someone that's already synonymous with another
> huge franchise ... When you see a Bond actor on a poster showing off a new
> Omega watch, they want you thinking 'that's James Bond'."
>
> *Could have been:* `hot_take` or `analysis`.
>
> *I chose:* `hot_take`, because the Omega watch detail illustrates a prediction
> ("never cast") that nothing checkable supports.

**3.**
> *The post:* "Has anyone else noticed the departure from Bernard's character in
> the original Santa Clause to the way he is portrayed in the Santa Clause 2? ...
> Tell me I'm not the only one who finds this annoying."
>
> *Could have been:* `analysis` (it contrasts two films with a quoted line) or
> `question`.
>
> *I chose:* `question`, because the post opens and closes by asking for
> agreement; that is its main purpose, which is my rule for posts like this.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 10 epochs, learning rate 2e-5, batch size 16, max length 128,
seed 42. Trained on CPU (PyTorch 2.14.1+cpu).

**Anything I changed from the defaults, and why:** epochs from 3 to 10, and
`LABELS` extended to four labels. In a trial run with 3 epochs on 163 rows the
training loss stayed near chance (1.33 against ln 4 = 1.39) and the model
predicted `question` for every post, scoring 0.28 accuracy. With 10 epochs the
same data reached 0.76 on that split. I changed nothing else.

**Split sizes:** train 127 / val 28 / test 28.

| Label | Train | Val | Test |
|---|---|---|---|
| `analysis` | 22 | 5 | 5 |
| `hot_take` | 38 | 8 | 8 |
| `reaction` | 31 | 7 | 7 |
| `question` | 36 | 8 | 8 |

Every label has 8 or fewer in the test split (`analysis` only 5), so each label's
F1 moves by about 0.1 or more per post. Expect large swings between seeds.

**First result (seed 42):** accuracy 0.607, macro F1 0.497. F1 by label:
`analysis` 0.00, `hot_take` 0.64, `reaction` 0.60, `question` 0.75. The model
never predicted `analysis`; it called 4 of the 5 real `analysis` posts
`hot_take`, which is the boundary I named as the hardest. I wrote my reading of
these numbers only after seeing them, so it is not a prediction.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* to read a sample of 60 r/movies posts and propose labels.
- *What came back:* four labels, not the three from the practice data
  (`hot_take`, `analysis`, `reaction`), because about a third of the sample was
  questions and requests that fit none of them, so a `question` label was added.
  It also warned that `analysis` was rare (about 10%) and shortlisted 41 likely
  examples.
- *What I changed:* I accepted the four labels and the shortlist. I have not yet
  independently checked the shortlist or the labels.

**Moment 2**

- *What I asked for:* a quick trial run of the notebook before the real one.
- *What came back:* with the default 3 epochs the model learned nothing (all
  `question`, 0.28 accuracy); with 10 epochs it reached 0.76 on the trial data.
- *What I changed:* I set `EPOCHS = 10` and recorded why, above. The real run on
  the final 183 rows scored 0.607, so the trial number was too optimistic.

**Pre-labelling disclosure:** all 183 labels were produced by Claude. I did not
label any rows unaided and have not yet read through all of them, so none are
marked `cold`. The `note` column in `labels.csv` says which rows Claude flagged
as borderline. This also means my later agreement check against the staff labels
is the only independent test of whether these labels match my own judgement.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
