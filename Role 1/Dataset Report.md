# Analysis Report: Role1_data_engineering.ipynb

## Overview
This Jupyter Notebook implements a comprehensive data engineering pipeline for the **EdNet-KT1 dataset**. The primary goal is to transform raw student-question interaction logs into a structured, student-level feature dataset suitable for downstream machine learning or causal analysis.

## 1. Data Pipeline & Processing
The notebook follows a structured workflow to handle the massive EdNet dataset:
- **Environment Setup**: Utilizes Google Colab environment, mounting Google Drive to access the source data.
- **Data Acquisition**: Extracts `EdNet-KT1.zip`, which contains interaction logs for approximately **784,309 students**.
- **Sampling Strategy**: Given the scale, the script samples **30,000 student files** for initial processing to ensure computational efficiency.
- **Temporal Alignment**: Timestamps are converted from milliseconds to standard datetime format, spanning from **April 2017 to December 2019**.

## 2. Feature Engineering Logic
The core value of this notebook is the derivation of meaningful educational metrics from low-level interaction data:

### Derived Core Metrics
- **Correctness (Majority Vote)**: Since ground truth answers weren't directly provided in the raw logs, the notebook assumes the most frequent answer globally for a `question_id` is the correct one.
- **Engagement (Time-based)**: A binary `high_engagement` feature is created by comparing the `elapsed_time` of an interaction against the student's own median response time.

### Student-Level Aggregates
The final dataset collapses interactions into 10 key features per student:
| Feature | Description |
| :--- | :--- |
| `multimedia_engagement` | Average engagement rate across all interactions. |
| `performance_gain` | Improvement in correctness from the first 1/3 of interactions to the last 1/3. |
| `prior_achievement` | Correctness rate in the initial interaction window. |
| `early_struggle` | Inverse of prior achievement (1 - initial correctness). |
| `consistency` | Ratio of active days to total days in the interaction window. |
| `skill_coverage` | Count of unique questions attempted by the student. |
| `session_duration_avg`| Mean elapsed time per question. |
| `total_interactions`| Total number of questions answered. |

## 3. Data Quality & Output
- **Validation**: The notebook includes a validation suite checking for minimum row counts (10,000 final students), zero missing values, and proper feature ranges (e.g., probability values between 0 and 1).
- **Final Output**: Produces `student_level_dataset.csv`, a clean dataset featuring **10,000 students** with 10 engineered columns.
- **Portability**: Includes a `files.download()` step to export the final CSV for use in other notebooks (e.g., `Trained_Model.ipynb`).

## 4. Technical Stack
- **Languages**: Python (Jupyter Notebook)
- **Primary Libraries**: `pandas` (Data manipulation), `numpy` (Numerical operations), `os`/`random` (File handling), `google.colab` (Environment integration).

---
**Summary**: The notebook effectively bridges the gap between raw CSV logs and a "ML-ready" dataset by implementing custom heuristics for correctness and engagement, while managing the logistical challenges of a large-scale dataset.
