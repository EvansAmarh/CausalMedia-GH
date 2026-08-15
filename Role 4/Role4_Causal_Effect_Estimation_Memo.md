# Role 4 Memo: Causal Effect Estimation

**Purpose:** Consolidates every estimation result produced for the OULAD primary corpus, with the exact configuration used for each, so results are traceable and reproducible. This is the artifact the manuscript's Results section should draw from directly.

**Status: COMPLETE.** Model specification corrected mid-session (Section 0); all downstream results (SHAP, refutation tests, heterogeneity checks) have been re-run on the corrected model and are cross-referenced from Role 5's memo, which now contains their final values.

**Corpus used throughout:** `oulad_full_corpus.csv` (N=17,529, treatment=`oucontent_clicks`, outcome=`performance_gain`, winsorized). GGG absent from all 6/7 modules represented — see Role 1 memo, Section 3.2b.

---

## 0. Confounder Specification Correction (read this first)

An initial round of estimation (Sections 2, 5, 7 below) used the confounder set specified in Role 3's original DAG memo: `region`, `imd_band`, `highest_education`, `age_band`, `gender`, `disability`, `code_presentation`, `num_of_prev_attempts`, `studied_credits`. **This set omitted `code_module`** (which of OULAD's 6 represented courses a student took) — a genuine specification gap in Role 3's original DAG, not caught until a SHAP-driven investigation into gender heterogeneity forced a check.

**Discovery path:** SHAP analysis on the original model ranked `gender_M` as by far the most important feature. Investigation confirmed a large, apparent gender gap in CATE (rank-biserial r=−0.489, p<2.2×10⁻¹⁶). Checking whether this was confounded by module composition (gender is heavily imbalanced across modules — BBB 88.7% female, FFF 82.0% male) revealed that `code_module` had never been included as a confounder anywhere in the pipeline, despite LOGO-CV already showing module identity drives substantial ATE variation.

**Refitting with `code_module` added changed the headline ATE from 0.0026 to 0.0048 — an 85% shift.** This is the canonical, corrected specification used throughout this memo (`X_encoded_v2`, 40 columns, saved as `cf_canonical_model.pkl`). The uncorrected model's numbers are not reported below except where explicitly noted for before/after comparison — do not cite the earlier 0.0026-based figures anywhere in the manuscript.

**Role 3's DAG memo has been updated** to add `code_module` as a fifth confounder block ("Course Identity"), with a correction note explaining the discovery.

---

## 1. Metric Decision

AUC-PR and Brier score were dropped for the OULAD analysis — both require binary ground-truth labels that don't exist for real students under the fundamental problem of causal inference. Individual-level accuracy is validated via Role 2's IHDP benchmark (PEHE); OULAD results are reported via ATE, confidence intervals, and formal statistical tests.

---

## 2. Baseline Progression (Corrected: `code_module` included, 40-column confounder matrix)

| Estimator | Effect (per `oucontent` click) | 95% CI |
|---|---|---|
| OLS | 0.0049 | — |
| Linear DML | 0.0037 | [0.0027, 0.0047] |
| **CausalForestDML (proposed)** | **0.0048** | **[0.0026, 0.0070]** |

**Note:** Linear DML (0.0037) sits noticeably below both OLS and CausalForestDML — the three estimators no longer agree as closely as under the uncorrected specification. A plausible explanation for Discussion (stated as plausible, not confirmed): Linear DML's linear-in-confounders assumption fits less well once a 6-level module confounder with genuinely heterogeneous per-module effects is included — exactly the kind of heterogeneity CausalForestDML is designed to handle better.

**Pearson/naive correlation** (unconditional on any confounder set, not recomputed): r=0.0794, p=6.1×10⁻²⁶.

---

## 3. Ground-Truth Validation (Cross-Reference)

Full detail in `Role2_Ground_Truth_Validation_Memo.md`. IHDP validation is independent of OULAD's confounder set and required no re-run after the correction.

---

## 4. Subgroup Heterogeneity — Full Results in Role 5 Memo

