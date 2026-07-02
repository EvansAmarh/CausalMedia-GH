"""
figure2_flowchart.py
----------------------
Generates Figure 2: the hybrid data fusion pipeline flowchart, showing
how EdNet KT1 system-log records combine with the synthetic Ghanaian
context layer via student_id.

This is a process diagram, not a data plot, so it's built with simple
matplotlib shapes rather than a plotting library. If you prefer, you
can redraw this in draw.io or Mermaid instead -- the box/arrow content
here is the authoritative spec either way.

Run:
    python src/figure2_flowchart.py
Output:
    figures/figure2_fusion_flowchart.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["savefig.dpi"] = 300

boxes = [
    # (x, y, width, height, text)
    (0.5, 9.0, 6, 1.0, "EdNet KT1 System-Log Records\n(Role 1 output)"),
    (0.5, 7.3, 6, 1.0, "Seed Dataset Construction\n(Ghana contextual variables)"),
    (0.5, 5.6, 2.8, 1.0, "CTGAN Training"),
    (3.7, 5.6, 2.8, 1.0, "Gaussian Copula\nTraining"),
    (0.5, 3.9, 6, 1.0, "SDMetrics / KS Evaluation\n(model selection)"),
    (0.5, 2.2, 6, 1.0, "Final Synthetic Context Dataset"),
    (0.5, 0.3, 6, 1.0, "Merge with Role 1 Data\non student_id"),
]

arrows = [
    (3.5, 9.0, 3.5, 8.3),   # EdNet -> Seed
    (3.5, 7.3, 1.9, 6.6),   # Seed -> CTGAN
    (3.5, 7.3, 5.1, 6.6),   # Seed -> Gaussian
    (1.9, 5.6, 3.0, 4.9),   # CTGAN -> Evaluation
    (5.1, 5.6, 4.0, 4.9),   # Gaussian -> Evaluation
    (3.5, 3.9, 3.5, 3.2),   # Evaluation -> Final dataset
    (3.5, 2.2, 3.5, 1.3),   # Final dataset -> Merge
]

fig, ax = plt.subplots(figsize=(8, 11))

for x, y, w, h, text in boxes:
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.05,rounding_size=0.08",
        linewidth=1.5, edgecolor="#2E75B6", facecolor="#D5E8F0"
    )
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=10, wrap=True)

for x1, y1, x2, y2 in arrows:
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=15,
        linewidth=1.3, color="#333333"
    )
    ax.add_patch(arrow)

ax.set_xlim(0, 7)
ax.set_ylim(0, 10.2)
ax.axis("off")
ax.set_title(
    "Figure 2: Hybrid Data Fusion Pipeline\n"
    "EdNet KT1 system-log records and synthetic Ghanaian SHS contextual\n"
    "variables integrated via early fusion on student_id",
    fontsize=11
)

plt.tight_layout()
plt.savefig("figures/figure2_fusion_flowchart.png")
plt.close()

print("Saved: figures/figure2_fusion_flowchart.png")
