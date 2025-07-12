import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'simulation_codes'))

from ising_model import IsingModel
from unit_converter import physical_to_simulation, simulation_to_physical
from monte_carlo import monte_carlo_animation
from visualization import create_animation

def main():
    
    T_phys = 50  # K
    h_phys = 0.04  # T
    grid_size = 16
    
    # Converting to simulation units
    T_sim, h_sim, mu_sim = physical_to_simulation(T_phys, h_phys)
    
    model = IsingModel(grid_size, T_sim, h=h_sim, mu=mu_sim)
    

    print(f"Starting simulation with T={T_phys}K, grid size={grid_size}x{grid_size}")
    E_sim, M_sim, spin_grids = monte_carlo_animation(model, steps=5000)
    
    E_phys, M_phys, _, _ = simulation_to_physical(E_sim, M_sim, 0, 0)
    
    print(f"Final energy: {E_phys:.4e} J")
    print(f"Final magnetization: {M_phys:.4e} J/T")
    
    save_path = '../plots_and_animations/ising_model_animation_16x16.gif'
    create_animation(spin_grids, T_phys, h_phys, save_path=save_path)
    
    print(f"Animation saved to: {save_path}")

if __name__ == "__main__":
    main()
