import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = SCRIPT_DIR / "Effective_Potential_Surface_Plot.png"

def plot_mesh():
    fig = plt.figure(figsize=(14, 6))
    fig.subplots_adjust(top=0.82, wspace=0.3)

    mu = 9.537 * 10**-4     # Jupiter Mass Ratio (mu = m2 / (m1 + m2))

    x = np.linspace(-1.3, 1.3, 1000)
    y = np.linspace(-1.3, 1.3, 1000)
    X, Y = np.meshgrid(x, y)

    r1 = np.sqrt((X + mu) ** 2 + Y**2)
    r2 = np.sqrt((X - 1 + mu) ** 2 + Y**2)

    U = 0.5 * (X**2 + Y**2) + (1 - mu) / r1 + mu / r2
    Jacobi_C = 2 * U

    # --- 3D PLOT ---
    ax1 = fig.add_subplot(121, projection="3d")
    U_clipped = np.clip(U, 1.0, 2.0)
    surf = ax1.plot_surface(X, Y, U_clipped, cmap="plasma", edgecolor="none", rstride=4, cstride=4, antialiased=True)
    
    ax1.set_title("3D Effective Potential Surface", fontsize=13, y=1.02)
    ax1.set_xlabel("$x / a$")
    ax1.set_ylabel("$y / a$")
    ax1.set_zlabel("Effective Potential ($\Omega$)")
    ax1.view_init(elev=35, azim=-50)

    # --- 2D CONTOUR PLOT ---
    ax2 = fig.add_subplot(122)

    def dU_dx(x_val):
        r1_val = abs(x_val + mu)
        r2_val = abs(x_val - 1 + mu)
        term1 = (1 - mu) / (r1_val**2) * np.sign(x_val + mu)
        term2 = mu / (r2_val**2) * np.sign(x_val - 1 + mu)
        return x_val - term1 - term2

    x_l1 = 1 - mu - (mu / 3) ** (1 / 3)
    x_l2 = 1 - mu + (mu / 3) ** (1 / 3)
    x_l3 = -1 - (5 * mu / 12)

    x_l1_num = fsolve(dU_dx, x_l1)[0]
    x_l2_num = fsolve(dU_dx, x_l2)[0]
    x_l3_num = fsolve(dU_dx, x_l3)[0]

    def get_C(x_val, y_val=0):
        r1_c = np.sqrt((x_val + mu) ** 2 + y_val**2)
        r2_c = np.sqrt((x_val - 1 + mu) ** 2 + y_val**2)
        return 2 * (0.5 * (x_val**2 + y_val**2) + (1 - mu) / r1_c + mu / r2_c)

    C_l1 = get_C(x_l1_num)
    C_l2 = get_C(x_l2_num)
    C_l3 = get_C(x_l3_num)
    C_l4 = get_C(0.5 - mu, np.sqrt(3) / 2)

    contour_levels = np.linspace(2.99, 5.0, 600)
    cf = ax2.contourf(X, Y, Jacobi_C, levels=contour_levels, cmap="plasma", extend="both")
    fig.colorbar(cf, ax=ax2, shrink=0.6, aspect=10, label="Jacobi Constant")

    critical_levels = np.sort([C_l1, C_l2, C_l3, C_l4])
    ax2.contour(X, Y, Jacobi_C, levels=critical_levels, colors="k", alpha=0.4, linewidths=1.0)

    ax2.contour(X, Y, Jacobi_C, levels=contour_levels[::50], colors="k", alpha=0.4, linewidths=1.0)

    x_sun = -mu
    x_jup = 1 - mu
    x_l4_l5 = 0.5 - mu
    y_l4 = np.sqrt(3) / 2
    y_l5 = -np.sqrt(3) / 2

    lagrange_x = [x_l1_num, x_l2_num, x_l3_num, x_l4_l5, x_l4_l5]
    lagrange_y = [0, 0, 0, y_l4, y_l5]
    lagrange_labels = ["L1", "L2", "L3", "L4", "L5"]

    ax2.plot(x_sun, 0, "ro", markersize=7, label="Sun")
    ax2.plot(x_jup, 0, "go", markersize=5, label="Jupiter")
    ax2.scatter(lagrange_x, lagrange_y, color="white", marker="x", s=45, linewidths=2, zorder=5)

    for i, txt in enumerate(lagrange_labels):
        ax2.annotate(txt, (lagrange_x[i], lagrange_y[i]), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=9, fontweight="bold", color="dimgray")

    ax2.set_title("Zero-Velocity Curves & Critical Energies", fontsize=13)
    ax2.set_xlabel("$x / a$")
    ax2.set_ylabel("$y / a$")
    ax2.set_aspect("equal")
    ax2.set_xlim(-1.3, 1.3)
    ax2.set_ylim(-1.3, 1.3)
    ax2.legend(loc="upper left", fontsize=8)

    plt.suptitle("Circular Restricted Three-Body Problem: Sun-Jupiter System", fontsize=16, x=0.535, y=0.950)

    plt.savefig(OUTPUT_PATH, dpi=1200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.show()

if __name__ == "__main__":
    plot_mesh()