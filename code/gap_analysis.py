from __future__ import annotations

import os
from statistics import mean, median
import matplotlib.pyplot as plt

from merit_model import calculate_merit
from survey_parsing import parse_scenarios


def percentile(sorted_values: list[float], p: float) -> float:
    """Return the pth percentile (0-100) using linear interpolation."""
    if not sorted_values:
        raise ValueError("No values to compute percentiles.")
    if p <= 0:
        return sorted_values[0]
    if p >= 100:
        return sorted_values[-1]
    k = (len(sorted_values) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(sorted_values) - 1)
    if f == c:
        return sorted_values[f]
    d = k - f
    return sorted_values[f] * (1 - d) + sorted_values[c] * d


def main() -> None:
    project_root = os.path.dirname(os.path.dirname(__file__))
    survey_path = os.path.join(project_root, "survey", "survey_questions.txt")

    scenarios = parse_scenarios(survey_path)
    gaps: list[float] = []

    for scenario in scenarios:
        merit1 = calculate_merit(scenario.candidate1)
        merit2 = calculate_merit(scenario.candidate2)
        gaps.append(abs(merit1 - merit2))

    gaps.sort()

    print(f"Scenarios: {len(gaps)}")
    print(f"Min gap: {gaps[0]:.4f}")
    print(f"Max gap: {gaps[-1]:.4f}")
    print(f"Mean gap: {mean(gaps):.4f}")
    print(f"Median gap: {median(gaps):.4f}")
    print(f"P25 gap: {percentile(gaps, 25):.4f}")
    print(f"P75 gap: {percentile(gaps, 75):.4f}")
    print(f"P90 gap: {percentile(gaps, 90):.4f}")

    plt.figure(figsize=(10, 6))
    plt.hist(gaps, bins=15, color='skyblue', edgecolor='black')
    plt.title('Distribution of Merit Gaps Across Scenarios')
    plt.xlabel('Merit Gap')
    plt.ylabel('Number of Scenarios')
    plt.grid(axis='y', alpha=0.75)
    plt.show()
    plt.savefig(os.path.join(project_root, "figures", "merit_gap_distribution.png"))



if __name__ == "__main__":
    main()
