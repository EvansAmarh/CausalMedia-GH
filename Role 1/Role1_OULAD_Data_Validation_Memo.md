# Role 1 Data-Validation Memo: OULAD Corpus Construction

**Purpose:** This memo documents every data-construction decision made in building the OULAD analytical corpus, with the empirical check that justified each decision, so that treatment, outcome, and confounder definitions are traceable to evidence rather than asserted. It is the artifact that should be cited in Methods Section 3.2.1 (or equivalent) and made available on request.

---

## 1. Data Source

Open University Learning Analytics Dataset (OULAD): 32,593 students, 22 module-presentations across 7 modules, 2013–2014, released under CC-BY 4.0 (Kuzilek, Hlosta & Zdrahal, 2017, *Scientific Data*). Seven relational tables used: `studentInfo.csv`, `studentVle.csv`, `vle.csv`, `studentAssessment.csv`, `assessments.csv`, `studentRegistration.csv`.

---

## 2. Treatment Variable Construction

### 2.1 Deduplication (prerequisite step)

`studentVle.csv` was found to contain genuine duplicate rows at the `(id_student, id_site, date)` level — 8,459,320 of 10,655,280 groups were unique; 1,614,505 groups had more than one row. These were collapsed via `sum()` before any click-volume analysis, since summing without deduplication would double-count engagement for roughly 19% of student-site-day observations.

### 2.2 Click-volume verification (all 20 activity types)

`studentVle.csv` (post-dedup) was merged with `vle.csv` on `(id_site, code_module, code_presentation)` — a clean join (8,459,320 rows in, 8,459,320 out, no inflation). Click volume by activity type, all 22 module-presentations:

| activity_type | total_clicks | % of engagement |
|---|---|---|
| oucontent | 11,206,803 | 28.30% |
| forumng | 7,973,390 | 20.13% |
| quiz | 6,981,240 | 17.63% |
| homepage | 6,949,064 | 17.55% |
| subpage | 3,411,582 | 8.61% |
| resource | 1,110,132 | 2.80% |
| ouwiki | 894,512 | 2.26% |
| url | 566,702 | 1.43% |
| oucollaborate | 108,974 | 0.28% |
| glossary | 87,962 | 0.22% |
| questionnaire | 64,764 | 0.16% |
| externalquiz | 64,292 | 0.16% |
| page | 63,631 | 0.16% |
| dataplus | 47,468 | 0.12% |
| **ouelluminate** | **39,028** | **0.10%** |
| dualpane | 20,716 | 0.05% |
| htmlactivity | 9,239 | 0.02% |
| folder | 5,420 | 0.01% |
| sharedsubpage | 171 | 0.00% |
| repeatactivity | 9 | 0.00% |

### 2.3 Two-tier treatment design

No single activity type is both dominant in volume *and* unambiguously multimedia:
- `oucontent` is the largest single category (28.3%) but OULAD's documentation describes it only as "structured content pages" — video, text, and interactive content are not distinguished within it.
- `ouelluminate` (live audio/video conferencing) is unambiguously multimedia but confined to 3 of 22 module-presentations (BBB-2013B: 1,433 clicks; DDD-2013B: 13,565 clicks; FFF-2013B: 24,030 clicks) — near-zero or absent elsewhere.

**Decision:** a two-tier design was adopted rather than forcing a single definition.

- **Primary treatment (`oucontent_clicks`):** aggregated `oucontent` engagement per student, all 22 presentations. Reported in Methods/Discussion as *structured content engagement*, not asserted as multimedia-specific.
- **Secondary/robustness treatment (`ouelluminate_clicks`):** aggregated `ouelluminate` engagement, restricted to BBB-2013B, DDD-2013B, FFF-2013B only. This is the genuinely unambiguous multimedia measure, used to check whether any effect found in the primary analysis replicates directionally under a narrower, verified construct.

---

## 3. Outcome Variable Construction

### 3.1 Why a raw-score trajectory, not a weighted final grade

