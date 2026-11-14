import csv
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_PATH = SCRIPT_DIR / "NASA JPL SBDB - Asteroid Belt and Jovian Trojans Only.csv"
OUTPUT_PATH = SCRIPT_DIR / "Asteroid_Distribution_Histogram.png"

def plot_histogram(data):

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(data, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            data_list = list(reader)
            print(f"Data read from {data}: {len(data_list)} rows")    
    except FileNotFoundError:
        print(f"Error: Could not find file at {data}")
        return

    xpoints = np.array([float(row[16]) for row in data_list[1:]], dtype=float)
    print(f"Plotting {len(xpoints)} Small Body Objects between 1.8 and 5.5 AU.")

    fig, ax = plt.subplots(figsize=(15.36, 7.54))

    print("Adding annotations for Mean Motion Resonances.")

    Annotations = [
        (1.78, 2500, "5:1 MMR"),
        (2.07, 2500, "4:1 MMR"),
        (2.50, 2500, "3:1 MMR"),
        (2.83, 2500, "5:2 MMR"),
        (2.96, 2400, "7:3 MMR"),
        (3.28, 2500, "2:1 MMR"),
        (3.97, 2500, "3:2 MMR"),
        (4.29, 2500, "4:3 MMR"),
        (5.20, 2500, "1:1 MMR")
    ]

    for x, y_height, main_text in Annotations:
        ax.vlines(x=x, ymin=0, ymax=y_height, color="black", linestyle="--", linewidth=0.5)
        ax.text(x=x, y=y_height + 4, s=main_text, fontsize=10, color="black", ha="center", va="bottom")

    print("Adding axis labels, title, and grid.")

    ax.hist(xpoints, bins=55000, edgecolor='royalblue')
    plt.suptitle("Asteroid Distribution Histogram", fontsize=20)
    ax.set_title("Kirkwood Gaps and Jovian Lagrange Points", fontsize=15)
    ax.set_xlabel("Semi-Major Axis (AU)")
    ax.set_ylabel("Number of Asteroids per 0.0001 AU bin")
    ax.grid(axis='y', alpha=0.75)

    plt.savefig(OUTPUT_PATH, dpi=600, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"Plot saved successfully to {OUTPUT_PATH}")

    plt.show()

if __name__ == "__main__":
    plot_histogram(DATA_PATH)



