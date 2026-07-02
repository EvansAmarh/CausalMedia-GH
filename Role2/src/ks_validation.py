"""
ks_validation.py
-----------------
Statistical validation comparing real (seed) vs. synthetic distributions.

IMPORTANT: The Kolmogorov-Smirnov (KS) test is defined for NUMERIC /
CONTINUOUS variables. If your final variable set is all-categorical
(as in the starter example — location, tablet_access, bandwidth,
resource_level, teacher_qualification), a KS test doesn't strictly
apply to them. This script:

  1. Runs a real KS test on any numeric columns present.
  2. Runs a Chi-square goodness-of-fit test on categorical columns
     (the correct analogue of "does the distribution match" for
     categorical data).

If your team adds numeric variables later (e.g. a continuous
"distance to nearest urban center" or "years of teaching experience"),
they'll automatically be picked up by the KS branch below.

Do NOT claim "KS test passed, p > 0.05" for categorical variables in
your report — cite the Chi-square result instead and say so explicitly.
This is the kind of imprecision that got Role 2 marked down.

Run:
    python src/ks_validation.py
Requires:
    data/seed/seed_dataset.csv
    data/synthetic/final_synthetic_dataset.csv (or point to gaussian/ctgan directly)
Output:
    data/reports/statistical_validation.md
"""

import pandas as pd
from scipy import stats

SEED_PATH = "data/seed/seed_dataset.csv"
# Point this at whichever dataset was selected in evaluate.py.
# Change to ctgan_dataset.csv if CTGAN wins instead.
FINAL_SYNTHETIC_PATH = "data/synthetic/gaussian_dataset.csv"
OUT_PATH = "data/reports/statistical_validation.md"

ID_COLUMNS = {"student_id"}


def run_ks_test(real_series, synth_series):
    statistic, p_value = stats.ks_2samp(real_series, synth_series)
    return statistic, p_value


def run_chi_square_test(real_series, synth_series):
    """
    Chi-square goodness-of-fit: does the synthetic category distribution
    match the real category distribution's shape?
    Uses the real data's proportions as the "expected" distribution,
    scaled to the synthetic sample size.
    """
    real_counts = real_series.value_counts()
    synth_counts = synth_series.value_counts()

    # Align categories (some may be missing in one or the other)
    categories = sorted(set(real_counts.index) | set(synth_counts.index))
    real_counts = real_counts.reindex(categories, fill_value=0)
    synth_counts = synth_counts.reindex(categories, fill_value=0)

    # Expected = real proportions scaled to synthetic sample size
    n_synth = synth_counts.sum()
    expected = (real_counts / real_counts.sum()) * n_synth

    statistic, p_value = stats.chisquare(f_obs=synth_counts, f_exp=expected)
    return statistic, p_value


if __name__ == "__main__":
    real_df = pd.read_csv(SEED_PATH)
    synth_df = pd.read_csv(FINAL_SYNTHETIC_PATH)

    numeric_cols = [
        c for c in real_df.columns
        if c not in ID_COLUMNS and pd.api.types.is_numeric_dtype(real_df[c])
    ]
    categorical_cols = [
        c for c in real_df.columns
        if c not in ID_COLUMNS and c not in numeric_cols
    ]

    print(f"Numeric columns (KS test): {numeric_cols or 'none'}")
    print(f"Categorical columns (Chi-square test): {categorical_cols}")

    results = []

    for col in numeric_cols:
        stat, p = run_ks_test(real_df[col], synth_df[col])
        results.append({
            "variable": col, "test": "KS", "statistic": round(stat, 4),
            "p_value": round(p, 4), "passes_p>0.05": p > 0.05,
        })

    for col in categorical_cols:
        stat, p = run_chi_square_test(real_df[col], synth_df[col])
        results.append({
            "variable": col, "test": "Chi-square", "statistic": round(stat, 4),
            "p_value": round(p, 4), "passes_p>0.05": p > 0.05,
        })

    results_df = pd.DataFrame(results)
    print("\n", results_df.to_string(index=False))

    all_pass = results_df["passes_p>0.05"].all()

    with open(OUT_PATH, "w") as f:
        f.write("# Statistical Validation Report\n\n")
        f.write(
            "KS tests are reported for numeric variables. Categorical "
            "variables are validated with a Chi-square goodness-of-fit "
            "test comparing synthetic category proportions against the "
            "real (seed) proportions, which is the correct analogue of "
            "the KS test for categorical data.\n\n"
        )
        f.write("| Variable | Test | Statistic | p-value | p > 0.05 |\n")
        f.write("|---|---|---|---|---|\n")
        for r in results:
            f.write(
                f"| {r['variable']} | {r['test']} | {r['statistic']} | "
                f"{r['p_value']} | {'Yes' if r['passes_p>0.05'] else 'No'} |\n"
            )
        f.write(f"\n**All variables pass (p > 0.05):** {'Yes' if all_pass else 'No'}\n")

    print(f"\nSaved: {OUT_PATH}")
    print(f"All variables pass p > 0.05: {all_pass}")
