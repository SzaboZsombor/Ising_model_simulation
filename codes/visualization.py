import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from IPython.display import HTML
import numpy as np

def create_animation(spin_grids, T_phys, h_phys, save_path=None, fps=60):
    """Create animation of spin evolution"""
    fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
    img = ax.imshow(spin_grids[0], cmap='plasma', vmin=-1, vmax=1)
    ax.set_title(f'2D Ising Model: T={T_phys:.2f}K, h={h_phys:.2f}T')
    ax.axis('off')
    fig.tight_layout()

    def update(frame):
        img.set_array(spin_grids[frame])
        return [img]

    ani = FuncAnimation(
        fig,
        update,
        frames=len(spin_grids),
        interval=1000/fps,
        blit=True,
        cache_frame_data=False
    )
    
    if save_path:
        if save_path.endswith('.mp4'):
            writer = FFMpegWriter(fps=fps, bitrate=5000)
            ani.save(save_path, writer=writer, dpi=100)
        else:
            ani.save(save_path, writer='pillow', fps=fps)
    
    plt.close(fig)
    return HTML(ani.to_jshtml(fps=fps))

def plot_thermodynamics(T_phys, energies, magnetization, susceptibility, specific_heat, save_path=None):
    """Plot thermodynamic quantities vs temperature"""
    plt.figure(figsize=(16, 12))
    
    plt.subplot(2, 2, 1)
    plt.plot(T_phys, energies, marker='o', linestyle='--', color='IndianRed')
    plt.xlabel("Temperature (K)", fontsize=20)
    plt.ylabel("Energy per spin (J)", fontsize=20)
    plt.axis('tight')
    
    plt.subplot(2, 2, 2)
    plt.plot(T_phys, abs(magnetization), marker='o', linestyle='--', color='RoyalBlue')
    plt.xlabel("Temperature (K)", fontsize=20)
    plt.ylabel("Magnetization per spin (A·m²)", fontsize=20)
    plt.axis('tight')

    plt.subplot(2, 2, 3)
    plt.plot(T_phys, susceptibility, marker='o', linestyle='--', color='DarkOrange')
    plt.xlabel("Temperature (K)", fontsize=20)
    plt.ylabel("Susceptibility (A²·m⁴/J)", fontsize=20)
    plt.axis('tight')

    plt.subplot(2, 2, 4)
    plt.plot(T_phys, specific_heat, marker='o', linestyle='--', color='DarkGreen')
    plt.xlabel("Temperature (K)", fontsize=20)
    plt.ylabel("Specific Heat (J/K)", fontsize=20)
    plt.axis('tight')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()

def plot_grid_comparison(T_phys, energies_dict, magnetization_dict, susceptibility_dict, specific_heat_dict, grid_sizes, save_path=None):
    """Plot comparison of different grid sizes"""
    plt.figure(figsize=(16, 12))
    
    colors = ['IndianRed', 'RoyalBlue', 'DarkOrange', 'DarkGreen', 'Purple', 'Brown']
    
    plt.subplot(2, 2, 1)
    for i, grid_size in enumerate(grid_sizes):
        plt.plot(T_phys, energies_dict[grid_size], marker='o', linestyle='--', 
                color=colors[i % len(colors)], label=f'Grid {grid_size}x{grid_size}')
    plt.xlabel("Temperature (K)", fontsize=20)
    plt.ylabel("Energy per spin (J)", fontsize=20)
    plt.legend()
    plt.axis('tight')
    
    plt.subplot(2, 2, 2)
    for i, grid_size in enumerate(grid_sizes):
        plt.plot(T_phys, abs(magnetization_dict[grid_size]), marker='o', linestyle='--', 
                color=colors[i % len(colors)], label=f'Grid {grid_size}x{grid_size}')
    plt.xlabel("Temperature (K)", fontsize=20)
    plt.ylabel("Magnetization per spin (A·m²)", fontsize=20)
    plt.legend()
    plt.axis('tight')

    plt.subplot(2, 2, 3)
    for i, grid_size in enumerate(grid_sizes):
        plt.plot(T_phys, susceptibility_dict[grid_size], marker='o', linestyle='--', 
                color=colors[i % len(colors)], label=f'Grid {grid_size}x{grid_size}')
    plt.xlabel("Temperature (K)", fontsize=20)
    plt.ylabel("Susceptibility (A²·m⁴/J)", fontsize=20)
    plt.legend()
    plt.axis('tight')

    plt.subplot(2, 2, 4)
    for i, grid_size in enumerate(grid_sizes):
        plt.plot(T_phys, specific_heat_dict[grid_size], marker='o', linestyle='--', 
                color=colors[i % len(colors)], label=f'Grid {grid_size}x{grid_size}')
    plt.xlabel("Temperature (K)", fontsize=20)
    plt.ylabel("Specific Heat (J/K)", fontsize=20)
    plt.legend()
    plt.axis('tight')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()
