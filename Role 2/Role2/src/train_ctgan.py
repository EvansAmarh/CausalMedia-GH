"""
train_ctgan.py
---------------
Trains an SDV CTGANSynthesizer on the seed dataset and generates
50,000 synthetic records. CTGAN is a GAN-based synthesizer, so
training takes noticeably longer than Gaussian Copula — expect a
few minutes on CPU for this dataset size.

Run:
    python src/train_ctgan.py
Requires:
    data/seed/seed_dataset.csv  (run generate_seed.py first)
Output:
    data/synthetic/ctgan_dataset.csv
"""

import pandas as pd
from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer

SEED_PATH = "data/seed/seed_dataset.csv"
OUT_PATH = "data/synthetic/ctgan_dataset.csv"
N_SYNTHETIC = 50_000
RANDOM_STATE = 42

# CTGAN epochs — 300 is the SDV default and reasonable for a paper-grade
# result. Drop to ~50 while you're debugging the pipeline (much faster),
# then run the full 300 for your final numbers.
EPOCHS = 300

if __name__ == "__main__":
    seed_df = pd.read_csv(SEED_PATH)
    print(f"Loaded seed dataset: {seed_df.shape}")

    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(seed_df)
    metadata.update_column(column_name="student_id", sdtype="id")
    metadata.set_primary_key("student_id")

    synthesizer = CTGANSynthesizer(
        metadata,
        epochs=EPOCHS,
        verbose=True,   # prints loss per epoch so you can see it's working
    )

    print(f"Training CTGAN for {EPOCHS} epochs...")
    synthesizer.fit(seed_df)
    print("CTGAN training complete.")

    synthetic_df = synthesizer.sample(num_rows=N_SYNTHETIC)
    print(f"Generated synthetic dataset: {synthetic_df.shape}")

    synthetic_df.to_csv(OUT_PATH, index=False)
    print(f"Saved to: {OUT_PATH}")

    synthesizer.save("data/reports/ctgan_synthesizer.pkl")
    print("Saved fitted model to: data/reports/ctgan_synthesizer.pkl")
