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

## 2. Identification Strategy
The notebook applies the **Backdoor Criterion** to verify if the causal effect is identifiable from the data. 

- **Backdoor Adjustment**: The model confirms that by adjusting for the 12 identified confounders, all "backdoor paths" (spurious correlations) between Multimedia Ratio and Performance Gain are blocked.
- **Unconfoundedness Assumption**: The identification relies on the assumption that no unobserved variables ($U$) simultaneously influence both the treatment and the outcome.

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
