# Systematic Review on Multimodal vs Unimodal AI in Clinical Decision-Making

This repository contains all the code and scripts used in the systematic review on the added value of multimodal approaches in healthcare machine learning. It includes data processing scripts, visualization tools, and analytical frameworks employed in the study.

---

## **Repository Structure**

- 📂 `data/` - Contains the source data files
  - 📈 `table1.csv` - The main dataset for analysis
- 📂 `figures/` - Contains all generated figures
  - 📂 `figure1/` - PRISMA flowchart outputs
  - 📂 `figure3/` - Performance comparison plot outputs
  - 📂 `figure4/` - Sample size violin plot outputs
- 📂 `lib/` - Core library code
  - 📂 `prism/` - PRISMA analysis library
    - 📂 `preprocessing` - Folder for data preprocessing functions
    - 📂 `utils` - Folder for utility functions
    - 📂 `visualization` - Folder for plotting functions
    - 📜 `prismadiagram.py` - PRISMA diagram generation
    - 📜 `boxplot.py` - Box plot generation
    - 📜 `scatterplot_perf_comparison.py` - Performance plot generation
- 📂 `scripts/` - Execution scripts folder
  - 📜 `generate_prisma.py` - Generate PRISMA diagram
  - 📜 `generate_performance_plot.py` - Generate performance comparison plot
  - 📜 `generate_sample_size_plot.py` - Generate sample size violin plot

---

## **Prerequisites**

- Python 3.11.6 or higher
- Poetry (Python package manager)

## **Installation & Setup**

1. Clone this repository:
```bash
git clone https://gitlab.ops.zoi.com/zoihq/data/data_explorations/sysreview-multimodality-draft.git
cd sysreview-multimodality-draft
```

2. Install dependencies using Poetry:
```bash
make install
```

Ensure that the dataset (`table1.csv`) is in the root directory before running scripts.

## **Development Commands**

- `make install` - Install project dependencies
- `make format` - Format code using black and isort
- `make clean` - Clean up Python cache files and build artifacts

## **Generating Figures**

The repository includes three visualization scripts that generate figures for the systematic review:

1. PRISMA Flowchart (`figure1/`)
2. Performance Comparison Scatter Plot (`figure3/`)
3. Dataset Sample Size Violin Plot (`figure4/`)

To generate all figures at once, use:
```bash
make figures
```

This will:
- Generate the PRISMA flowchart in `figure1/figures/`
- Generate the scatter plot in `figure3/saved_fig/`
- Generate the violin plot in `figure4/saved_fig/`

Each figure will be saved in both PNG and SVG formats with a timestamp in the filename.

---

## **Contributing**

Contributions and suggestions are welcome. If you would like to improve this repository, please open an issue or submit a pull request.

Before submitting changes, please ensure your code is properly formatted:
```bash
make format
```

---

## **Authors & Acknowledgments**

Developed by:  
👨‍⚕️ **Alaedine Benani, MD, PhD candidate** (Zoī, AP-HP, Sorbonne University)  
📚 **Pierre Bauvin, Emmanuel Messas, Xavier Tannier, Sylvain Bodard** (Zoī, AP-HP, Sorbonne University, Harvard)  

We acknowledge the support of our collaborators and reviewers.

---

## **License**
This project is licensed under the [MIT License](LICENSE).

---

## **Project Status**
This repository is actively maintained and updated as part of the systematic review submission process.