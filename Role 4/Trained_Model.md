# Analysis Report: Trained_Model.ipynb

## Overview
This notebook executes a **Causal Discovery and Inference** workflow using advanced machine learning techniques. It aims to isolate the causal impact of **multimedia engagement** on student **performance gains**, accounting for environmental and socioeconomic confounders.

## 1. Experimental Design
The study uses a "Merging of Worlds" approach, combining real-world student interaction patterns with synthetic school context data.

- **Treatment ($T$)**: `multimedia_engagement` (continuous).
- **Outcome ($Y$)**: `performance_gain` (improvement in score between early and late sessions).
- **Confounders ($X$)**: 12 variables including:
  - Socioeconomic: `tablet_access`, `bandwidth_category`, `location`.
  - Educational: `prior_achievement`, `teacher_qual`, `school_resource_level`.
  - Behavioural: `consistency`, `early_struggle`, `peer_activity_index`.

## 2. Methodology & Baselines
The notebook implements a progression of complexity to demonstrate the need for causal methods:

| ID | Model Type | Result (ATE/Coef) | Insight |
| :--- | :--- | :--- | :--- |
| **B1** | Naive Pearson Correlation | 0.0500 | Simple association; ignores bias. |
| **B2** | OLS (Linear Regression) | 0.0949 | Adjusts for linear confounding. |
| **B3** | Linear DML (LGBM) | 0.0665 | Semi-parametric causal estimate. |
| **Main**| **Causal Forest DML** | **0.0392** | Non-parametric, robust to non-linear bias. |

## 3. Key Findings
- **ATE (Average Treatment Effect)**: The ensemble ATE across multiple seeds is **0.0392 ± 0.0108**.
- **Bias Correction**: The **Inflation Ratio (1.28x)** indicates that naive methods (B1) overestimate the benefit of multimedia engagement by roughly 28% due to selection bias.
- **Statistical Significance**: The 95% Confidence Interval $[-0.602, 0.681]$ includes zero for the primary seed, suggesting the effect is not universally robust across the entire population at a 5% alpha level.
- **Heterogeneous Effects (CATE)**: Significant variance in impact was found across subgroups:
  - **Rural Students**: Showed significantly higher causal gains (**~0.12**) compared to Urban students (**~0.01**).
  - **Low Bandwidth (Cat 1)**: Experienced the highest uplift (**0.126**), suggesting multimedia tools provide the most value where resources are scarce.

## 4. Technical Implementation
- **Eco-system**: Built on top of the `econml` library by Microsoft Research.
- **Base Learners**: `LightGBM` (LGBMRegressor) used for modeling the outcome ($Y|X$) and treatment assignment ($T|X$).
- **Robustness**: Uses an "Ensemble of Seeds" approach to ensure findings aren't artifacts of random initialization.

---
**Summary**: The analysis confirms that while multimedia engagement has a positive association with performance, its *causal* benefit is slightly lower than association suggests and is highly dependent on the student's geographic and technological context.
