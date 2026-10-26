# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy of at least 0.60 on every seed

The fine-tuned model gets at least 0.60 accuracy on the held-out set in each of
the three seeds, not on average.

**Why this target:** I have four labels, so a random guesser gets about 25%, and
always guessing the biggest label (`question` or `hot_take`, about 28% each)
gets about 28%. 0.60 is more than double either, which is where I would call
the model useful for sorting r/movies posts. I did not pick 0.70 because my
labels have a soft boundary (`analysis` vs `hot_take`) and I only have about 180
examples; a test split of about 27 posts means one wrong post moves accuracy by
almost 4 points.

---

## 2. Every label has an F1 of at least 0.50 on every seed

No label may fall below 0.50 F1 on the held-out set in any of the three seeds.

**Why this target:** this is looser than the overall target on purpose. Each
label has only about 5 posts in the test split (my smallest, `analysis` and
`reaction`, have 35 and 37 labelled examples), so a single mistake swings that
label's F1 by 0.1 or more. 0.50 still catches a label the model has given up on.
The one I expect to fail is `analysis`, because it is the label most often
confused with `hot_take`.

---

## 3. Beat the zero-shot baseline by at least 10 accuracy points

On the same `test_split.csv`, the trained model's accuracy is at least 0.10
higher than the zero-shot baseline run with only my label definitions.

**Why this target:** the point of fine-tuning on 180 posts is that it learns
something the definitions alone do not. If it is within a few points of the
baseline, I trained for nothing. Ten points is more than the noise from a
27-post test split (about 4 points per post), so a smaller gap would not be
distinguishable from luck. My definitions say `analysis` needs a "checkable
fact", which a general model may apply well, so I do not expect an easy win.

---

## 4. At least 0.70 agreement with the staff labels

On the 30 staff posts, labelled under the staff taxonomy, I agree with staff on
at least 70% of them.

**Why this target:** this is my check that I can apply a written rule the way
its authors did, and it is the only evidence I have about whether my own labels
are consistent. Chance with three labels is about 33%. I chose 0.70 rather than
0.90 because the staff set has a different taxonomy from mine and its
`analysis` / `hot_take` boundary is the same one I find hardest. Most of my
labels were pre-labelled by AI and then reviewed by me, so I want an independent
check on my own judgement.

---

## 5. Accuracy varies by no more than 0.10 across the three seeds

The gap between my best and worst seed is at most 0.10 accuracy.

**Why this target:** the project warns that a dataset too small or lopsided gives
unstable scores. With about 27 test posts and about 130 training posts, I expect
some swing, so I will not ask for it to be tiny. A spread above 0.10 (about 3
posts) would mean the results are not stable enough to trust any other criterion
in this file.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
