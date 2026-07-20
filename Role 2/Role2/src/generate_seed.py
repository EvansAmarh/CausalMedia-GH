"""
generate_seed.py
-----------------
Generates the SEED dataset: 10,000 synthetic student/school records
with Ghana-specific contextual variables, sampled from probability
distributions grounded in published education statistics.

IMPORTANT: The distribution values below (e.g. 0.40 / 0.35 / 0.25 for
location) are PLACEHOLDERS. Replace them with the real published
figures once you have the GES/NCTE citation, and record the citation
in docs/methodology.docx. Until then, mark them "[citation pending]"
in your evidence log — do NOT present them as sourced.

Run:
    python src/generate_seed.py
Output:
    data/seed/seed_dataset.csv
"""

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------
# 1. Reproducibility — always fix the seed so results can be regenerated
# ----------------------------------------------------------------------
SEED = 42
rng = np.random.default_rng(SEED)

N_RECORDS = 10_000

# ----------------------------------------------------------------------
# 2. Define each variable's possible values and probability distribution
#    Replace the probabilities with cited GES/NCTE figures when available.
# ----------------------------------------------------------------------

# School Location — [citation pending: GES report]
location_values = ["rural", "peri-urban", "urban"]
location_probs = [0.40, 0.35, 0.25]

# Tablet Access — [citation pending: GES/NCTE report]
tablet_values = ["no_access", "shared_access", "individual_access"]
tablet_probs = [0.45, 0.35, 0.20]

# Bandwidth — [citation pending: NCTE report]
bandwidth_values = ["low", "medium", "high"]
bandwidth_probs = [0.50, 0.35, 0.15]

# School Resource Level — [citation pending: GES report]
resource_values = ["low", "medium", "high"]
resource_probs = [0.45, 0.40, 0.15]

# Teacher Qualification — [citation pending: GES/NCTE report]
teacher_qual_values = ["untrained", "diploma", "degree", "postgraduate"]
teacher_qual_probs = [0.15, 0.40, 0.35, 0.10]


def sample_column(values, probs, n, rng):
    """Sample a categorical column given values, probabilities, and count."""
    assert abs(sum(probs) - 1.0) < 1e-6, "Probabilities must sum to 1.0"
    return rng.choice(values, size=n, p=probs)


def generate_seed_dataset(n=N_RECORDS, seed=SEED) -> pd.DataFrame:
    local_rng = np.random.default_rng(seed)

    df = pd.DataFrame({
        "student_id": [f"STU{str(i).zfill(6)}" for i in range(1, n + 1)],
        "location": sample_column(location_values, location_probs, n, local_rng),
        "tablet_access": sample_column(tablet_values, tablet_probs, n, local_rng),
        "bandwidth": sample_column(bandwidth_values, bandwidth_probs, n, local_rng),
        "resource_level": sample_column(resource_values, resource_probs, n, local_rng),
        "teacher_qualification": sample_column(
            teacher_qual_values, teacher_qual_probs, n, local_rng
        ),
    })
    return df


if __name__ == "__main__":
    df = generate_seed_dataset()

    out_path = "data/seed/seed_dataset.csv"
    df.to_csv(out_path, index=False)

    print(f"Seed dataset generated: {len(df)} records")
    print(f"Saved to: {out_path}")
    print("\nColumn distributions (sanity check — should roughly match probs above):")
    for col in df.columns:
        if col == "student_id":
            continue
        print(f"\n{col}:")
        print(df[col].value_counts(normalize=True).round(3))
