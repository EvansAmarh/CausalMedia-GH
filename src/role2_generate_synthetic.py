import pandas as pd
import numpy as np

# SDV imports
from sdv.metadata import Metadata
from sdv.single_table import CTGANSynthesizer, GaussianCopulaSynthesizer
from sdv.evaluation.single_table import evaluate_quality

# -----------------------------
# PART 1: Generate Seed Dataset
# -----------------------------

np.random.seed(42)
n = 10000

locations = np.random.choice(
    ['Urban', 'Peri-urban', 'Rural'],
    size=n,
    p=[0.60, 0.25, 0.15]
)

def tablet_access(loc):
    probs = {'Urban': 0.85, 'Peri-urban': 0.45, 'Rural': 0.20}
    return np.random.binomial(1, probs[loc])

def bandwidth(loc):
    mapping = {'Urban': 3, 'Peri-urban': 2, 'Rural': 1}
    return mapping[loc]

def resource_level(loc):
    if loc == 'Urban':
        return np.random.choice([2, 3], p=[0.3, 0.7])
    elif loc == 'Peri-urban':
        return np.random.choice([1, 2, 3], p=[0.2, 0.6, 0.2])
    else:
        return np.random.choice([1, 2], p=[0.8, 0.2])

def teacher_qual(loc):
    means = {'Urban': 0.8, 'Peri-urban': 0.6, 'Rural': 0.4}
    value = np.random.normal(means[loc], 0.05)
    return np.clip(value, 0, 1)

seed = pd.DataFrame({
    'student_id': range(1, n + 1),
    'location': locations,
})

seed['tablet_access'] = seed['location'].apply(tablet_access)
seed['bandwidth_category'] = seed['location'].apply(bandwidth)
seed['school_resource_level'] = seed['location'].apply(resource_level)
seed['teacher_qual'] = seed['location'].apply(teacher_qual)

seed.to_csv('data/processed/seed_data.csv', index=False)
print("Seed data saved.")

# -----------------------------
# PART 2: Load Seed Data
# -----------------------------

real_data = pd.read_csv('data/processed/seed_data.csv')

# Detect metadata automatically
metadata = Metadata.detect_from_dataframe(real_data)

# -----------------------------
# PART 3: Train Models
# -----------------------------

print("Training CTGAN...")
ctgan = CTGANSynthesizer(metadata)
ctgan.fit(real_data)
synthetic_ctgan = ctgan.sample(50000)

print("Training Gaussian Copula...")
gc = GaussianCopulaSynthesizer(metadata)
gc.fit(real_data)
synthetic_gc = gc.sample(50000)

# -----------------------------
# PART 4: Evaluate Quality
# -----------------------------

print("Evaluating CTGAN...")
report_ctgan = evaluate_quality(real_data, synthetic_ctgan, metadata)
score_ctgan = report_ctgan.get_score()

print("Evaluating Gaussian Copula...")
report_gc = evaluate_quality(real_data, synthetic_gc, metadata)
score_gc = report_gc.get_score()

print("CTGAN Score:", score_ctgan)
print("Gaussian Copula Score:", score_gc)

# -----------------------------
# PART 5: Select Best Model
# -----------------------------

if score_ctgan > score_gc:
    best_name = "CTGAN"
    synthetic_best = synthetic_ctgan
    best_score = score_ctgan
else:
    best_name = "GaussianCopula"
    synthetic_best = synthetic_gc
    best_score = score_gc

print("Best model:", best_name)
print("Best score:", best_score)

# Save best synthetic data
synthetic_best.to_csv(
    'data/synthetic/synthetic_school_data.csv',
    index=False
)

# Save quality report
with open('reports/quality_report.txt', 'w') as f:
    f.write(f"CTGAN Score: {score_ctgan}\n")
    f.write(f"Gaussian Copula Score: {score_gc}\n")
    f.write(f"Best Model: {best_name}\n")
    f.write(f"Best Score: {best_score}\n")

print("Synthetic data saved.")
print("Quality report saved.")

# PART 6: Statistical Validation (KS Test)

from scipy.stats import ks_2samp

numeric_cols = [
    'bandwidth_category',
    'school_resource_level',
    'teacher_qual'
]

for col in numeric_cols:
    stat, p = ks_2samp(real_data[col], synthetic_best[col])
    print(f'{col}: p={p:.4f}')

# PART 7: Data Visualization (Real Data Distribution)

import matplotlib.pyplot as plt

real_data['location'].value_counts(normalize=True).plot(kind='bar')
plt.title('Seed Data Location Distribution')
plt.tight_layout()

plt.savefig('reports/figures/location_distribution.png')
plt.close()

print("Location distribution plot saved.")