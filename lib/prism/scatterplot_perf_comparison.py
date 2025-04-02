from datetime import datetime
from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_csv_file(directory: Path) -> pd.DataFrame:
    """Loads the first CSV file found in the given directory.

    Args:
        directory: Path object representing the directory containing the CSV file.

    Returns:
        A pandas DataFrame containing the data from the CSV.

    Raises:
        FileNotFoundError: If no CSV files are found.
    """
    csv_files = list(directory.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {directory}.")

    return pd.read_csv(csv_files[0])


def validate_dataframe(df: pd.DataFrame, required_columns: list) -> None:
    """Validates that the DataFrame contains the required columns.

    Args:
        df: The DataFrame to check.
        required_columns: A list of required column names.

    Raises:
        KeyError: If required columns are missing.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Missing required columns: {', '.join(missing_columns)}")


def preprocess_data(
    df: pd.DataFrame, score_columns: list, evaluation_column: str, modality_column: str
) -> Tuple[pd.DataFrame, pd.Series]:
    """Cleans and filters the DataFrame for analysis.

    Args:
        df: The input DataFrame.
        score_columns: List of column names that need conversion to float.
        evaluation_column: The column indicating the evaluation metric.
        modality_column: The column containing modality information.

    Returns:
        A tuple (processed scores DataFrame, modalities Series).
    """
    # Drop missing values in key columns
    df = df.dropna(subset=score_columns + [evaluation_column, modality_column])

    # Filter only AUC-based evaluations
    df = df[df[evaluation_column].str.contains("AUC", na=False)]

    # Convert numeric columns and handle inconsistencies
    df[score_columns] = (
        df[score_columns]
        .apply(lambda col: col.astype(str).str.replace(",", "."))
        .astype(float)
    )

    return df[score_columns], df[modality_column]


def plot_performance(
    unimodality_scores: pd.Series,
    multimodality_scores: pd.Series,
    modalities: pd.Series,
    save_dir: Path,
) -> None:
    """Generates and saves a scatter plot comparing unimodal and multimodal AUC scores.

    Args:
        unimodality_scores: A Series of unimodal AUC scores.
        multimodality_scores: A Series of multimodal AUC scores.
        modalities: A Series representing the modality types.
        save_dir: Path object representing the directory where the plot should be saved.
    """
    unique_modalities = modalities.unique()
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_modalities)))
    color_map = dict(zip(unique_modalities, colors))
    modality_colors = modalities.map(color_map)

    # Compute deltas (multimodal - unimodal)
    deltas = multimodality_scores - unimodality_scores
    median_difference = np.median(deltas)

    # Compute statistics
    negative_delta_count = (deltas < 0.01).sum()
    large_improvement_count = (deltas > 0.10).sum()
    total_studies = len(unimodality_scores)

    # Print statistics
    print(f"Total number of studies: {total_studies}")
    print(f"Studies favoring unimodality (Δ < 0.01): {negative_delta_count}")
    print(f"Studies with Δ > 0.10 (favoring multimodality): {large_improvement_count}")

    # Create scatter plot
    plt.figure(figsize=(22, 8))
    plt.scatter(
        unimodality_scores,
        multimodality_scores,
        c=modality_colors,
        alpha=0.9,
        edgecolors="k",
        linewidth=0.5,
    )

    # Reference lines
    plt.plot(
        [0.5, 1],
        [0.5, 1],
        color="red",
        linestyle="--",
        label="y = x (Equal Performance)",
    )
    plt.plot(
        [0.5, 1],
        [0.5 + median_difference, 1 + median_difference],
        color="blue",
        linestyle="-.",
        label=f"Median Threshold (Δ={median_difference:.2f})",
    )

    # Labels & title
    plt.title(
        "Unimodality vs. Multimodality AUC Performance", fontsize=18, fontweight="bold"
    )
    plt.xlabel("Unimodality AUC", fontsize=14)
    plt.ylabel("Multimodality AUC", fontsize=14)
    plt.xlim(0.5, 1)
    plt.ylim(0.5, 1)
    plt.grid(alpha=0.5)

    # Add quadrant labels
    plt.text(
        0.55,
        0.9,
        "Favors Multimodality",
        fontsize=12,
        color="blue",
        weight="bold",
        bbox=dict(facecolor="white", edgecolor="green", boxstyle="round,pad=0.5"),
    )
    plt.text(
        0.6,
        0.55,
        "Favors Unimodality",
        fontsize=12,
        color="blue",
        weight="bold",
        bbox=dict(facecolor="white", edgecolor="orange", boxstyle="round,pad=0.5"),
    )

    # Compute modality counts
    modality_counts = modalities.value_counts()

    # Create legend
    modality_patches = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=color,
            markersize=10,
            label=f"{modality} ({modality_counts[modality]})",
        )
        for modality, color in color_map.items()
    ]

    # Combine legend entries
    plt.legend(
        handles=modality_patches
        + [
            plt.Line2D(
                [], [], color="red", linestyle="--", label="y = x (Equal Performance)"
            ),
            plt.Line2D(
                [],
                [],
                color="blue",
                linestyle="-.",
                label=f"Median Threshold (Δ={median_difference:.2f})",
            ),
        ],
        title="Modalities combinations",
        fontsize=8,
        title_fontsize=10,
        loc="center left",
        bbox_to_anchor=(0.70, 0.30),
    )

    # Save the plot
    save_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.savefig(save_dir / f"performance_plot_{timestamp}.png", dpi=900, format="png")
    plt.savefig(
        save_dir / f"performance_plot_{timestamp}.svg",
        format="svg",
        bbox_inches="tight",
    )

    plt.close()


def main():
    """Main function to load, process, and visualize the CSV data."""
    # Setup paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent
    save_dir = script_dir / "saved_fig"

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
        validate_dataframe(df, required_columns)
        scores, modalities = preprocess_data(
            df, required_columns[:2], required_columns[2], required_columns[3]
        )

        # Create and save the plot
        plot_performance(scores.iloc[:, 0], scores.iloc[:, 1], modalities, save_dir)

    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
