# Role 2 — Synthetic Context Generation & Validation

Part of the CausalMedia-GH project. Generates and validates Ghana-specific
synthetic contextual variables (school location, tablet access, bandwidth,
resource level, teacher qualification) that supplement Role 1's EdNet-based
learning dataset.

## Installation

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the pipeline

Run scripts in this order — each one depends on the output of the last:

```bash
# 1. Generate the seed dataset (10,000 records)
python src/generate_seed.py

# 2. Train both synthesizers
python src/train_ctgan.py        # slower — GAN training, ~5 min on CPU
python src/train_gaussian.py     # fast — closed-form fit

# 3. Evaluate quality (produces the numbers for the paper)
python src/evaluate.py

# 4. Run statistical validation (KS / Chi-square tests)
python src/ks_validation.py

# 5. Generate figures
python src/visualization.py
python src/figure2_flowchart.py
```

## What each script produces

| Script | Output |
|---|---|
| `generate_seed.py` | `data/seed/seed_dataset.csv` |
| `train_ctgan.py` | `data/synthetic/ctgan_dataset.csv`, `data/reports/ctgan_synthesizer.pkl` |
| `train_gaussian.py` | `data/synthetic/gaussian_dataset.csv`, `data/reports/gaussian_synthesizer.pkl`, `data/reports/metadata.json` |
| `evaluate.py` | `data/reports/sdmetrics_report.json`, `data/reports/sdmetrics_summary.md` |
| `ks_validation.py` | `data/reports/statistical_validation.md` |
| `visualization.py` | `figures/figure1...png`, `figure3...png`, `figure4...png`, `figure5...png` |
| `figure2_flowchart.py` | `figures/figure2_fusion_flowchart.png` |

## Important notes

- **Random seed is fixed at 42** throughout for reproducibility.
- **CTGAN vs. Gaussian Copula**: both are trained and evaluated; the
  winner (by SDMetrics overall quality score) is selected automatically
  and logged in `data/reports/sdmetrics_summary.md`, including a
  ready-to-paste justification sentence for the paper.
- **The synthetic data is a supplement, not a substitute** for real
  Ghanaian school data. See `docs/ethics.md` for the full statement —
  this framing must be preserved in any paper or report text.
- **Citations pending**: the probability distributions in
  `generate_seed.py` are placeholders until the team supplies GES/NCTE
  source citations. Search for `[citation pending]` in that file.

## Publishing

Once the pipeline has been run and reviewed:

1. Push to GitHub, tag a release.
2. Create a Zenodo record (type: Dataset) containing the SDV pipeline
   notebook, `data/reports/metadata.json` (seed dataset schema), and
   `data/reports/sdmetrics_report.json` / `.md`.
3. Add the resulting DOI to Section 2.14 of the paper.
