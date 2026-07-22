# Submission Package — Final Checklist

This is the master checklist for submitting Task Gravity. Tick each box
before pressing "submit".

## Pre-submission (T-2 weeks)

- [ ] Decide target venue (default: **CICAI 2026** for Chinese, **AAAI Spring Symposium 2027** for English).
- [ ] Confirm CFP page URL and update `venues.md`.
- [ ] Confirm page limit (typically 4–6 pages for position papers).
- [ ] Confirm reference style required (IEEE / ACM / LNCS / 自定).
- [ ] Confirm submission format (PDF / DOCX / 双盲 / 单盲 / 公开署名).
- [ ] Confirm supplementary policy (是否允许 zip / 链接 / GitHub).
- [ ] Confirm author anonymization policy (single-blind 需去掉身份信息).

## Manuscript (T-1 week)

- [ ] Paper source: `paper/position/paper.md` — 编辑定稿。
- [ ] Paper word count ≤ venue limit (not counting references).
- [ ] Abstract ≤ venue limit (typically 150–250 words).
- [ ] Keywords: English + 中文版在 `keywords.md`。
- [ ] Author block: 姓名、单位、邮箱、ORCID (如有)。
- [ ] All figures embedded with proper captions.
- [ ] All tables in venue's required format.
- [ ] References: BibTeX or venue format; check for venue's required style.
- [ ] No LLM co-author (per ICML 2026 rule; conservative even if not required).
- [ ] Acknowledge any funding source (we have none).

## Cover letter (T-1 week)

- [ ] Use `cover_letter.md` (English) or `cover_letter_zh.md` (中文).
- [ ] Fill in actual author name(s) and contact.
- [ ] Sign with date.
- [ ] Attach as separate file if venue allows; otherwise paste into form.

## Supplementary (T-3 days)

- [ ] `supplementary/experiment/` is complete and self-contained.
- [ ] `supplementary/README.md` explains reproduce-in-3-steps.
- [ ] `supplementary/requirements.txt` lists exact versions.
- [ ] Zip everything into one file `task_gravity_supplementary.zip`.
- [ ] Verify md5 checksum of zip.

> Reference checksum for v2 (2026-07-22): **MD5 = 09C1BB8D8C4B50296DC979E7AFF8EBDC**, 695 KB.
>
> v2 change: included `paper.pdf` (10 pages, 459 KB) as `paper/position/paper.pdf` in the supplementary zip. v1 had only `paper.md` and `paper.html`; v2 adds the rendered PDF that reviewers actually open.

## Submission (T-0)

- [ ] Upload PDF + supplementary zip (or GitHub link).
- [ ] Save submission confirmation email.
- [ ] Note submission ID in `venues.md` for tracking.
- [ ] Post on arXiv (separate action) to lock timestamp.

## Post-submission (T+1 week)

- [ ] Add entry to personal calendar for camera-ready deadline.
- [ ] Prepare rebuttal template (use 防御性话术 in `venues.md`).
- [ ] If rejected, copy review and update paper for next venue.

## Single-shot quick submission (e.g., openreview)

If the venue uses OpenReview, you can submit by:

1. Replace `paper.md` with single-column LaTeX (`paper.tex`).
2. Run `tar czf submission.tgz paper.pdf cover_letter.pdf supplementary/`.
3. Upload via OpenReview's submission form.
4. Authors: fill in order, affiliation, email, ORCID.
5. Conflicts: declare any collaborators in last 3 years.
6. Submit.

---

## Common pitfalls we have already avoided

1. **Naming the phenomenon vs. just observing it.** A common rejection
   reason is "you observed something but didn't isolate it." Our
   *formalization* (Langevin SDE + gravity operator) is the
   distinguishing contribution.
2. **Metrics without validation.** Both TRR and CTRR have been
   measured on real agents (tabular + PPO) and shown to produce
   non-trivial, monotonic, noise-responsive values.
3. **Over-claiming.** We do not claim Task Gravity is a complete
   theory of compulsive behavior. We claim a *vocabulary, two metrics,
   and a falsifiable bridge.* Reviewers respect this calibration.

## What to do if a reviewer asks for the code

If the venue does not allow supplementary material, link to the
public GitHub repository (create one and update `supplementary/README.md`).

## What to do if a reviewer asks for more tasks

Point them to Open Problem OP-3 (64-task corpus). If you have time
before the rebuttal, generate the additional results and append them
as an "Extended Empirical Note" (1–2 pages).