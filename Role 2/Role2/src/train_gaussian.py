"""
train_gaussian.py
------------------
Trains an SDV GaussianCopulaSynthesizer on the seed dataset and
generates 50,000 synthetic records.

Run:
    python src/train_gaussian.py
Requires:
    data/seed/seed_dataset.csv  (run generate_seed.py first)
Output:
    data/synthetic/gaussian_dataset.csv
"""

import pandas as pd
from sdv.metadata import SingleTableMetadata
from sdv.single_table import GaussianCopulaSynthesizer

SEED_PATH = "data/seed/seed_dataset.csv"
OUT_PATH = "data/synthetic/gaussian_dataset.csv"
N_SYNTHETIC = 50_000
RANDOM_STATE = 42

if __name__ == "__main__":
    # 1. Load seed data
    seed_df = pd.read_csv(SEED_PATH)
    print(f"Loaded seed dataset: {seed_df.shape}")

    # 2. Auto-detect metadata (column types) from the seed data.
    #    SDV needs this to know which columns are categorical vs numeric etc.
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(seed_df)

    # student_id is a unique identifier, not a variable to model —
    # tell SDV to treat it as an ID column so it doesn't try to learn
    # a distribution over it.
    metadata.update_column(column_name="student_id", sdtype="id")
    metadata.set_primary_key("student_id")

    # Save metadata to disk — SDV recommends this for reproducibility,
    # and you'll want it in the Zenodo deposit alongside the notebook.
    metadata.save_to_json("data/reports/metadata.json", mode="overwrite")


    # 3. Train the synthesizer
    synthesizer = GaussianCopulaSynthesizer(metadata)
    synthesizer.fit(seed_df)
    print("Gaussian Copula training complete.")

    # 4. Generate synthetic records
    synthetic_df = synthesizer.sample(num_rows=N_SYNTHETIC)
    print(f"Generated synthetic dataset: {synthetic_df.shape}")

    # 5. Save
    synthetic_df.to_csv(OUT_PATH, index=False)
    print(f"Saved to: {OUT_PATH}")

    # 6. Also save the fitted synthesizer, in case you want to resample
    #    later without retraining (useful for the Zenodo notebook)
    synthesizer.save("data/reports/gaussian_synthesizer.pkl")
    print("Saved fitted model to: data/reports/gaussian_synthesizer.pkl")
