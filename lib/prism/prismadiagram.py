from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def create_box(ax, text, x, y, width=4, height=1.8, fontsize=10):
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
    box = FancyBboxPatch(
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


def create_prisma_diagram():
    """Create and save the PRISMA flowchart."""
    # Initialize the plot
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
        "Articles excluded\nthrough title and abstract\nn = 216\n\nreasons :\n• no comparison of unimodality\nversus multimodality (n= 189)\n• wrong population (n=46)\n• not a clinical-making\ndecision task (n=37)\n• wrong publication type (n=27)",
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
        "Full text articles excluded\nn = 37\n\nreasons :\n• no comparison of unimodality\nversus multimodality (n = 28)\n• wrong population (n = 2)\n• not a clinical-making\ndecision task (n = 2)\n• wrong publication type (n = 4)\n• duplicate (n = 1)",
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


def save_figure(fig, output_dir: Path):
    """Save the figure in both SVG and PNG formats.

    Args:
        fig: Matplotlib figure object
        output_dir: Directory to save the figures
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir.mkdir(parents=True, exist_ok=True)

    base_filename = output_dir / f"prisma_flowchart_{timestamp}"
    fig.savefig(f"{base_filename}.svg", format="svg", bbox_inches="tight")
    fig.savefig(f"{base_filename}.png", format="png", bbox_inches="tight")
    print(f"Flowchart saved in png and svg: {base_filename}")


def main():
    """Main function to generate and save the PRISMA diagram."""
    # Create output directory relative to the script location
    output_dir = Path(__file__).parent / "figures"

    # Create and save the diagram
    fig = create_prisma_diagram()
    save_figure(fig, output_dir)
    plt.close(fig)


if __name__ == "__main__":
    main()
