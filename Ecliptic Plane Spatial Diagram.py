from platform import node
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import csv

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_PATH = SCRIPT_DIR / "NASA JPL SBDB - Asteroid Belt and Jovian Trojans Only.csv"
OUTPUT_PATH = SCRIPT_DIR / "Ecliptic_Plane_Spatial_Diagram.png"

def plot_scatter(dataList):

    fig, ax = plt.subplots(figsize=(40, 40))
    ax.set_aspect('equal', adjustable='box')
    ax.set_facecolor(color= "black")        
    fig.patch.set_facecolor(color= "white")

    Jup_x = -2.68
    Jup_y = 4.46

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(dataList, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            data_list = list(reader)
            print(f"Data read from {dataList}: {len(data_list)} rows")    
    except FileNotFoundError:
        print(f"Error: Could not find file at {dataList}")
        return

    e = np.array([float(row[15]) for row in data_list[1:]], dtype=float)     # Eccentricity
    a = np.array([float(row[16]) for row in data_list[1:]], dtype=float)     # Semi-Major Axis
    q = np.array([float(row[17]) for row in data_list[1:]], dtype=float)     # Perihelion Distance
    i = np.array([float(row[18]) for row in data_list[1:]], dtype=float)     # Inclination
    om = np.array([float(row[19]) for row in data_list[1:]], dtype=float)    # Longitude of Ascending Node
    w = np.array([float(row[20]) for row in data_list[1:]], dtype=float)     # Argument of Perihelion
    ma = np.array([float(row[21]) for row in data_list[1:]], dtype=float)    # Mean Anomaly

    om_rad = np.deg2rad(om)
    w_rad = np.deg2rad(w)
    inc_rad = np.deg2rad(i)
    ma_rad = np.deg2rad(ma)

    print(f"Orbital elements extracted from {len(a)} Small Body Objects between 1.8 and 5.5 AU.")

    def solve_kepler(M, e, tol=1e-8, max_iter=1000):
        E = M if e < 0.8 else np.pi
    
        for _ in range(max_iter):
            f = E - e * np.sin(E) - M
            df = 1.0 - e * np.cos(E)
            dE = f / df
            E -= dE
            if abs(dE) < tol:
                return E

    E_values = np.array([solve_kepler(ma_rad[idx], e[idx]) for idx in range(len(a))])

    r = a * (1.0 - e * np.cos(E_values))

    v = 2.0 * np.arctan2(
        np.sqrt(1.0 + e) * np.sin(E_values / 2.0),
        np.sqrt(1.0 - e) * np.cos(E_values / 2.0)
        )

    u = w_rad + v

    cos_OM = np.cos(om_rad)
    sin_OM = np.sin(om_rad)
    cos_i = np.cos(inc_rad)
    cos_u = np.cos(u)
    sin_u = np.sin(u)

    x_values = r * (cos_OM * cos_u - sin_OM * sin_u * cos_i)
    y_values = r * (sin_OM * cos_u + cos_OM * sin_u * cos_i)

    theta_j = np.arctan2(Jup_y, Jup_x)

    cos_t = np.cos(-theta_j)
    sin_t = np.sin(-theta_j)

    x_rot = x_values * cos_t - y_values * sin_t
    y_rot = x_values * sin_t + y_values * cos_t

    Jup_rot_x = np.sqrt(Jup_x**2 + Jup_y**2)
    Jup_rot_y = 0.0

    ax.set_xlim(-9, 9)
    ax.set_ylim(-6.5, 6.5)

    mask_main = (a < 3.8)
    mask_hilda = (a >= 3.8) & (a <= 4.2)
    mask_thule = (a > 4.2) & (a < 4.3)
    mask_trojan_greek = (a >= 5.0) & (a <= 5.5)

    print("Solved Kepler's equation for all Small Body Objects and computed their positions in the ecliptic plane.")

    ax.scatter(x_rot[mask_main], y_rot[mask_main], s=0.06, color='silver', rasterized=True, alpha=0.2, zorder=3, label='Main Belt')
    ax.scatter(x_rot[mask_hilda], y_rot[mask_hilda], s=3.0, color='orange', alpha=0.8, zorder=4, label='Hildas')
    ax.scatter(x_rot[mask_thule], y_rot[mask_thule], s=3.0, color='red', alpha=0.8, zorder=4, label='Thule')
    ax.scatter(x_rot[mask_trojan_greek], y_rot[mask_trojan_greek], s=3.0, color='limegreen', alpha=0.8, zorder=4, label='Greeks and Trojans')

    print("Plotted Small Body Objects in the ecliptic plane with color-coded populations.")

    ax.plot(0, 0, color='yellow', marker='o', markersize=30, zorder=6, label='Sun')  

    planet_elements = {
        'Mercury': {'a': 0.3871, 'e': 0.2056, 'i': 7.00,  'om': 48.33,  'w': 77.46,  'ma': 174.79,  'marker': 4,  'color': 'silver'},
        'Venus':   {'a': 0.7233, 'e': 0.0068, 'i': 3.39,  'om': 76.68,  'w': 131.53, 'ma': 50.11,   'marker': 8,  'color': 'gold'},
        'Earth':   {'a': 1.0000, 'e': 0.0167, 'i': 0.00,  'om': 0.00,   'w': 102.94, 'ma': 357.52,  'marker': 10, 'color': 'deepskyblue'},
        'Mars':    {'a': 1.5237, 'e': 0.0934, 'i': 1.85,  'om': 49.58,  'w': 336.04, 'ma': 19.37,   'marker': 5,  'color': 'tomato'}
    }

    for name, p in planet_elements.items():
        p_om = np.deg2rad(p['om'])
        p_w = np.deg2rad(p['w'])
        p_inc = np.deg2rad(p['i'])
        p_ma = np.deg2rad(p['ma'])
        
        E_p = p_ma if p['e'] < 0.8 else np.pi
        for _ in range(1000):
            f = E_p - p['e'] * np.sin(E_p) - p_ma
            df = 1.0 - p['e'] * np.cos(E_p)
            dE = f / df
            E_p -= dE
            if abs(dE) < 1e-8:
                break
                
        r_p = p['a'] * (1.0 - p['e'] * np.cos(E_p))

        v_p = 2.0 * np.arctan2(
            np.sqrt(1.0 + p['e']) * np.sin(E_p / 2.0),
            np.sqrt(1.0 - p['e']) * np.cos(E_p / 2.0)
            )
        
        u_p = p_w + v_p
        
        x_p_inertial = r_p * (np.cos(p_om) * np.cos(u_p) - np.sin(p_om) * np.sin(u_p) * np.cos(p_inc))
        y_p_inertial = r_p * (np.sin(p_om) * np.cos(u_p) + np.cos(p_om) * np.sin(u_p) * np.cos(p_inc))
        
        x_p_rot = x_p_inertial * cos_t - y_p_inertial * sin_t
        y_p_rot = x_p_inertial * sin_t + y_p_inertial * cos_t
        
        ax.plot(x_p_rot, y_p_rot, color=p['color'], marker='o', markersize=p['marker'], zorder=6, label=name)

    for name, p in planet_elements.items():
        p_om = np.deg2rad(p['om'])
        p_w = np.deg2rad(p['w'])
        p_inc = np.deg2rad(p['i'])
        
        ma_track = np.linspace(0, 2 * np.pi, 500)
        
        E_track = np.zeros_like(ma_track)
        for idx, M_val in enumerate(ma_track):
            E_val = M_val if p['e'] < 0.8 else np.pi
            for _ in range(100):
                f = E_val - p['e'] * np.sin(E_val) - M_val
                df = 1.0 - p['e'] * np.cos(E_val)
                dE = f / df
                E_val -= dE
                if abs(dE) < 1e-8:
                    break
            E_track[idx] = E_val
            
        r_track = p['a'] * (1.0 - p['e'] * np.cos(E_track))
        v_track = 2.0 * np.arctan2(
            np.sqrt(1.0 + p['e']) * np.sin(E_track / 2.0),
            np.sqrt(1.0 - p['e']) * np.cos(E_track / 2.0)
        )

        u_track = p_w + v_track
        
        x_track_inertial = r_track * (np.cos(p_om) * np.cos(u_track) - np.sin(p_om) * np.sin(u_track) * np.cos(p_inc))
        y_track_inertial = r_track * (np.sin(p_om) * np.cos(u_track) + np.cos(p_om) * np.sin(u_track) * np.cos(p_inc))
        
        x_track_rot = x_track_inertial * cos_t - y_track_inertial * sin_t
        y_track_rot = x_track_inertial * sin_t + y_track_inertial * cos_t
        
        ax.plot(x_track_rot, y_track_rot, color=p['color'], alpha=0.5, linestyle='-', linewidth=1.5, zorder=5)

    Jupiter_Orbit= Ellipse(xy=(0,0), height=2 * 5.2038, width=2 * 5.1976, fill=False, color='white', zorder=6)

    ax.plot(Jup_rot_x, Jup_rot_y, color='orange', marker='o', markersize=20, zorder=7, label='Jupiter')
    ax.add_patch(Jupiter_Orbit)

    print("Plotted planetary orbits and positions in the ecliptic plane.")

    l4_x = Jup_rot_x * np.cos(np.pi / 3)
    l4_y = Jup_rot_x * np.sin(np.pi / 3)
    l5_x = Jup_rot_x * np.cos(-np.pi / 3)
    l5_y = Jup_rot_x * np.sin(-np.pi / 3)
    
    ax.plot([l4_x, l5_x], [l4_y, l5_y], 'rx', markersize=15, markeredgewidth=1.5, zorder=7, label='L4 / L5 Centers')

    legend = ax.legend(loc='upper right', facecolor='black', edgecolor='white', labelcolor='white', fontsize=25, markerscale=2)

    for handle in legend.legend_handles:
        if hasattr(handle, "set_markersize"):
            handle.set_markersize(15)
        elif hasattr(handle, "set_sizes"):
            handle.set_sizes([150])

    plt.savefig(OUTPUT_PATH, dpi=600, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"Plot saved successfully to {OUTPUT_PATH}")

    plt.show()

if __name__ == "__main__":
    plot_scatter(DATA_PATH)