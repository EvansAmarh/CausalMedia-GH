"""
evaluate.py
------------
Runs SDMetrics quality evaluation on BOTH synthetic datasets
(CTGAN and Gaussian Copula) against the real seed data, and prints/
saves a side-by-side comparison. This is the script that produces
the numbers you need for the paper -- do not write your model
justification until this has run.

Run:
    python src/evaluate.py
Requires:
    data/seed/seed_dataset.csv
    data/synthetic/ctgan_dataset.csv
    data/synthetic/gaussian_dataset.csv
    data/reports/metadata.json
Output:
    data/reports/sdmetrics_report.json   (machine-readable scores)
    data/reports/sdmetrics_summary.md    (human-readable, paste into paper)
"""

import itertools
import json
import pandas as pd
from sdv.metadata import Metadata
from sdmetrics.reports.single_table import QualityReport
from sdmetrics.column_pairs.statistical import ContingencySimilarity
from sdmetrics.column_pairs.statistical import CorrelationSimilarity

SEED_PATH = "data/seed/seed_dataset.csv"
CTGAN_PATH = "data/synthetic/ctgan_dataset.csv"
GAUSSIAN_PATH = "data/synthetic/gaussian_dataset.csv"
METADATA_PATH = "data/reports/metadata.json"


def compute_column_pair_trends(real_df, synthetic_df, metadata_dict):
    """
    Manually compute the average pairwise column-trend score.

    NOTE: In this SDMetrics version, QualityReport's built-in
    "Column Pair Trends" property returns NaN for all-categorical
    tables (a known aggregation bug -- the underlying per-pair metric
    computes correctly when called directly). This function
    reproduces that property by hand: for every pair of columns, use
    ContingencySimilarity if both are categorical/boolean, or
    CorrelationSimilarity if both are numerical, then average all
    pairwise scores.
    """
    columns = metadata_dict["columns"]
    col_names = [c for c in columns if columns[c].get("sdtype") != "id"]

    scores = []
    for col_a, col_b in itertools.combinations(col_names, 2):
        type_a = columns[col_a]["sdtype"]
        type_b = columns[col_b]["sdtype"]
        try:
            if type_a in ("categorical", "boolean") and type_b in ("categorical", "boolean"):
                score = ContingencySimilarity.compute(
                    real_data=real_df[[col_a, col_b]],
                    synthetic_data=synthetic_df[[col_a, col_b]],
                )
            elif type_a == "numerical" and type_b == "numerical":
                score = CorrelationSimilarity.compute(
                    real_data=real_df[[col_a, col_b]],
                    synthetic_data=synthetic_df[[col_a, col_b]],
                )
            else:
                continue  # mixed categorical/numerical pair -- skipped
            scores.append(score)
        except Exception as e:
            print(f"  [warning] could not score pair ({col_a}, {col_b}): {e}")

    return round(sum(scores) / len(scores), 4) if scores else float("nan")


def evaluate_model(real_df, synthetic_df, metadata_dict, model_name):
    """Run SDMetrics QualityReport for Column Shapes, and compute
    Column Pair Trends manually (see note above). Return key scores."""
    report = QualityReport()
    report.generate(real_df, synthetic_df, metadata_dict, verbose=False)

    properties_df = report.get_properties()
    scores = dict(zip(properties_df["Property"], properties_df["Score"]))
    column_shapes_score = round(scores.get("Column Shapes", float("nan")), 4)

    column_pair_trends_score = compute_column_pair_trends(real_df, synthetic_df, metadata_dict)

    # Overall score = average of the two properties (matches how
    # SDMetrics itself defines the overall QualityReport score)
    valid_scores = [s for s in [column_shapes_score, column_pair_trends_score] if s == s]
    overall_score = round(sum(valid_scores) / len(valid_scores), 4) if valid_scores else float("nan")

    return {
        "model": model_name,
        "overall_quality_score": overall_score,
        "column_shapes_score": column_shapes_score,
        "column_pair_trends_score": column_pair_trends_score,
    }


if __name__ == "__main__":
    real_df = pd.read_csv(SEED_PATH)
    ctgan_df = pd.read_csv(CTGAN_PATH)
    gaussian_df = pd.read_csv(GAUSSIAN_PATH)

    metadata = Metadata.load_from_json(METADATA_PATH)
    # SDMetrics expects the metadata as a plain dict for a single table.
    # Grab whichever table name is present (SDV may use a placeholder
    # name like "table" if the metadata was saved from an older format).
    metadata_full = metadata.to_dict()
    if "tables" in metadata_full:
        first_table_name = next(iter(metadata_full["tables"]))
        metadata_dict = metadata_full["tables"][first_table_name]
    else:
        metadata_dict = metadata_full

    results = []
    for name, synth_df in [("CTGAN", ctgan_df), ("Gaussian Copula", gaussian_df)]:
        print(f"\nEvaluating {name}...")
        result = evaluate_model(real_df, synth_df, metadata_dict, name)
        results.append(result)
        print(result)

    winner = max(results, key=lambda r: r["overall_quality_score"])

    with open("data/reports/sdmetrics_report.json", "w") as f:
        json.dump({"results": results, "selected_model": winner["model"]}, f, indent=2)

    with open("data/reports/sdmetrics_summary.md", "w") as f:
        f.write("# SDMetrics Evaluation Summary\n\n")
        f.write("| Model | Overall Quality Score | Column Shapes | Column Pair Trends |\n")
        f.write("|---|---|---|---|\n")
        for r in results:
            f.write(
                f"| {r['model']} | {r['overall_quality_score']} | "
                f"{r['column_shapes_score']} | {r['column_pair_trends_score']} |\n"
            )
        f.write(f"\n**Selected model:** {winner['model']} "
                 f"(overall quality score: {winner['overall_quality_score']})\n\n")

        loser = [r for r in results if r["model"] != winner["model"]][0]
        f.write(
            f"**Justification sentence (paste into paper):**\n\n"
            f"> The {winner['model']} model achieved an overall SDMetrics quality "
            f"score of {winner['overall_quality_score']} (column shapes: "
            f"{winner['column_shapes_score']}, column pair trends: "
            f"{winner['column_pair_trends_score']}) compared to {loser['model']}'s "
            f"{loser['overall_quality_score']}, and was therefore selected as the "
            f"final synthesiser.\n"
        )

    print(f"\n{'='*60}")
    print(f"WINNER: {winner['model']} (score: {winner['overall_quality_score']})")
    print(f"{'='*60}")
    print("\nSaved:")
    print("  data/reports/sdmetrics_report.json")
    print("  data/reports/sdmetrics_summary.md  <- paste this into your paper")
