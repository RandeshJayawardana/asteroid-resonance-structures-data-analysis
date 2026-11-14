import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import csv

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_PATH = SCRIPT_DIR / "NASA JPL SBDB - All Inner Solar System Asteroids.csv"
OUTPUT_PATH = SCRIPT_DIR / "Semi_Major_Axis_vs_Perihelion_Distance.png"

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
    ypoints = np.array([float(row[17]) for row in data_list[1:]], dtype=float)
    print(f"Plotting {len(xpoints)} Small Body Objects between 0.5 and 5.5 AU.")

    fig, ax = plt.subplots(figsize=(15.36, 7.54))

    print("Adding annotations for Mean Motion Resonances and Planetary Orbits.")

    x_axis_Annotations = [
        (2.07, 5.1, 0.5, "4:1 MMR"),
        (2.10, 5.5, 0.5, "Saturn ν6 Resonance"),
        (2.50, 5.1, 0.5, "3:1 MMR"),
        (2.83, 5.1, 0.5, "5:2 MMR"),
        (2.96, 4.8, 0.5, "7:3 MMR"),
        (3.28, 5.1, 0.5, "2:1 MMR"),
        (3.97, 5.1, 0.5, "3:2 MMR"),
        (5.20, 5.3, 0.5, "1:1 MMR"),
    ]

    for x, y_height, line_width, main_text in x_axis_Annotations:
        ax.vlines(x=x, ymin=0, ymax=y_height, color="black", linestyle="--", linewidth=line_width)
        ax.text(x=x, y=y_height + 0.01, s=main_text, fontsize=8, color="black", ha="center", va="bottom")

    y_axis_Annotations = [
        (0.9833, 0.5, "Earth Perihelion"),
        (1.3814, 0.5, "Mars Perihelion"),
        (4.9506, 0.5, "Jupiter Perihelion")
    ]

    for y, line_width, main_text in y_axis_Annotations:
        ax.hlines(y=y, xmin=0, xmax=6, color="black", linestyle="-", linewidth=line_width)
        ax.text(x=0.5, y=y + 0.01, s=main_text, fontsize=10, color="black", ha="center", va="bottom")

    plt.ylim(0.0, 6.0)
    plt.xlim(0.0, 6.0)

    print("Adding axis labels, title, and grid.")

    plt.scatter(xpoints, ypoints, s=0.01, color='mediumslateblue')
    plt.suptitle("Asteroid Orbital Elements Distribution", fontsize=20)
    ax.set_title("Semi-Major Axis vs. Perihelion Distance", fontsize=15)
    ax.set_xlabel("Semi-Major Axis (AU)")
    ax.set_ylabel("Perihelion Distance (AU)")

    plt.savefig(OUTPUT_PATH, dpi=1200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"Plot saved successfully to {OUTPUT_PATH}")

    plt.show()

if __name__ == "__main__":
    plot_scatter(DATA_PATH)