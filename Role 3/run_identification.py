from pathlib import Path
import sys

import pandas as pd
from dowhy import CausalModel

sys.stdout.reconfigure(encoding="utf-8")


ROLE3_DIR = Path(__file__).resolve().parent
REPO_ROOT = ROLE3_DIR.parent

CONFOUNDERS = [
    "prior_achievement",
    "content_modality_preference",
    "bandwidth_category",
    "consistency",
    "early_struggle",
    "skill_coverage",
    "session_duration_avg",
    "peer_activity_index",
    "school_resource_level",
    "tablet_access",
    "location_encoded",
]


def build_gml_string(edges):
    nodes = sorted({node for edge in edges for node in edge})
    node_ids = {name: index for index, name in enumerate(nodes)}
    lines = ["graph [", "  directed 1"]
    lines.extend(
        f'  node [ id {node_ids[name]} label "{name}" ]' for name in nodes
    )
    lines.extend(
        f"  edge [ source {node_ids[source]} target {node_ids[target]} ]"
        for source, target in edges
    )
    lines.append("]")
    return "\n".join(lines)


def load_analysis_data():
    student = pd.read_csv(REPO_ROOT / "Role 1" / "student_level_dataset.csv")
    school = pd.read_csv(
        REPO_ROOT / "Role 2" / "data" / "synthetic" / "synthetic_school_data.csv"
    )
    school = school.sample(n=len(student), random_state=42).reset_index(drop=True)

    data = student.reset_index(drop=True).copy()
    data["multimedia_ratio"] = data.pop("multimedia_engagement")
    data["content_modality_preference"] = data["peer_collaboration"]
    data["peer_activity_index"] = data["total_interactions"]
    data["location_encoded"] = school["location"].map(
        {"Rural": 1, "Peri-urban": 2, "Urban": 3}
    )
    for column in [
        "tablet_access",
        "bandwidth_category",
        "school_resource_level",
        "teacher_qual",
    ]:
        data[column] = school[column]

    return data.drop(
        columns=["student_id", "total_interactions", "peer_collaboration"]
    )


def main():
    edges = []
    for confounder in CONFOUNDERS:
        edges.append((confounder, "multimedia_ratio"))
        edges.append((confounder, "performance_gain"))
    edges.extend(
        [
            ("teacher_qual", "performance_gain"),
            ("multimedia_ratio", "performance_gain"),
        ]
    )

    data = load_analysis_data()
    model = CausalModel(
        data=data,
        treatment="multimedia_ratio",
        outcome="performance_gain",
        graph=build_gml_string(edges),
        proceed_when_unidentifiable=True,
    )
    identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
    output_path = ROLE3_DIR / "identified_estimand.txt"
    output_path.write_text(str(identified_estimand), encoding="utf-8")
    print(f"Loaded {len(data):,} aligned rows from both project datasets.")
    print(identified_estimand)
    print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
