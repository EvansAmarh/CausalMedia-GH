# CausalMedia-GH

**CausalForestDML for Heterogeneous Estimation of Multimedia-Engagement Effects on Learning Outcomes: A Validated Framework and Data-Readiness Blueprint for Ghanaian Senior High Schools**

CausalMedia-GH is an end-to-end causal machine learning pipeline built by **NexusLearn Group 4**, Department of Computer Science, Kwame Nkrumah University of Science and Technology (KNUST), under the supervision of **Dr. Eric Osei**. The project develops and validates a `CausalForestDML`-based estimator of *heterogeneous* multimedia-engagement effects on learning outcomes — on a public dataset that genuinely contains the required treatment, confounder, and outcome measures — then translates the validated method into a teacher-facing decision-support tool and a concrete data-readiness blueprint for Ghanaian institutions.

> Motivated, better-resourced students tend to both engage more with course content *and* perform better independently of that engagement — a classic selection-effect confound. CausalMedia-GH uses `CausalForestDML` (Microsoft EconML) to control for measured confounders and estimate each student's individual conditional average treatment effect (CATE), rather than a single population-level average.

---

## Table of Contents

- [Why Ghana, Given the Data Isn't Ghanaian](#why-ghana-given-the-data-isnt-ghanaian)
- [Key Finding](#key-finding)
- [Pipeline & Team Roles](#pipeline--team-roles)
- [Repository Structure](#repository-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Data Sources](#data-sources)
- [Methodology Summary](#methodology-summary)
- [Web Application (Role 6)](#web-application-role-6)
- [Limitations](#limitations)
- [Ethical Compliance](#ethical-compliance)
- [Project History](#project-history)
- [Contributors](#contributors)
- [License](#license)

---

## Why Ghana, Given the Data Isn't Ghanaian

Ghana's Ministry of Education EMIS reliably captures institutional-level census data (enrolment, staffing, facilities) but not individual-level learning-process data — the combination of a directly measured engagement indicator, high-resolution behavioural confounders, and a linked continuous outcome that heterogeneous causal-effect estimation requires. This gap is not permanent: Ghana's 2024 Smart Schools Project has begun distributing 1.3 million tablets to SHS students, creating for the first time the technical capacity to log individual multimedia-interaction data — but no analytics pipeline or data standard yet exists to capture, structure, or act on it.

This project makes **no quantitative claim about any Ghanaian population.** It validates a causal-forest estimator on a public dataset that genuinely contains the required measures (OULAD, below), so that a validated method and a working decision-support system already exist for the moment Ghana's emerging learning-technology infrastructure begins generating individual-level engagement data.

---

## Key Finding

| Metric | Value |
|---|---|
| Population-level ATE, primary corpus (n = 17,529) | 0.0048 per `oucontent` click, 95% CI [0.0026, 0.0070] |
| Robustness subsample (`ouelluminate_clicks`, n = 2,031) | 0.0646, 95% CI [−0.0283, 0.1576] — directionally consistent, underpowered on this estimator alone |
| **Primary heterogeneity finding** | **`highest_education`** — ε² = 0.0712, clean monotonic decline: students with less formal prior education show the largest estimated benefit from engagement |
| Secondary heterogeneity | `imd_band` (deprivation band), ε² = 0.0247; gender, rank-biserial r = −0.170 |
| Top SHAP driver | `code_module` (course identity) — dominates the ranking once correctly included as a confounder |

The primary corpus's confidence interval excludes zero. The `ouelluminate_clicks` robustness subsample — a genuinely unambiguous multimedia measure, versus the primary corpus's broader "structured content" proxy — shows an effect of similar order of magnitude and, notably, a **sign reversal under adjustment**: the raw, unconfounded correlation is negative, while every confound-adjusted estimator is positive. An unadjusted analysis would have concluded multimedia engagement is harmful; correcting for selection effects reverses that conclusion.

---

## Pipeline & Team Roles

| Role | Responsibility | Status |
|---|---|---|
| **1** | Data engineering — OULAD corpus construction, treatment-construct validation, outcome derivation | ✅ Complete |
| **2** | Ground-truth benchmark validation (IHDP) — confirms the estimator recovers a known causal effect, independent of any specific population | ✅ Complete |
| **3** | Causal structure specification — DAG, confounder-set justification, identification assumption | ✅ Complete |
| **4** | Causal effect estimation — baselines, `CausalForestDML`, leave-one-module-out CV, ablation | ✅ Complete |
| **5** | Evaluation & explainability — SHAP, DoWhy refutation tests, subgroup heterogeneity, figures | ✅ Complete (HCAI teacher study: instrument ready, data collection blocked — see [Limitations](#limitations)) |
| **6** | Web-based decision-support application + Ghana data-readiness blueprint | Build-ready against mock data; not yet deployed |

See `/docs` for the full per-role memos (`Role1_OULAD_Data_Validation_Memo.md` through `Role5_Evaluation_Explainability_Memo.md`), which are the authoritative source for every number in this README.

---

## Repository Structure

```
CausalMedia-GH/
├── Role 1/                     # OULAD data-engineering notebook
├── Role 2/                     # IHDP ground-truth benchmark notebook
├── Role 3/                     # Causal DAG definition (role3_dag.png)
├── Role 4/                     # CausalForestDML estimation notebook
├── Role 5/                     # SHAP, DoWhy refutation, heterogeneity, figures
├── docs/                       # Role 1–5 memos, Methods and Results & Analysis sections
├── requirements.txt
└── README.md
```

*Role 6 (web application) directory structure is not yet finalised — see [Web Application](#web-application-role-6).*

---

## Tech Stack

### Data Science Pipeline (Roles 1–5)
- **Python** — pandas, NumPy, SciPy
- **EconML** (Microsoft, `0.17.0`) — `CausalForestDML`, `LinearDML`
- **scikit-learn** — `HistGradientBoostingRegressor` / `GradientBoostingRegressor` as nuisance models (not LightGBM — see [Methodology Summary](#methodology-summary))
- **DoWhy** (`0.14`) — causal refutation testing
- **SHAP** — model explainability, via EconML's native `shap_values()` method
- **NetworkX** — causal DAG representation

### Web Application (Role 6)

Not yet built beyond the mock-data-ready specification. Tech-stack decisions live in the Role 6 build memo — **not included in this repository listing yet**, since including a specific stack here without that memo would risk stating something unconfirmed.

---

## Getting Started

### Prerequisites
- Python 3.10+ (project notebooks were run under Python 3.12 in Google Colab)
- Jupyter, or Google Colab (all notebooks were developed and executed there)

### Data Science Notebooks

```bash
pip install -r requirements.txt
jupyter notebook
```

Notebooks run in dependency order: Roles 1, 2, and 3 have no interdependencies and can run in any order or in parallel; Role 4 depends on the outputs of all three; Role 5 depends on Role 4.

---

## Data Sources

| Dataset | Type | Size | Role |
|---|---|---|---|
| OULAD (Kuzilek, Hlosta & Zdrahal, 2017) | Public, CC-BY 4.0 | 32,593 students → 17,529 primary corpus (6 of 7 modules; GGG excluded — its only gradeable component has no recorded scores in this OULAD release), 2,031 robustness subsample | Primary analytical corpus |
| IHDP benchmark (Hill, 2011, Setting B) | Public research benchmark | 672 units × 25 covariates × 100 realisations | Estimator ground-truth validation only — never merged with OULAD |

**No synthetic data of any kind is used anywhere in this pipeline.** An earlier design considered a synthetic Ghanaian school-context layer merged onto real interaction data; it was rejected (see [Project History](#project-history)) because a positionally-merged synthetic layer fabricates a covariate–outcome relationship that never existed in reality.

**Treatment (two-tier design):**
- Primary — `oucontent_clicks`, aggregated structured-content engagement, all 22 module-presentations (n = 17,529). OULAD documents `oucontent` only as generic "structured content," not confirmed video-specific — reported accordingly.
- Robustness — `ouelluminate_clicks`, live audio/video conferencing engagement, the genuinely unambiguous multimedia measure, restricted to the 3 presentations where it occurs (n = 2,031).

**Outcome:** `performance_gain` — last valid assessment score minus first valid assessment score (raw scores, not weighted grades — OULAD's weight fields don't sum to 100 in 19 of 22 presentations), winsorised at the 1st/99th percentiles.

**Confounders (10):** `gender`, `region`, `highest_education`, `imd_band`, `age_band`, `num_of_prev_attempts`, `studied_credits`, `disability`, `code_presentation`, `code_module`. `code_module` was a late addition, discovered via a SHAP-driven investigation into an anomalous gender effect; adding it changed the headline ATE by 85% (0.0026 → 0.0048) — see the Role 3 and Role 4 memos for the full discovery narrative.

---

## Methodology Summary

1. **Baseline progression** — naïve Pearson correlation → OLS → Linear DML → `CausalForestDML`, isolating what each layer of confound-adjustment and non-parametric flexibility contributes.
2. **Main estimator** — `CausalForestDML` (EconML), replacing Double Machine Learning's linear second stage with a non-parametric causal forest (the study's engineered contribution). Nuisance models: scikit-learn `HistGradientBoostingRegressor`, 5-fold cross-fitting, `honest=True`, `min_samples_leaf=50`, `n_estimators=500`, single random seed (42). Multi-seed replication is planned but not yet executed — stated as an open limitation, not concealed.
3. **Ground-truth validation (Role 2)** — the same estimator class validated against IHDP, a benchmark with a documented true causal effect, independent of the OULAD population.
4. **Refutation testing (Role 4/5)** — four DoWhy tests: placebo treatment, random common cause, data-subset, and bootstrap refuters. Three pass cleanly (deviations under 2%); the bootstrap refuter shows a reproducible ~42–46% attenuation, reported as a genuine limitation.
5. **Explainability (Role 5)** — SHAP values computed via EconML's native method on a 500-student subsample.
6. **Communication (Objective 3)** — a teacher-facing decision-support web application and a concrete minimal data-schema recommendation for Ghanaian institutions building learning-analytics infrastructure.

---

## Web Application (Role 6)

Per the project's Objective 3, the web application's purpose is to present validated causal-ML findings to a non-technical audience, operationalise a teacher usability evaluation, and host the Ghana data-readiness blueprint. As of this README, Role 6 is **build-ready against a mock-data contract** but not yet implemented or deployed — there is no live deployment to link here yet. This section will be updated once the Role 6 build memo's specification is implemented.

---

## Limitations

- The `ouelluminate_clicks` robustness subsample's `CausalForestDML` confidence interval does not exclude zero (n = 2,031, roughly a ninth of the primary corpus) — read as a sample-size limitation, not a contradictory finding; Linear DML's CI on the same subsample does exclude zero.
- The bootstrap refutation test shows a reproducible ~42–46% attenuation from the primary estimate across two independent runs — the most significant limitation identified during robustness testing, not smoothed into an unqualified pass.
- On the IHDP ground-truth benchmark, `CausalForestDML` does **not** outperform Linear DML on individual-level accuracy (PEHE), losing on 70 of 100 realisations despite three documented, justified tuning attempts — attributed to IHDP's small sample size and largely-linear response surface, not treated as a configuration artifact.
- Multi-seed replication of the primary-corpus fit has not yet been executed against the corrected specification — a stated, open item, not a completed procedure.
- The HCAI teacher usability study's instrument, protocol, and analysis code are finalised, but no data has been collected: this is blocked on a real HuSSREC (KNUST) ethics reference, still pending.
- This DAG cannot rule out confounders OULAD does not record — most importantly student motivation, effort, and home or family academic support. The four DoWhy refutation tests probe robustness to this concern but cannot eliminate it.

---

## Ethical Compliance

OULAD is public, pre-anonymised secondary data released under CC-BY 4.0 for research use, with no identifiable personal data and no primary human-subjects contact by this study — no additional ethics approval is required for its analysis. The teacher-facing HCAI usability evaluation (Role 5) is separate, primary human-subjects research and requires clearance from KNUST's Humanities and Social Sciences Research Ethics Committee (HuSSREC); that clearance is still pending, and no data collection under that evaluation has begun or will begin before it is granted.

---

## Project History

This design (OULAD standalone, no synthetic layer, IHDP for ground-truth validation) is the third and final of three design iterations:

1. An initial design used EdNet KT1 with a `multimedia_engagement` field that turned out to be a response-latency proxy, not a genuine multimedia measure — a fatal construct-validity flaw.
2. A revised design added a synthetic Ghanaian school-context layer, positionally merged onto real interaction data — rejected because that merge fabricates a covariate–outcome relationship that never existed in reality, regardless of how well each source dataset validates individually.
3. The current design: OULAD alone, standalone, no merge, no projected Ghana numbers — Ghana relevance argued through a documented data-infrastructure gap and a forward-looking data-readiness blueprint, never through a quantitative claim about Ghanaian students.

Full decision log in the project's Methods documentation.

---

## Contributors

**NexusLearn Group 4**, KNUST Department of Computer Science
Supervisor: **Dr. Eric Osei**

*[Contributor-to-role attribution to be added — the per-role memos document team deliverables but do not individually attribute authorship, so this table needs to be filled in directly by the team.]*

---

## License

*[Not yet specified.]*