`assessments.csv` weight sums do not equal 100 in 19 of 22 module-presentations (mean 195.5, only the three GGG presentations sum to exactly 100), because continuous-assessment (TMA/CMA) and Exam weights are recorded on separate ~100-point scales rather than one combined scale, with the true blending formula living outside this file, in each module's own (undocumented-in-data) grading policy. Reconstructing an "official final grade" from raw weights would require guessing that formula. **`performance_gain` was therefore defined from raw per-assessment scores (already 0–100), not weighted scores**, avoiding this ambiguity entirely.

### 3.2 Exclusions applied, in order

| Step | Students remaining | Rationale |
|---|---|---|
| Registered students | 32,593 | — |
| ≥1 valid (non-banked, non-zero-weight) assessment | 23,239 | Excludes `is_banked==1` rows (1,909 total — scores carried over from a prior attempt, not earned under this presentation's conditions) and zero-weight CMA rows (46 of 76 CMA definitions — formative/practice, not graded) |
| ≥2 valid assessments (trajectory feasible) | 20,807 | A first-to-last gain measure requires at least two graded data points |
| Excluding early withdrawals (unregistered before final valid-assessment due date) | 18,364 | A withdrawal is a missing outcome, not a zero outcome |
| Excluding remaining NaN scores | 18,363 | One residual row with a missing score |

### 3.2b GGG module exclusion (discovered during Role 4 estimation, traced back here)

During Role 4's leave-one-module-out cross-validation, GGG was found to be entirely absent from the corpus — 0 of 2,107 GGG students with assessment records made it into the final outcome table, despite GGG having substantial real `oucontent` engagement (477,373 clicks, its largest activity-type category). Traced to source: GGG's `assessments.csv` defines exactly one weighted component per presentation (Exam, weight=100, `id_assessment` 37424/37434/37444 across its three presentations 2013J/2014B/2014J), all nine of its CMA/TMA components being weight=0. **None of GGG's three Exam `id_assessment` values appear anywhere in `studentAssessment.csv`** — a complete absence of recorded scores for GGG's only gradeable component, confirmed directly rather than inferred. This is a documented gap in this OULAD release for this specific module (exams marked externally and not entered into this file), not a pipeline error and not a study-specific exclusion criterion.

**Consequence:** the primary corpus covers 6 of OULAD's 7 modules (19 of 22 module-presentations) — AAA, BBB, CCC, DDD, EEE, FFF. GGG cannot be included in any outcome-based analysis under this study's `performance_gain` definition, regardless of treatment definition or confounder handling.

### 3.3 Winsorization

`performance_gain` (last valid score − first valid score) ranged [−95, 95] before treatment. The 1st/99th percentiles ([−61.38, 40.00]) were used as winsorization bounds (capping, not dropping): 353 students (1.92%) were capped. Post-winsorization: mean −5.54, SD 19.85 (vs. −5.56/20.35 pre-cap).

### 3.4 Course-stage difficulty escalation (documented, not treated as an error)

The negative mean `performance_gain` reflects assessments generally becoming harder as a module progresses, not a data defect. Two independent pieces of evidence:

1. **Mean gain by last-assessment type:** TMA-last −6.80 (n=10,558), Exam-last −11.25 (n=4,937), CMA-last +8.78 (n=2,868) — negative for the two assessment types that dominate "last position," with the Exam-last group most negative, consistent with exam-vs-coursework difficulty gaps.
2. **Tail asymmetry:** 1st percentile −61.38 vs. 99th percentile +40.00 — large negative outliers are more common and more extreme than large positive ones, consistent with a difficulty-escalation pattern rather than symmetric noise.

**Interpretive consequence for Discussion:** any estimated treatment effect of `oucontent`/`ouelluminate` engagement on `performance_gain` should be read as *engagement moderating the rate of decline as coursework difficulty increases*, not as *engagement producing absolute performance improvement*. This should be stated explicitly rather than left for a reviewer to infer.

### 3.5 Final corpus sizes after merging outcome onto each treatment definition

| Corpus | N | Coverage |
|---|---|---|
| `oulad_full_corpus.csv` (oucontent treatment) | 17,529 | 6 of 7 modules (19 of 22 module-presentations) — GGG excluded, see Section 3.2b |
| `oulad_ouelluminate_subsample.csv` (multimedia treatment) | 2,031 (BBB: 390, DDD: 649, FFF: 992) | 3 module-presentations only |

**Module breakdown of `oulad_full_corpus.csv` (N=17,529):** FFF 4,930; BBB 4,279; DDD 3,608; CCC 2,114; EEE 1,986; AAA 612.

---

## 4. Confounder Set

`gender`, `region`, `highest_education`, `imd_band`, `age_band`, `num_of_prev_attempts`, `studied_credits`, `disability` — pulled from `studentInfo.csv`.

**Missingness:** all confounders 0% missing except `imd_band` at 4.7%.

**`imd_band` handling — confirmed by region cross-tabulation:**

| Region | Missing | Total | Missing rate |
|---|---|---|---|
| North Region | 547 | 1,049 | 52.1% |
| Ireland | 209 | 815 | 25.6% |
| South Region | 34 | 1,735 | 2.0% |
| West Midlands Region | 28 | 1,262 | 2.2% |
| Scotland | 6 | 2,095 | 0.3% |
| South West / North Western / Yorkshire Regions | 6 (combined) | — | <0.3% each |
| East Anglian, London, Wales, East Midlands, South East Regions | 0 | — | 0.0% |

Missingness is heavily and unevenly concentrated by region (0% in five regions, 52% in one), which rules out missing-completely-at-random. An initial hypothesis — that missingness reflects Northern Ireland's use of a separate deprivation measure (NIMDM) incompatible with OULAD's English IMD — is **not supported** by this check: Ireland is only 25.6% missing (not near-100% as that hypothesis would predict), and Wales, which also runs its own non-English deprivation index, shows 0% missingness. The true mechanism (most plausibly postcode-to-LSOA geocoding failures concentrated in specific areas) is not confirmed by this check and is not asserted here.

**Decision: retained as an explicit `"Missing"` category rather than dropped.** Regardless of the unconfirmed mechanism, the region-skew itself is sufficient reason not to drop: doing so would remove over half of North Region's students and a quarter of Ireland's while removing almost none from five other regions, distorting the corpus's regional composition. Tree-based estimators (CausalForestDML) handle an explicit missing category as a natural split level; linear baselines (OLS, Linear DML) one-hot encode it as its own indicator.

**Verification code run:**
```python
print(full_corpus[full_corpus['imd_band'].isna()]['region'].value_counts())
print(full_corpus['region'].value_counts())
```

**Flag for Role 3 (DAG specification):** `code_presentation` and/or `last_assessment_type` should be considered as a control variable, given the documented course-stage difficulty effect in Section 3.4 above.

---

## 5. Known Limitations (for Discussion section)

1. `oucontent` is a broad "structured content engagement" proxy, not a confirmed video-specific measure — the primary analysis should be labeled accordingly, with the `ouelluminate` subsample presented as the genuinely unambiguous multimedia validation.
2. **GGG (all 3 presentations) is entirely absent from the analytic corpus** because its only weighted assessment component (Exam) has no recorded scores anywhere in `studentAssessment.csv` — see Section 3.2b. There is no weight-sum-100 internal validation subsample; the earlier plan to use GGG this way is not possible, since GGG cannot appear in any outcome-based analysis. The primary corpus covers 6 of 7 modules, 19 of 22 module-presentations — this should be stated explicitly wherever corpus coverage is reported in Methods, not implied to be the full 22.
3. `performance_gain`'s negative mean reflects course-stage difficulty escalation (Section 3.4); causal estimates must be interpreted as effects on rate of decline, not absolute improvement.
4. `imd_band` missingness handling is stated above and should be reported explicitly in Methods, not left implicit.

---

## 6. Handoff Summary

**To Role 2 (ground-truth benchmark):** No dependency — proceeds independently.

**To Role 3 (causal structure specification):** Confounder set as listed in Section 4; consider `code_presentation`/`last_assessment_type` as an additional DAG node per the difficulty-escalation finding.

**To Role 4 (causal effect estimation):** Two corpora ready — `oulad_full_corpus.csv` (N=17,529, primary) and `oulad_ouelluminate_subsample.csv` (N=2,031, robustness check across 3 presentations only), both with winsorized `performance_gain` as outcome and the Section 4 confounder set attached.
