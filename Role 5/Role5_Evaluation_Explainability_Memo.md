# Role 5 Memo: Evaluation and Explainability

**Purpose:** Documents explainability work on the corrected (canonical) CausalForestDML model. **This memo is a work in progress, not a closed-out record like Roles 1–3** — several core Role 5 deliverables remain outstanding. Status is marked explicitly throughout rather than implied.

**Model used:** `cf_canonical_model.pkl` — the `code_module`-corrected specification (ATE=0.0048), confirmed current per Role 4 memo Section 0.

---

## 1. SHAP Analysis — ✅ COMPLETE (re-run on corrected model)

Computed via EconML's native `shap_values()` on the fitted CausalForestDML object, 500-student subsample (seed 42), per Methods Section 3.10.

**Top-ranked features (full table saved as `shap_ranking_v2.csv`):**

| Rank | Feature | Mean |SHAP| |
|---|---|---|
| 1 | `code_module_BBB` | 0.001720 |
| 2 | `code_presentation_2013J` | 0.001021 |
| 3 | `code_module_CCC` | 0.001015 |
| 4 | `age_band_35-55` | 0.000726 |
| 5 | `code_module_DDD` | 0.000709 |
| 6 | `code_presentation_2014B` | 0.000708 |
| 7 | `code_module_FFF` | 0.000598 |
| 8 | `studied_credits` | 0.000552 |
| 9 | `highest_education_Lower Than A Level` | 0.000424 |
| 10 | `code_presentation_2014J` | 0.000345 |
| 11 | `gender_M` | 0.000246 |

**Key finding — before/after comparison across the model correction (Section 0 of Role 4 memo):** `code_module` dummies now dominate the top of the ranking, consistent with LOGO-CV's independently-observed module-level ATE variation. `gender_M` — the single dominant feature under the uncorrected model (ranked #1, ~9x its current magnitude) — dropped to #11 once module identity was properly controlled. This is strong internal cross-validation: three independent diagnostics (LOGO-CV, the ablation study, and SHAP) now tell a mutually consistent story, which was not true before the correction.

`code_module_AAA` does not appear (absorbed into the model intercept as the dropped reference category in one-hot encoding — expected, not an omission).

---

## 2. DoWhy Refutation Tests — ✅ COMPLETE (re-run on corrected model)

All four tests run against `cf_canonical_model.pkl` (ATE=0.004786, confirmed matching between direct fit and DoWhy wrapper before testing began). `num_simulations=5` used throughout except bootstrap (run twice, n=5 and n=8, per the stopping-rule protocol below) — a stated computational-constraint limitation, well below the field-standard 100.

**Note (superseding the table below this memo originally carried):** the notebook was re-run in a later Colab session; DoWhy's refuters resample internally without a global fixed seed, so a genuine re-run legitimately produces different specific numbers while preserving the same qualitative pattern. The values below are from that later run, captured directly in `Role_5_Refutation_CausalMedia.ipynb`'s stored output, and are the numbers now carried in the Results document (Table 5) and should be treated as authoritative going forward.

| Test | New effect | Deviation | p-value | Verdict |
|---|---|---|---|---|
| Placebo treatment | −0.0000257 | Collapses to ~0 | 0.450 | ✅ Clean pass |
| Random common cause | 0.004797 | 0.2% | 0.388 | ✅ Clean pass |
| Data subset (80%) | 0.004711 | −1.6% | 0.303 | ✅ Clean pass |
| Bootstrap (n=5) | 0.002773 | 42.1% | ≈0.0 (as reported by DoWhy) | ⚠️ See below |
| Bootstrap (n=8) | 0.002584 | 46.0% | ≈0.0 (as reported by DoWhy) | ⚠️ See below |

**Three of four tests pass cleanly** (placebo, random-cause, and subset are all consistent with a well-specified, stable estimate — placebo collapses toward zero as expected, and both random-common-cause and data-subset deviations stay under 2%).

**Bootstrap requires an honest, specific caveat — not a pass/fail label.** Two independent bootstrap runs (n=5 and n=8) sit within about 4 percentage points of each other (42.1% vs. 46.0%) while both showing a substantial attenuation from the original estimate. This reasonable agreement between two independent runs suggests this is a real, reproducible attenuation under bootstrap resampling specifically, not simulation-count noise. A plausible, unverified hypothesis: with `code_module` now in the confounder set, bootstrap's with-replacement resampling may be more prone to under-representing small strata (e.g., AAA, the smallest module at 612 students) or specific module/gender combinations — but this mechanism has not been directly tested and should be presented as a candidate explanation, not a confirmed one.

**Reportable conclusion for Results:** *"Three of four refutation tests (placebo, random common cause, data subset) showed strong effect stability, with deviations under 2% from the original estimate (placebo collapsing toward zero as expected). The bootstrap refuter showed a substantial and reproducible attenuation (~42–46% across two independent runs, n=5 and n=8), the most significant limitation identified during robustness testing. The estimated effect retained its sign and order of magnitude throughout all four tests. This finding is reported as a genuine limitation of the study's causal identification robustness, not smoothed into an unqualified pass, and is recommended as a priority for further investigation (e.g., stratified or block bootstrap by module) beyond the scope of the current analysis."*

