# Task Gravity — Submission Package

> **Suggested next venue**: CICAI 2026 (中文投稿) or AAAI Spring
> Symposium 2027 (英文投稿). See `venues.md` for full list.

This directory contains everything needed to submit Task Gravity to a
workshop or main conference. The package is **self-contained**:
unzip, run the supplementary's quick-reproduction commands, and you
have every figure and table in the paper.

## Files in this directory

| File | Purpose | When to use |
|------|---------|------------|
| `paper.md` (or `paper.html`) | Camera-ready paper source | T-1 week |
| `cover_letter.md` | English cover letter | International venues |
| `cover_letter_zh.md` | 中文投稿信 | 国内会议 |
| `keywords.md` | Keywords + author bio + data availability | All venues |
| `open_problems.md` | 6 concrete follow-ups | Position-paper appendix |
| `venues.md` | Target submission venues + defensive talking points | Pre-submission |
| `checklist.md` | T-2w / T-1w / T-0 / T+1w checklist | Operational |
| `supplementary/` | Self-contained reproducibility package | Upload as zip |
| `supplementary.zip` | Compressed version of above | Upload to OpenReview etc. |

## Three-line quick start

```bash
# 1. (Optional) verify the supplementary reproduces
cd supplementary && pip install -r requirements.txt
cd experiment/tabular && python -u -m src.experiment
cd ../deep && python -u -m src.run --timesteps 10000

# 2. Pick a venue from venues.md

# 3. Follow checklist.md for the submission timeline
```

## What to read first

- **If you have 5 minutes:** Read `cover_letter.md` (or `_zh.md`).
- **If you have 30 minutes:** Read `paper.md` (`paper/position/paper.md` in the
  parent) and skim the figures in `supplementary/experiment/.../results/`.
- **If you have 2 hours:** Read everything in this directory and the
  parent `paper/`.

## Common questions

> *Is this paper ready to submit?*

Yes for a **workshop** or **position-paper track**. Not yet for a
**main conference** — main conferences expect benchmark-level
experimental results, which requires running Open Problem OP-3
(64-task corpus).

> *What's the main risk for the paper?*

A reviewer may say "this is just reward hacking under another name."
The defensive talking points in `venues.md` and `cover_letter.md`
address this directly. The strongest version of the response is
"we add (i) a formalization, (ii) a metric, and (iii) a falsifiable
bridge to human compulsion — none of which exist in the reward-hacking
literature."

> *What's the deadline pressure?*

Based on 2026-07-22, no major venue is in active submission for
position papers. Use this time to:
1. Get the paper on arXiv (locks timestamp, builds citation base).
2. Polish the position paper based on early feedback.
3. Build the OP-3 64-task corpus for the main-conference push.

See `venues.md` for the suggested timeline.