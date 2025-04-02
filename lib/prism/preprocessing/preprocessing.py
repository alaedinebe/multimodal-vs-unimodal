"""Data preprocessing functions for the PRISMA analysis."""

from typing import Tuple

import pandas as pd


def preprocess_performance_data(
    df: pd.DataFrame, score_columns: list, evaluation_column: str, modality_column: str
) -> Tuple[pd.DataFrame, pd.Series]:
    """Cleans and filters the DataFrame for performance analysis.

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


def preprocess_sample_size_data(df: pd.DataFrame) -> pd.Series:
    """Extract and clean sample size data.

    Args:
        df: The input DataFrame.

    Returns:
        Series containing cleaned sample size data.
    """
    if "total_data" not in df.columns:
        raise ValueError("Column 'total_data' not found in the CSV file.")

    return df["total_data"].dropna().astype(float)
