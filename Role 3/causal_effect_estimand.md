# Analysis Report: causal_effect_estimand.ipynb

## Overview
This notebook serves as the **theoretical foundation** for the causal inference pipeline. It defines the structural relationships between variables using a Directed Acyclic Graph (DAG) and formally identifies the causal effect of multimedia engagement on student performance.

## 1. Causal Model Architecture
The notebook constructs a rigorous **Structural Causal Model (SCM)** with the following configuration:

- **Nodes**: 14 variables (1 Treatment, 1 Outcome, 12 Contextual Factors).
- **Edges**: 24 causal paths defining how confounders influence both the treatment and the outcome.
- **Identification Framework**: Built using the **DoWhy** library.

### Variables & Roles
| Role | Variables |
| :--- | :--- |
| **Treatment ($T$)** | `multimedia_ratio` |
| **Outcome ($Y$)** | `performance_gain` |
| **Confounders ($W$)** | `prior_achievement`, `bandwidth_category`, `early_struggle`, `consistency`, `tablet_access`, etc. |
| **Outcome-Only** | `teacher_qual` (Affects $Y$ but not $T$). |

## 2.7 Identification Strategy
The notebook applies the **Backdoor Criterion** to verify if the causal effect is identifiable from the data.

**Equation 1**

$$
\mathbb{E}[Y(t)-Y(0)]
=
\mathbb{E}_{X}\!\left[
\mathbb{E}[Y \mid T=t, X]
-
\mathbb{E}[Y \mid T=0, X]
\right].
\tag{1}
$$

Here, $Y(t)$ is a student's potential performance gain under multimedia exposure level $t$; $Y(0)$ is the same student's potential performance gain under the reference exposure level 0; $T$ is the observed continuous multimedia ratio; $t$ is the exposure level being contrasted with 0; $X$ is the vector of observed pre-treatment adjustment variables in the DAG; $\mathbb{E}[\cdot]$ denotes expectation; and $\mathbb{E}_{X}[\cdot]$ averages the conditional contrast over the observed distribution of $X$.

- **Backdoor Adjustment**: The model confirms that by adjusting for the 12 identified confounders, all "backdoor paths" (spurious correlations) between Multimedia Ratio and Performance Gain are blocked.
- **Unconfoundedness Assumption**: Conditional on the measured pre-treatment covariates $X$, treatment assignment is independent of the potential outcomes, $Y(t) \perp T \mid X$ for every exposure level $t$. Equivalently, after adjustment for $X$, no unobserved variable $U$ jointly causes multimedia exposure and performance gain. Together with consistency, positivity, and no interference, this assumption identifies Equation 1 from the observed data.

`teacher_qual` is modeled as an outcome-only predictor because teacher quality plausibly affects student performance gain, while multimedia exposure is recorded from students' platform activity and is not assigned by teacher quality in the study design.

Because the student and synthetic school files use independently generated identifiers, the notebook reproducibly assigns a fixed-seed sample of school profiles to the 10,000 student rows rather than claiming an unsupported key-based linkage.

## 3. Key Deliverables
- **Formal Estimand**: Generates a non-parametric expression for the Average Treatment Effect (ATE), saved as `identified_estimand.txt`.
- **DAG Visualization**: Produces a high-resolution publication-quality DAG (`figure1_dag_causalmedia_gh.png`) illustrating the causal hierarchy.
- **Pre-registration Ready**: The logic is explicitly designed for **OSF (Open Science Framework) pre-registration**, ensuring scientific transparency.

## 4. Technical Stack
- **Causal Logic**: `dowhy` (Identification and Estimation framework).
- **Graph Theory**: `networkx` (DAG manipulation).
- **Visualization**: `matplotlib` with custom aesthetic styling (Glassmorphism inspired colors).

---
**Summary**: This notebook transitions the project from "simple machine learning" to **formal causal science**. By mathematically proving that the effect is identifiable, it justifies the use of the advanced models (like Causal Forests) seen in subsequent stages of the project.
