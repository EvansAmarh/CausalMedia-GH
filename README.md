# CausalMedia-GH

**Does multimedia engagement causally improve learning outcomes in Ghanaian Senior High Schools?**

CausalMedia-GH is an end-to-end causal machine learning pipeline built by **NexusLearn Group 4**, Department of Computer Science, Kwame Nkrumah University of Science and Technology (KNUST), under the supervision of **Dr. Eric Osei**. The project estimates the causal — not merely correlational — effect of video/multimedia engagement on student performance gains, using real EdNet KT1 interaction data merged with synthetic Ghanaian school-context data, and communicates the results to teachers through a plain-English interactive web application.

> Motivated students tend to both watch more videos *and* score higher — which makes it look like videos cause improvement even when they might not. CausalMedia-GH uses **CausalForestDML** (Microsoft EconML) to control for measured confounders and isolate each student's individual causal benefit from multimedia content.

---

## Table of Contents

- [Key Finding](#key-finding)
- [Pipeline & Team Roles](#pipeline--team-roles)
- [Repository Structure](#repository-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Data Sources](#data-sources)
- [Methodology Summary](#methodology-summary)
- [Web Application (Role 6)](#web-application-role-6)
- [Output Artefacts](#output-artefacts)
- [Limitations](#limitations)
- [Ethical Compliance](#ethical-compliance)
- [Contributors](#contributors)
- [Citation](#citation)
- [License](#license)

---

## Key Finding

| Metric | Value |
|---|---|
| Population-level ATE (ensemble, 3 seeds) | ≈ 0.019 (not statistically significant — 95% CI includes zero) |
| **Primary contribution** | **Heterogeneous treatment effects across achievement quartiles** |
| CATE, lowest achievement quartile (Q1) | −0.143 |
| CATE, highest achievement quartile (Q4) | +0.177 |
| Top SHAP driver (CausalForestDML) | `early_struggle` — rank 12 → rank 3 vs. Linear DML |

The population-average effect of multimedia engagement is not statistically significant on its own. The project's headline result is instead a **prior-knowledge facilitation gradient**: students with early struggle and lower prior achievement benefit least (or are hurt slightly) from multimedia content, while higher-achieving students benefit substantially — a compensatory learning pattern only the non-linear causal forest could detect.

---

## Pipeline & Team Roles

| Role | Name | Owner | Responsibility |
|---|---|---|---|
| **1** | Data Engineering | Evans | Cleaned EdNet KT1 interaction logs into `student_level_dataset_R1.csv` (10,000 students) |
| **2** | Synthetic Data | Bashiru Yerima Sadat | Generated `gaussian_dataset.csv` — synthetic Ghanaian school-context variables (SDV Gaussian Copula, quality score 0.9948) |
| **3** | Causal DAG | Kojo Adu-Brempong | Defined the causal structure (treatment, outcome, confounders) underpinning the model |
| **4** | Causal Modelling | Evans | Trained CausalForestDML (`min_samples_leaf=50`), estimated per-student CATE scores |
| **5** | Evaluation & Explainability | Evans | DoWhy refutation tests, SHAP explainability, teacher dashboard, HCAI usability study |
| **6** | Web Application | *(assign)* | Public-facing website translating results into plain English for non-technical stakeholders |

Original Role 4 (before reassignment): Akorsu Emmanuella Amenuveve. Original Role 5: Kwame Asante Jr.

---

## Repository Structure

```
CausalMedia-GH/
├── Role 1/                     # Data engineering notebook + student_level_dataset_R1.csv
├── Role 2/                     # Synthetic data notebook + gaussian_dataset.csv
├── Role 3/                     # Causal DAG definition
├── Role 4/                     # CausalForestDML notebook, model_summary.json, results_with_cate.csv
├── Role 5/                     # Refutation tests, SHAP charts, teacher_dashboard.pdf, HCAI results
├── backend/                    # Node.js + Express + Prisma API (Role 6)
│   ├── prisma/
│   │   ├── schema.prisma
│   │   └── seed.ts
│   ├── src/
│   │   ├── controllers/
│   │   ├── middleware/
│   │   ├── routes/
│   │   └── server.ts
│   └── package.json
├── frontend/                   # React + TypeScript web application (Role 6)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   └── package.json
├── docs/                       # Reports (methodology, briefing, change reports)
└── README.md
```

---

## Tech Stack

### Data Science Pipeline (Roles 1–5)
- **Python** — pandas, NumPy
- **EconML** (Microsoft) — CausalForestDML
- **LightGBM** — nuisance models for DML residualisation
- **SDV** (Synthetic Data Vault) — Gaussian Copula synthesiser
- **DoWhy** — causal refutation testing
- **SHAP** — model explainability
- **ReportLab** — offline teacher PDF dashboard

### Web Application (Role 6)

| Layer | Choice | Why |
|---|---|---|
| Backend runtime | Node.js v20 LTS + TypeScript | Type safety across the stack |
| Web framework | Express.js | Lightweight, well-documented, fast to ship for a student team |
| ORM / DB | Prisma ORM + PostgreSQL (SQLite for local dev) | Type-safe queries, painless migrations |
| Auth | JWT (`jsonwebtoken`) + `bcryptjs` | Stateless auth, role-based access (Teacher/Student) |
| Real-time | Socket.io | Live "quiz submitted" alerts on the teacher dashboard |
| Validation | Zod | Runtime request validation |
| Frontend framework | React 18 + TypeScript + Vite | Fast dev/build cycle |
| Styling | Tailwind CSS + shadcn/ui | Accessible, consistent components without heavy custom CSS |
| Charts | Recharts | SHAP waterfall/beeswarm and CATE visualisations |
| Data fetching | TanStack Query | Caching, background refresh |
| State | Zustand | Minimal global state (auth session, selected student) |
| Hosting | Vercel (frontend) · Render/Railway (backend) · HuggingFace Hub (98MB model file) | Free-tier friendly, matches existing `causalmedia-gh.vercel.app` deployment |

---

## Getting Started

### Prerequisites
- Node.js v20+
- Python 3.10+ (for the data science notebooks)
- PostgreSQL (or SQLite for local development)

### Backend

```bash
cd backend
npm install
npx prisma migrate dev
npx prisma db seed
npm run dev
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Data Science Notebooks

```bash
pip install -r requirements.txt
jupyter notebook
```

Notebooks are numbered by role (`Role 1/`, `Role 2/`, …) and are designed to run in dependency order: 1 → 2 → 3 → 4 → 5.

---

## Data Sources

| File | Source | Shape | Role |
|---|---|---|---|
| `student_level_dataset_R1.csv` | EdNet KT1 (real interaction logs) | 10,000 × 10 | Role 1 |
| `gaussian_dataset.csv` | SDV Gaussian Copula synthetic generator | 50,000 × 6 (10,000 sampled) | Role 2 |
| `results_with_cate.csv` | Merged + CATE-scored output | 10,000 × 17+ | Role 4 |

**Treatment (T):** `multimedia_engagement` — proportion of interactions with elapsed time above the student's Q75 threshold.
**Outcome (Y):** `performance_gain` — correctness-rate improvement from the first to final third of chronological interactions.
**Confounders (X):** 12 variables spanning prior achievement, engagement consistency, session behaviour, and school context (bandwidth, tablet access, teacher qualification, school resources).

---

## Methodology Summary

1. **Baseline progression** — Naïve correlation → OLS → Linear DML → CausalForestDML, demonstrating the selection bias present in raw observational data.
2. **Main estimator** — CausalForestDML (EconML), LightGBM nuisance models, 5-fold cross-fitting, `honest=True`, `min_samples_leaf=50`, 1,000 trees, ensembled across 3 seeds (42, 123, 777).
3. **Refutation testing (Role 5)** — Four DoWhy tests: placebo treatment, random common cause, data subset, and bootstrap refuters.
4. **Explainability (Role 5)** — SHAP beeswarm, dependence, and per-profile waterfall charts computed on a 500-student sample.
5. **Communication (Role 5 + 6)** — Offline PDF teacher dashboard plus an interactive web application, both translating statistical findings into plain-language, actionable recommendations.
6. **Validation (Role 5)** — HCAI usability study with 3 SHS teachers comparing raw CATE numbers (Condition A) vs. SHAP-explained profiles (Condition B): comprehension improved from 1.77/5 to 3.77/5 (Cohen's d > 0.8).

---

## Web Application (Role 6)

The web app makes the project's technical findings usable by non-technical teachers and school administrators.

**Core features:**
- **Public landing page** — one-paragraph, jargon-free explanation of the study and its purpose
- **Teacher Dashboard** — class-level summary stats (average CATE, high-uplift count, low-bandwidth count), student roster filterable by location/bandwidth/CATE
- **Student CATE Explorer** — per-student SHAP waterfall chart with a one-sentence plain-English explanation per contributing factor
- **Live quiz alerts** — real-time notification via Socket.io when a student submits a video quiz
- **Assessment engine** — teachers create timestamped video quizzes; students complete them and receive an immediate performance-gain readout
- **Glossary tooltips** — inline definitions for terms like CATE, SHAP, and confounder
- **Low-bandwidth mode** — lazy-loaded charts and a text-only fallback, reflecting that roughly half of students in the study context report low-bandwidth access

**Live deployment:** [causalmedia-gh.vercel.app](https://causalmedia-gh.vercel.app)

See [`Backend.pdf`](./docs/Backend.pdf) for the full API specification, Prisma schema, and unit-by-unit backend work breakdown.

---

## Output Artefacts

| File | Role | Status |
|---|---|---|
| `results_with_cate.csv` | 4 | Committed to GitHub |
| `model_summary.json` | 4 | Committed to GitHub |
| `cf_model_42.pkl` (98MB) | 4 | HuggingFace Hub / Kaggle — upload pending |
| `refutation_results.json` | 5 | Committed to GitHub |
| `shap_beeswarm.png`, `shap_dependence.png` | 5 | Committed to GitHub |
| `shap_waterfall_*.png` (3 profiles) | 5 | Committed to GitHub |
| `shap_ranking_comparison.csv` | 5 | Committed to GitHub |
| `teacher_dashboard.pdf` | 5 | Committed to GitHub |
| `survey_results.csv`, `hcai_summary.json` | 5 | Committed to GitHub |

**Open science archiving:**
1. **GitHub** — code, notebooks, and CSV outputs ([github.com/EvansAmarh/CausalMedia-GH](https://github.com/EvansAmarh/CausalMedia-GH))
2. **HuggingFace Hub / Kaggle** — `cf_model_42.pkl` (upload pending)
3. **Zenodo** — `results_with_cate.csv` + `model_summary.json` (DOI pending)

Google Drive is used only as a working backup and is **not** cited as a permanent archive.

---

## Limitations

- Population-level ATE 95% CI includes zero — the study reports a directional, exploratory finding, not a confirmed population effect.
- School-context variables (Role 2) are synthetically generated and statistically validated against seed data only, not against real Ghanaian administrative records.
- Negative CATEs for low-achieving students should not be read as "video harms these students" — more likely a prerequisite-knowledge threshold effect requiring longitudinal data to confirm.
- HCAI usability study used n=3 teachers; a confirmatory study with n≥28 is needed for statistical significance (current results are practically, not statistically, significant).
- `cf_model_42.pkl` exceeds GitHub's 25MB limit and must be regenerated from the Role 4 notebook (~10–15 min) or downloaded from HuggingFace once uploaded.

---

## Ethical Compliance

This project operates under **Path D ethics governance** — a validated synthetic supplement to a publicly available, anonymised system-log dataset (EdNet KT1). No real Ghanaian student records are processed. This is consistent with Ghana's Data Protection Act, 2012 (Act 843), which exempts fully anonymised and synthetic data from individual consent requirements.

---

## Contributors

**NexusLearn Group 4**, KNUST Department of Computer Science
Supervisor: **Dr. Eric Osei**

| Name | Role(s) |
|---|---|
| Evans Amarh | Roles 1, 4 |
| Bashiru Yerima Sadat | Role 6 |
| Kojo Adu-Brempong | Role 2 |
| Akorsu Emmanuella Amenuveve | Role 3 |
| Kwame Asante Jr. | Role 5 |

---
