"""Visualization functions for the PRISMA analysis."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def create_box(
    ax: plt.Axes,
    text: str,
    x: float,
    y: float,
    width: float = 4,
    height: float = 1.8,
    fontsize: int = 10,
) -> tuple:
    """Create a box with text in the diagram.

    Args:
        ax: Matplotlib axis object
        text: Text to display in the box
        x, y: Position coordinates
        width, height: Box dimensions
        fontsize: Font size for the text

    Returns:
        Tuple of key positions (center, top-center, bottom-center, right-center, left-center)
    """
    box = plt.matplotlib.patches.FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="square, pad=0",
        edgecolor="black",
        facecolor="white",
    )
    ax.add_patch(box)
    ax.text(
        x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=fontsize
    )

    center = (x + width / 2, y + height / 2)
    top_center = (x + width / 2, y + height)
    bottom_center = (x + width / 2, y)
    right_center = (x + width, y + height / 2)
    left_center = (x, y + height / 2)
    return center, top_center, bottom_center, right_center, left_center


def create_prisma_diagram() -> plt.Figure:
    """Create the PRISMA flowchart.

    Returns:
        Matplotlib figure object containing the PRISMA diagram.
    """
    fig, ax = plt.subplots(figsize=(12, 16))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 16)
    ax.axis("off")

    # Create the boxes
    box_positions = {}

    # Identification
    box_positions["identification"] = create_box(
        ax, "Records identified\nthrough database search\nn = 352", 2, 12
    )
    box_positions["duplicates_removed"] = create_box(
        ax, "Duplicates excluded = 2", 8, 12
    )

    # Eligibility
    box_positions["eligibility_title_abstract"] = create_box(
        ax, "Records screened\nthrough title and abstract\nn = 350", 2, 9.3
    )
    box_positions["excluded_title_abstract"] = create_box(
        ax,
        "Articles excluded\nthrough title and abstract\nn = 216\n\nreasons :\n"
        "• no comparison of unimodality\nversus multimodality (n= 189)\n"
        "• wrong population (n=46)\n• not a clinical-making\ndecision task (n=37)\n"
        "• wrong publication type (n=27)",
        x=8,
        y=6.1,
        width=6,
        height=5,
    )
    box_positions["eligibility_full_text"] = create_box(
        ax, "Full-text articles\nassessed for eligibility\n(n = 134)", x=2, y=4.2
    )
    box_positions["excluded_full_text"] = create_box(
        ax,
        "Full text articles excluded\nn = 37\n\nreasons :\n"
        "• no comparison of unimodality\nversus multimodality (n = 28)\n"
        "• wrong population (n = 2)\n• not a clinical-making\ndecision task (n = 2)\n"
        "• wrong publication type (n = 4)\n• duplicate (n = 1)",
        x=8,
        y=1,
        width=6,
        height=5,
    )

    # Included
    box_positions["included"] = create_box(
        ax, "Studies included\nin review\nn = 97", 2, 1
    )

    # Add arrows
    arrow_properties = dict(arrowstyle="->", color="black", lw=2)

    # Vertical arrows
    ax.annotate(
        "",
        xy=box_positions["identification"][2],
        xytext=box_positions["identification"][2],
        arrowprops=arrow_properties,
    )
    ax.annotate(
        "",
        xy=box_positions["eligibility_title_abstract"][1],
        xytext=box_positions["identification"][2],
        arrowprops=arrow_properties,
    )
    ax.annotate(
        "",
        xy=box_positions["eligibility_full_text"][1],
        xytext=box_positions["eligibility_title_abstract"][2],
        arrowprops=arrow_properties,
    )
    ax.annotate(
        "",
        xy=box_positions["included"][1],
        xytext=box_positions["eligibility_full_text"][2],
        arrowprops=arrow_properties,
    )

    # Horizontal arrows
    ax.annotate(
        "",
        xy=box_positions["duplicates_removed"][4],
        xytext=box_positions["identification"][3],
        arrowprops=arrow_properties,
    )
    ax.annotate("", xy=(8, 10), xytext=(6, 10), arrowprops=arrow_properties)
    ax.annotate("", xy=(8, 5), xytext=(6, 5), arrowprops=arrow_properties)

    # Add phase labels
    ax.text(
        0.5,
        8,
        "Identification and screening",
        fontsize=12,
        fontweight="bold",
        ha="center",
        rotation=90,
    )
    ax.text(
        0.5,
        4.5,
        "Eligibility",
        fontsize=12,
        fontweight="bold",
        ha="center",
        rotation=90,
    )
    ax.text(
        0.5, 1.5, "Included", fontsize=12, fontweight="bold", ha="center", rotation=90
    )

    return fig


def create_performance_plot(
    unimodality_scores: pd.Series,
    multimodality_scores: pd.Series,
    modalities: pd.Series,
) -> plt.Figure:
    """Create scatter plot comparing unimodal and multimodal performance.

    Args:
        unimodality_scores: Series of unimodal AUC scores
        multimodality_scores: Series of multimodal AUC scores
        modalities: Series of modality types

    Returns:
        Matplotlib figure object containing the performance plot
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
    fig, ax = plt.subplots(figsize=(22, 8))
    ax.scatter(
        unimodality_scores,
        multimodality_scores,
        c=modality_colors,
        alpha=0.9,
        edgecolors="k",
        linewidth=0.5,
    )

    # Reference lines
    ax.plot(
        [0.5, 1],
        [0.5, 1],
        color="red",
        linestyle="--",
        label="y = x (Equal Performance)",
    )
    ax.plot(
        [0.5, 1],
        [0.5 + median_difference, 1 + median_difference],
        color="blue",
        linestyle="-.",
        label=f"Median Threshold (Δ={median_difference:.2f})",
    )

    # Labels & title
    ax.set_title(
        "Unimodality vs. Multimodality AUC Performance", fontsize=18, fontweight="bold"
    )
    ax.set_xlabel("Unimodality AUC", fontsize=14)
    ax.set_ylabel("Multimodality AUC", fontsize=14)
    ax.set_xlim(0.5, 1)
    ax.set_ylim(0.5, 1)
    ax.grid(alpha=0.5)

    # Add quadrant labels
    ax.text(
        0.55,
        0.9,
        "Favors Multimodality",
        fontsize=12,
        color="blue",
        weight="bold",
        bbox=dict(facecolor="white", edgecolor="green", boxstyle="round,pad=0.5"),
    )
    ax.text(
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
    ax.legend(
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

    return fig


def create_sample_size_plot(data: pd.Series) -> plt.Figure:
    """Create violin plot of dataset sample sizes.

    Args:
        data: Series containing sample size data

    Returns:
        Matplotlib figure object containing the violin plot
    """
    # Compute key statistics
    stats = {
        "Minimum": np.min(data),
        "First Quartile": np.percentile(data, 25),
        "Median": np.median(data),
        "Third Quartile": np.percentile(data, 75),
        "Maximum": np.max(data),
    }

    # Create the figure
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
