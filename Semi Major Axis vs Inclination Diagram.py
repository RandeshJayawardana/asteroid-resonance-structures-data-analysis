import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import csv

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_PATH = SCRIPT_DIR / "NASA JPL SBDB - Asteroid Belt and Jovian Trojans Only.csv"
OUTPUT_PATH = SCRIPT_DIR / "Semi_Major_Axis_vs_Inclination.png"

def plot_scatter(data):

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
    ypoints = np.array([float(row[18]) for row in data_list[1:]], dtype=float)
    print(f"Plotting {len(xpoints)} Small Body Objects between 1.8 and 5.5 AU.")

    fig, ax = plt.subplots(figsize=(15.36, 7.54))

    print("Adding annotations for Mean Motion Resonances and Jovian Orbital Plane.")

    Annotations = [
        (1.78, 55, "5:1 MMR"),
        (2.07, 55, "4:1 MMR"),
        (2.50, 55, "3:1 MMR"),
        (2.83, 55, "5:2 MMR"),
        (2.96, 52, "7:3 MMR"),
        (3.28, 55, "2:1 MMR"),
        (3.97, 55, "3:2 MMR"),
        (4.29, 55, "4:3 MMR"),
        (5.20, 55, "1:1 MMR"),
        (5.20, 60, "Jupiter Orbital Plane")
    ]

    for x, y_height, main_text in Annotations:
        ax.vlines(x=x, ymin=0, ymax=y_height, color="black", linestyle="--", linewidth=0.5)
        ax.text(x=x, y=y_height + 0.5, s=main_text, fontsize=10, color="black", ha="center", va="bottom")

    print("Adding axis labels, title, and grid.")

    plt.ylim(0.0, 60)
    plt.xlim(1.7, 5.5)
    plt.scatter(xpoints, ypoints, s=0.01, color='green')
    plt.suptitle("Asteroid Orbital Elements Distribution", fontsize=20)
    ax.set_title("Semi-Major Axis vs. Inclination", fontsize=15)
    ax.set_xlabel("Semi-Major Axis (AU)")
    ax.set_ylabel("Inclination (deg)")
    ax.grid(axis='y', alpha=0.75)

    plt.savefig(OUTPUT_PATH, dpi=1200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"Plot saved successfully to {OUTPUT_PATH}")

    plt.show()

if __name__ == "__main__":
    plot_scatter(DATA_PATH)