---

## 3. Subgroup Heterogeneity Checks — ✅ COMPLETE (all three, corrected model)

**Ranking by effect size (epsilon-squared / rank-biserial r):**

| Variable | Effect size | Size | Pattern |
|---|---|---|---|
| **`highest_education`** | **ε²=0.0712** | **Medium** | Clean, monotonic decline from "Lower Than A Level" peak (0.00531) through Postgraduate (0.00292) |
| `imd_band` | ε²=0.0247 | Small | Mild, non-monotonic across deprivation bands; `Missing` category (n=830) notably lowest (0.00404) |
| Gender | r=−0.170 | Small-moderate | Real but modest after correction; substantially explained by module composition (see Role 4 memo Section 4) |

**`highest_education` is the recommended primary heterogeneity finding for Results** — effect size roughly 3x `imd_band`'s, and a substantively coherent, monotonic pattern (students with less formal prior education show larger benefit from `oucontent` engagement — a plausible "compensatory" interpretation, stated as a candidate explanation, not confirmed). This reverses the original (uncorrected-model) finding, where `highest_education` appeared negligible (ε²=0.009) and gender appeared dominant (r=−0.489) — the `code_module` correction inverted which variable actually drives heterogeneity in this corpus.

**`imd_band` note:** its `Missing` category (830 students, concentrated in North Region/Ireland per Role 1's memo, mechanism unconfirmed) shows the lowest mean CATE of all eleven groups — worth a sentence in Discussion, not over-interpreted given the unresolved missingness mechanism.

Full table saved as `heterogeneity_checks_v2.csv`.

---

## 4. CV-Stability and Error-Analysis Figures — ✅ COMPLETE

**CV-stability:** `figure_cv_stability.png` — grouped bar chart of train vs. held-out ATE across all 6 modules from LOGO-CV (Role 4 memo Section 5), with the full-corpus ATE (0.0048) marked as a reference line. Confirms visually what the LOGO-CV table already showed: all six modules agree in sign and cluster near the reference line, with FFF as the clear (but positive) low outlier.

**Error analysis:** `figure_error_analysis_ihdp.png` — predicted-vs-true CATE scatter plot on Role 2's IHDP benchmark (realization 0), the one place ground truth genuinely exists (see Section 1's metric decision for why the original confusion-matrix-style figure is inapplicable here). PEHE for this specific saved run: **0.6835** (see Role 2 memo Section 7 for the minor, understood cross-session discrepancy from earlier diagnostic runs). The figure visually shows CausalForestDML's predictions tracking the identity line reasonably well for true effects above ~3, but staying nearly flat (~2.9–3.1) for true effects below ~2 — a clear visual companion to Role 2's documented finding that CF underperformed Linear DML on PEHE in the majority of IHDP realizations.

---

## 5. `ouelluminate_clicks` Robustness Subsample — ✅ COMPLETE

N=2,031 (BBB: 390, DDD: 649, FFF: 992), all restricted to presentation `2013B` — confirmed `code_presentation` contributes zero encoded columns in this subsample (single value, structurally uninformative here, unlike in the primary corpus). Confounder set includes `code_module` from the start (34 columns), applying the lesson from the primary-corpus correction rather than repeating the omission. `min_samples_leaf=15` used (vs. primary corpus's 50), a documented sample-size-appropriate adjustment.

| Estimator | Effect (raw, per click) |
|---|---|
| Pearson (naive) | r=−0.0484, p=0.029 (**negative**) |
| OLS | 0.0563 |
| Linear DML | 0.0696, 95% CI [0.0018, 0.1374] |
| CausalForestDML | 0.0646, 95% CI [−0.0283, 0.1576] |

**Sign reversal under adjustment** — more pronounced than the primary corpus's suppression pattern (which increased but didn't reverse sign). The raw correlation is negative; every adjusted estimator is positive. A naive analysis would have concluded `ouelluminate` engagement is harmful.

**Scaled comparison to primary corpus (per 1-SD increase in engagement):**

| | Primary (`oucontent`) | Robustness (`ouelluminate`) |
|---|---|---|
| Effect per SD | 2.075 points | 1.519 points (≈73% as large) |
| CI excludes zero | Yes | Linear DML: yes. CausalForestDML: **no** |

**Reportable conclusion:** the robustness subsample shows an effect of similar order of magnitude using a genuinely unambiguous multimedia measure on an independent subset — meaningfully strengthening the "multimedia engagement" construct-validity claim in the title. However, CausalForestDML's CI does not exclude zero at N=2,031 — this is a sample-size limitation, not a contradictory finding, and must be stated as such, not smoothed into an unqualified confirmation. Saved as `cf_ouelluminate_model.pkl`.

---

## 6. HCAI Teacher Comprehension Study — ⚠️ INSTRUMENT READY, DATA COLLECTION BLOCKED

**Status:** the survey instrument, protocol, and analysis code below are finalized and ready to administer. **Actual data collection cannot happen without (a) the real KNUST ethics reference (still a placeholder per the Project Overview memo, Section 7) and (b) real teacher participants.** This section documents what is prepared, not what has been collected — no responses exist yet, real or otherwise.

