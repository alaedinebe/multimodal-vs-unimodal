#!/usr/bin/env python3
"""Script to generate the sample size violin plot."""

from pathlib import Path

import matplotlib.pyplot as plt

from lib.prism.preprocessing.preprocessing import preprocess_sample_size_data
from lib.prism.utils.utils import load_csv_file, save_figure
from lib.prism.visualization.visualization import create_sample_size_plot


def main():
    """Generate and save the sample size violin plot."""
    # Setup paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    output_dir = script_dir.parent / "figures" / "figure4" / "saved_fig"

    try:
        # Load and process data
        df = load_csv_file(data_dir)
        data = preprocess_sample_size_data(df)

        # Create and save the plot
        fig = create_sample_size_plot(data)
        save_figure(fig, output_dir, "violinplot_samplesize")
        plt.close(fig)

    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
