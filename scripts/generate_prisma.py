#!/usr/bin/env python3
"""Script to generate the PRISMA diagram."""

from pathlib import Path

import matplotlib.pyplot as plt

from lib.prism.utils.utils import save_figure
from lib.prism.visualization.visualization import create_prisma_diagram


def main():
    """Generate and save the PRISMA diagram."""
    # Setup paths
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent / "figures" / "figure1" / "figures"

    # Create and save the diagram
    fig = create_prisma_diagram()
    save_figure(fig, output_dir, "prisma_flowchart")
    plt.close(fig)


if __name__ == "__main__":
    main()
