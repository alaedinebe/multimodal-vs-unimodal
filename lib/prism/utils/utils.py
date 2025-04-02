"""Common utility functions for the PRISMA analysis."""

from datetime import datetime
from pathlib import Path
from typing import Any

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


def get_timestamp() -> str:
    """Generate a timestamp string for file naming.

    Returns:
        A timestamp string in the format YYYYMMDD_HHMMSS.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_figure(fig: Any, output_dir: Path, base_filename: str) -> None:
    """Save a matplotlib figure in both SVG and PNG formats.

    Args:
        fig: Matplotlib figure object
        output_dir: Directory to save the figures
        base_filename: Base name for the output files
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = get_timestamp()
    full_filename = output_dir / f"{base_filename}_{timestamp}"

    fig.savefig(f"{full_filename}.svg", format="svg", bbox_inches="tight")
    fig.savefig(f"{full_filename}.png", format="png", bbox_inches="tight")
    print(f"Figure saved in png and svg: {full_filename}")
