#!/usr/bin/env python3
"""Script to generate the performance comparison plot."""

from pathlib import Path

import matplotlib.pyplot as plt

from lib.prism.preprocessing.preprocessing import preprocess_performance_data
from lib.prism.utils.utils import load_csv_file, save_figure
from lib.prism.visualization.visualization import create_performance_plot


def main():
    """Generate and save the performance comparison plot."""
    # Setup paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    output_dir = script_dir.parent / "figures" / "figure3" / "saved_fig"

    # Required columns for the analysis
    required_columns = [
        "unimodal_best_score",
        "multimodal_best_score",
        "evaluation_metric",
        "modalities",
    ]

    try:
        # Load and process data
        df = load_csv_file(data_dir)
        scores, modalities = preprocess_performance_data(
            df, required_columns[:2], required_columns[2], required_columns[3]
        )

        # Create and save the plot
        fig = create_performance_plot(scores.iloc[:, 0], scores.iloc[:, 1], modalities)
        save_figure(fig, output_dir, "performance_plot")
        plt.close(fig)

    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
