import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import csv

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_PATH = SCRIPT_DIR / "NASA JPL SBDB - All Inner Solar System Asteroids.csv"
OUTPUT_PATH = SCRIPT_DIR / "Semi_Major_Axis_vs_Eccentricity.png"

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
    ypoints = np.array([float(row[15]) for row in data_list[1:]], dtype=float)
    print(f"Plotting {len(xpoints)} Small Body Objects between 0.5 and 5.5 AU.")

    fig, ax = plt.subplots(figsize=(15.36, 7.54))

    print("Adding annotations for Mean Motion Resonances and Planetary Orbits.")

    Annotations = [
        (1.00, 1.0, "Earth Orbit"),
        (1.52, 1.0, "Mars Orbit"),
        (1.78, 0.9, "5:1 MMR"),
        (2.07, 0.9, "4:1 MMR"),
        (2.50, 0.9, "3:1 MMR"),
        (2.83, 0.9, "5:2 MMR"),
        (2.96, 0.875, "7:3 MMR"),
        (3.28, 0.9, "2:1 MMR"),
        (3.97, 0.9, "3:2 MMR"),
        (4.29, 0.72, "4:3 MMR"),
        (5.20, 0.72, "1:1 MMR"),
        (5.20, 1.0, "Jupiter Orbit")
    ]

    for x, y_height, main_text in Annotations:
        ax.vlines(x=x, ymin=0, ymax=y_height, color="black", linestyle="--", linewidth=0.5)
        ax.text(x=x, y=y_height + 0.01, s=main_text, fontsize=10, color="black", ha="center", va="bottom")

    print("Adding crosser limit lines for Earth, Mars, and Jupiter.")

    a_line = np.linspace(0, 5.5, 500)
    e_earth = 1.0 - (1.0 / a_line)
    e_earth1 = (1.0 / a_line) - 1.0
    e_mars = 1.0 - (1.523 / a_line)
    e_mars1 = (1.523 / a_line) - 1.0
    e_jupiter = (5.20 / a_line) - 1.0
    e_jupiter1 = 1.0 - (5.20 / a_line)

    plt.plot(a_line, e_earth, color='green', linestyle='-', linewidth=1.5, label='Earth Crosser Limit ($q = 1.00\\text{ AU}$)',)
    plt.plot(a_line, e_earth1, color='green', linestyle='-', linewidth=1.5)
    plt.plot(a_line, e_mars, color='crimson', linestyle='--', linewidth=1.5, label='Mars Crosser Limit ($q = 1.52\\text{ AU}$)',)
    plt.plot(a_line, e_mars1, color='crimson', linestyle='--', linewidth=1.5)
    plt.plot(a_line, e_jupiter, color='royalblue', linestyle='-.', linewidth=1.5, label='Jupiter Crosser Limit ($Q = 5.20\\text{ AU}$)',)
    plt.plot(a_line, e_jupiter1, color='royalblue', linestyle='-.', linewidth=1.5)

    plt.ylim(0.0, 1.0)
    plt.xlim(0.5, 5.5)
    plt.legend(loc='upper right')

    print("Adding axis labels, title, and grid.")

    plt.scatter(xpoints, ypoints, s=0.05, color='orange')
    plt.suptitle("Asteroid Orbital Elements Distribution", fontsize=20)
    ax.set_title("Semi-Major Axis vs. Orbital Eccentricity", fontsize=15)
    ax.set_xlabel("Semi-Major Axis (AU)")
    ax.set_ylabel("Orbital Eccentricity (e)")
    ax.grid(axis='y', alpha=0.75)

    plt.savefig(OUTPUT_PATH, dpi=1200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"Plot saved successfully to {OUTPUT_PATH}")

    plt.show()

if __name__ == "__main__":
    plot_scatter(DATA_PATH)