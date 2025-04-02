from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_data(data_path: Path) -> pd.DataFrame:
    """Load and validate the dataset.

    Args:
        data_path: Path to the CSV file

    Returns:
        DataFrame containing the data

    Raises:
        ValueError: If required column is missing
    """
    df = pd.read_csv(data_path)
    if "total_data" not in df.columns:
        raise ValueError("Column 'total_data' not found in the CSV file.")
    return df


def compute_statistics(data: np.ndarray) -> dict:
    """Compute key statistics for the dataset.

    Args:
        data: Array of numeric values

    Returns:
        Dictionary containing minimum, quartiles, median, and maximum
    """
    return {
        "Minimum": np.min(data),
        "First Quartile": np.percentile(data, 25),
        "Median": np.median(data),
        "Third Quartile": np.percentile(data, 75),
        "Maximum": np.max(data),
    }


def create_violin_plot(data: np.ndarray, stats: dict) -> plt.Figure:
    """Create the violin plot with statistics.

    Args:
        data: Array of numeric values
        stats: Dictionary of computed statistics

    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    # Generate violin plot with log scale
    sns.violinplot(data=data, ax=ax, log_scale=True, color="lightblue")

    # Add jittered scatter plot
    sns.stripplot(data=data, ax=ax, jitter=True, size=4, color="black", alpha=0.5)

    # Annotate statistics
    for label, value in stats.items():
        ax.text(
            x=0.30,
            y=value,
            s=f"{label}\n{int(value)}",
            fontsize=10,
            color="black",
            va="center",
            ha="center",
        )

    # Set labels and title
    ax.set_ylabel("Dataset Sample Size", fontsize=12)
    plt.title("Violin Plot of Dataset Sample Sizes", fontsize=14)

    plt.tight_layout()
    return fig


def save_figure(fig: plt.Figure, output_dir: Path):
    """Save the figure in both SVG and PNG formats.

    Args:
        fig: Matplotlib figure object
        output_dir: Directory to save the figures
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir.mkdir(parents=True, exist_ok=True)

    base_filename = output_dir / f"violinplot_samplesize_{timestamp}"
    fig.savefig(f"{base_filename}.svg", format="svg", bbox_inches="tight")
    fig.savefig(f"{base_filename}.png", format="png", bbox_inches="tight")
    print(f"Violin plot saved in png and svg: {base_filename}")


def main():
    """Main function to generate and save the violin plot."""
    # Setup paths
    script_dir = Path(__file__).parent
    data_path = script_dir.parent / "table1.csv"
    output_dir = script_dir / "saved_fig"

    # Load and process data
    df = load_data(data_path)
    data = df["total_data"].dropna().astype(float).values
    stats = compute_statistics(data)

    # Create and save the plot
    fig = create_violin_plot(data, stats)
    save_figure(fig, output_dir)
    plt.close(fig)


if __name__ == "__main__":
    main()