**Methods clarification (add verbatim to the manuscript):** *"Teacher comprehension was evaluated using synthetic student profiles derived from the OULAD feature distributions, presented to participants as illustrative cases for testing interface usability rather than as records of real students from any specific institution."*

### 6.1 Stimuli

Ten synthetic student profiles, generated by sampling from the corrected model's actual confounder and CATE distributions (`full[confounders_v2]` and `full['cate_v2']`, per Role 4's corrected corpus) — realistic in distribution, explicitly disclosed as illustrative per the clarification above, not drawn from or attributable to any real student record.

### 6.2 Design

Within-subject, two conditions, counterbalanced order across the three teachers to control for order effects (Teacher 1: A→B; Teacher 2: B→A; Teacher 3: A→B, or a full 3×2 Latin square if a 4th+ teacher is later added):
- **Condition A:** each of the 10 profiles shown with only the raw numerical CATE estimate.
- **Condition B:** the same 10 profiles shown with the CATE estimate, a SHAP waterfall chart, and a plain-language recommendation sentence.

### 6.3 Instrument

**Comprehension items (5-point Likert, 1=Strongly Disagree to 5=Strongly Agree), administered after each condition block:**
1. "I understood the magnitude of the estimated benefit for this student."
2. "I could identify what factors were driving this result."
3. "I could explain this result to the student or their parent in plain language."
4. "I could interpret this result without needing statistical training."

**Action-intention items (5-point Likert), administered only after Condition B:**
5. "This information would change how I allocate my attention or resources for this student."
6. "I would feel confident acting on this recommendation."

**System Usability Scale (Brooke, 1996), standard 10-item wording, administered once after all profiles (both conditions) are complete:**
1. I think that I would like to use this system frequently.
2. I found the system unnecessarily complex.
3. I thought the system was easy to use.
4. I think that I would need the support of a technical person to be able to use this system.
5. I found the various functions in this system were well integrated.
6. I thought there was too much inconsistency in this system.
7. I would imagine that most people would learn to use this system very quickly.
8. I found the system very cumbersome to use.
9. I felt very confident using the system.
10. I needed to learn a lot of things before I could get going with this system.
(Standard SUS scoring: odd items score = rating−1; even items score = 5−rating; sum ×2.5 = 0–100 scale.)

### 6.4 Analysis code (ready to run once real data exists — currently untested against real responses, only against a dummy shape check)

```python
import pandas as pd
from scipy.stats import wilcoxon
from scipy.stats import cronbach_alpha  # or compute manually if unavailable

# Expected input shape: one row per teacher x condition, columns = the 4 comprehension items
# responses.csv columns: teacher_id, condition, item1, item2, item3, item4

responses = pd.read_csv('hcai_responses.csv')  # real file, once collected
responses['comprehension_score'] = responses[['item1','item2','item3','item4']].mean(axis=1)

grand_means = responses.groupby('condition')['comprehension_score'].agg(['mean','std'])
print(grand_means)

cond_a = responses[responses['condition']=='A'].sort_values('teacher_id')['comprehension_score']
cond_b = responses[responses['condition']=='B'].sort_values('teacher_id')['comprehension_score']
stat, p = wilcoxon(cond_b, cond_a)
print(f"Wilcoxon signed-rank (paired, n=3): stat={stat}, p={p:.4g}")
# Note: minimum achievable p at n=3 paired observations is 0.25 — expected, not a failure

# SUS scoring
sus_items = [f'sus{i}' for i in range(1,11)]
def score_sus(row):
    total = 0
    for i in range(1,11):
        v = row[f'sus{i}']
        total += (v-1) if i % 2 == 1 else (5-v)
    return total * 2.5
responses_sus = pd.read_csv('sus_responses.csv')  # one row per teacher
responses_sus['sus_score'] = responses_sus.apply(score_sus, axis=1)
print(responses_sus[['teacher_id','sus_score']])
print(f"Mean SUS: {responses_sus['sus_score'].mean():.1f}  (>=70 = conventional 'good usability' threshold)")
```

---

## 7. Teacher Dashboard Content — ❌ NOT DONE

Depends on Sections 2–6 above being complete, since dashboard content should reflect real, corrected, finalized results — not draft numbers that may still change.

---

## Summary Table

| Task | Status |
|---|---|
| SHAP analysis | ✅ Complete (corrected model) |
| Refutation tests | ✅ Complete (3/4 clean pass, bootstrap flagged with honest caveat) |
| Gender heterogeneity | ✅ Complete (corrected model) |
| `highest_education` heterogeneity | ✅ Complete (corrected model) — primary finding |
| `imd_band` heterogeneity | ✅ Complete (corrected model) — secondary finding |
| CV-stability / error-analysis figures | ✅ Complete |
| `ouelluminate` robustness subsample | ✅ Complete — directionally supportive, underpowered on CausalForestDML CI |
| HCAI teacher study | ❌ Blocked on ethics reference |
| Teacher dashboard | ❌ Blocked on above |
