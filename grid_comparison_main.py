import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'codes'))

import numpy as np
from ising_model import IsingModel
from unit_converter import physical_to_simulation, simulation_to_physical
from monte_carlo import monte_carlo_equilibrium
from visualization import plot_grid_comparison

def main():
    # Physical parameters
    nT = 30
    T_phys = np.linspace(250, 420, nT)  # K
    h_phys = 0.0  # T
    
    # Grid sizes to compare
    grid_sizes = [12, 16, 32, 64, 128, 256]
    
    # Simulation parameters
    eq_steps = 200
    measurement_steps = 1500
    N_runs = 80
    
    # Storage dictionaries
    energies_dict = {}
    magnetization_dict = {}
    susceptibility_dict = {}
    specific_heat_dict = {}
    
    print(f"Starting grid size comparison")
    print(f"Grid sizes: {grid_sizes}")
    print(f"Temperature range: {T_phys[0]:.1f}K to {T_phys[-1]:.1f}K ({nT} points)")
    
    for grid_size in grid_sizes:
        print(f"\nRunning simulation for grid size {grid_size}x{grid_size}")
        
        # Initialize arrays for this grid size
        energies = np.zeros(nT)
        magnetization = np.zeros(nT)
        susceptibility = np.zeros(nT)
        specific_heat = np.zeros(nT)
        
        for kT in range(nT):
            print(f"  Temperature {kT+1}/{nT}: {T_phys[kT]:.1f}K")
            
            # Convert to simulation units
            T_sim, h_sim, mu_sim = physical_to_simulation(T_phys[kT], h_phys)
            
            # Create model
            model = IsingModel(grid_size, T_sim, h=h_sim, mu=mu_sim)
            
            # Accumulate results from multiple runs
            E_total = M_total = X_total = C_total = 0.0
            
            for _ in range(N_runs):
                E_sim, M_sim, X_sim, C_sim = monte_carlo_equilibrium(model, eq_steps, measurement_steps)
                E_total += E_sim
                M_total += M_sim
                X_total += X_sim
                C_total += C_sim
            
            # Average over runs
            E_avg = E_total / N_runs
            M_avg = M_total / N_runs
            X_avg = X_total / N_runs
            C_avg = C_total / N_runs
            
            # Convert to physical units
            E_phys, M_phys, X_phys, C_phys = simulation_to_physical(E_avg, M_avg, X_avg, C_avg)
            
            energies[kT] = E_phys
            magnetization[kT] = M_phys
            susceptibility[kT] = X_phys
            specific_heat[kT] = C_phys
        
        # Store results for this grid size
        energies_dict[grid_size] = energies.copy()
        magnetization_dict[grid_size] = magnetization.copy()
        susceptibility_dict[grid_size] = susceptibility.copy()
        specific_heat_dict[grid_size] = specific_heat.copy()
        
        print(f"Completed grid size {grid_size}x{grid_size}")
    
    # Plot comparison
    save_path = './plots_and_animations/ising_model_results_grid_sizes.png'
    plot_grid_comparison(T_phys, energies_dict, magnetization_dict, susceptibility_dict, 
                        specific_heat_dict, grid_sizes, save_path)
    
    print(f"\nGrid size comparison plotted and saved to: {save_path}")

if __name__ == "__main__":
    main()