All three heterogeneity checks (gender, `highest_education`, `imd_band`) are complete on the corrected model and documented in full in `Role5_Evaluation_Explainability_Memo.md`, Section 3. Summary:

| Variable | Effect size | Pattern | Role in Results |
|---|---|---|---|
| **`highest_education`** | ε²=0.0712 (medium) | Clean, monotonic decline from peak | **Primary heterogeneity finding** |
| `imd_band` | ε²=0.0247 (small) | No clear gradient | Secondary |
| Gender | r=−0.170 (small-moderate) | Real but modest after correction | Secondary |

**Gender is the finding that triggered the `code_module` discovery** (Section 0) — under the uncorrected model it appeared dominant (r=−0.489); after correction it dropped to small-moderate (r=−0.170), revealing the original apparent gap was substantially, though not completely, a module-composition artifact. `highest_education` moved in the opposite direction after correction (ε²=0.009 → 0.071), making it the paper's actual strongest, most interpretable heterogeneity result — see Role 5 memo for full detail on all three.

---

## 5. Leave-One-Module-Out Cross-Validation (Corrected)

| Held-out module | Train ATE | Held-out ATE |
|---|---|---|
| AAA | 0.0052 | 0.0051 |
| BBB | 0.0046 | 0.0044 |
| CCC | 0.0057 | 0.0056 |
| DDD | 0.0048 | 0.0051 |
| EEE | 0.0043 | 0.0039 |
| FFF | 0.0025 | 0.0022 |

**FFF's earlier negative result is resolved.** Under the uncorrected model, FFF showed a consistent negative effect (train −0.0029, held-out −0.0021). Under the corrected model, **FFF is positive** (0.0025/0.0022) — smallest of the six modules, but consistent in sign with all others. The original negative result is understood to have been an artifact of the missing `code_module` confounder. **All six modules now agree on effect direction.** Visualized in `figure_cv_stability.png` (Role 5 memo, Section 4).

---

## 6. DoWhy Refutation Tests — Full Results in Role 5 Memo

All four tests re-run on the corrected model; full results and the honest bootstrap-attenuation caveat are in `Role5_Evaluation_Explainability_Memo.md`, Section 2. Summary: three of four tests (placebo, random common cause, data subset) pass cleanly with deviations under 2%. The bootstrap refuter shows a reproducible ~42–46% attenuation across two independent runs (n=5, n=8) — reported as a genuine limitation, not smoothed into an unqualified pass. Effect retains sign and order of magnitude in all four tests.

---

## 7. Ablation Study (Corrected)

| Configuration | ATE | 95% CI | CI width |
|---|---|---|---|
| OLS | 0.004898 | — | — |
| Linear DML | 0.003706 | [0.002715, 0.004698] | 0.0020 |
| CausalForestDML, `honest=False` | 0.004567 | [−0.001105, 0.010239] | 0.0113 |
| **CausalForestDML, `honest=True` (proposed)** | **0.004786** | **[0.002576, 0.006997]** | **0.0044** |

**The honesty finding is confirmed and stronger than under the uncorrected model.** Non-honest CF's CI is 2.6x wider than the honest version and still crosses zero — honest estimation is what makes the CI defensibly exclude zero. This is the primary quantified justification for the `honest=True` design decision.

---

## 8. Remaining Open Items (project-wide, not Role 4/5-specific)

All Role 4 and Role 5 computational/statistical work is complete. Two items remain open at the project level, neither closeable through further analysis:

1. **HCAI teacher comprehension study** — instrument, protocol, and analysis code finalized (Role 5 memo, Section 6), but no data collected. Blocked on the real KNUST ethics reference and real teacher participants.
2. **Web application deployment** (Role 6) — build specification exists; not yet implemented.

---

## 9. Handoff

**To the manuscript's Results and Analysis section:** this memo (baselines, LOGO-CV, ablation) plus Role 5's memo (SHAP, refutation tests, heterogeneity, figures) plus Role 2's memo (ground-truth validation) together constitute the complete, corrected, internally-consistent evidence base for Objectives 1 and 2. All cite the same canonical model (`cf_canonical_model.pkl`, ATE=0.0048) with no outstanding contradictions between documents.
