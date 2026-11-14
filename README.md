# asteroid-resonance-structures-data-analysis

Python data processing and visualisation scripts for the paper titled *"On the Nature of Resonance Structures and Orbital Dynamics in the Asteroid Belt"*.

---

## Overview

This repository contains the Python data processing and visualisation scripts used to generate the figures and statistical distributions presented in the research paper. The codebase processes asteroid orbital parameters to evaluate resonance structures, Jovian Lagrange points, and dynamical boundaries within the main asteroid belt.

---

## Repository Structure

```text
├── data/
│   └── (Required dataset files hosted externally: https://doi.org/10.5281/zenodo.24212198)
├── scripts/
│   └── generate_graphs.py
├── requirements.txt
└── README.md
```

---

## Prerequisites & Dataset Setup

To successfully run these scripts, complete the following setup steps:

### 1. Python Environment & Dependencies
The scripts were developed and tested using Python 3.x. Install the required libraries by running:

```bash
pip install -r requirements.txt
```

*(Core dependencies include `numpy`, `matplotlib`, `pathlib`, `csv`, `scipy`, and `pandas`).*

### 2. Dataset Location
Because the large dataset files (`~256 MB` and `~268 MB`) exceed GitHub's file size limits, they are hosted externally on Zenodo.

1. Download both dataset files from the permanent archive: [https://doi.org/10.5281/zenodo.24212198](https://doi.org/10.5281/zenodo.24212198).
2. Place the downloaded files inside the local `data/` directory of this repository before executing the scripts.

---

## How to Run

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/RandeshJayawardana/asteroid-resonance-structures-data-analysis.git
   cd asteroid-resonance-structures-data-analysis
   ```

2. Ensure your datasets are correctly placed in the `data/` folder as outlined above.

3. Execute the visualization script:
   ```bash
   python scripts/generate_graphs.py
   ```
   Generated figures will be output automatically.

---

## Data Provenance

* **Source Database:** NASA Jet Propulsion Laboratory (JPL) Small-Body Database ([https://ssd.jpl.nasa.gov/](https://ssd.jpl.nasa.gov/)), queried on October 6, 2026.
* **Archived Data:** The processed subsets used in this study are permanently citable via the Zenodo DOI linked above.

---

## Citation

If you use these scripts or datasets in your research, please cite our paper:

```bibtex
@article{jayawardana2026asteroid,
  title={On the Nature of Resonance Structures and Orbital Dynamics in the Asteroid Belt},
  author={Jayawardana, Randesh},
  year={2026}
}
```
