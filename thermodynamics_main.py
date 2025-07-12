import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'simulation_codes'))

import numpy as np
from ising_model import IsingModel
from unit_converter import physical_to_simulation, simulation_to_physical
from monte_carlo import monte_carlo_equilibrium
from visualization import plot_thermodynamics

sys.path.append(os.path.join(os.path.dirname(__file__), 'simulation_codes'))


def main():
    nT = 60
    T_phys = np.linspace(210, 480, nT)  # K
    h_phys = 0.0  # T
    grid_size = 16
    
    eq_steps = 200
    measurement_steps = 2000
    N_runs = 100
    
    energies = np.zeros(nT)
    magnetization = np.zeros(nT)
    susceptibility = np.zeros(nT)
    specific_heat = np.zeros(nT)
    
    print(f"Starting thermodynamic calculation with grid size {grid_size}x{grid_size}")
    
    for kT in range(nT):
        print(f"Temperature {kT+1}/{nT}: {T_phys[kT]:.1f}K")
        
        T_sim, h_sim, mu_sim = physical_to_simulation(T_phys[kT], h_phys)
        
        model = IsingModel(grid_size, T_sim, h=h_sim, mu=mu_sim)
        
        E_total = M_total = X_total = C_total = 0.0
        
        for _ in range(N_runs):
            E_sim, M_sim, X_sim, C_sim = monte_carlo_equilibrium(model, eq_steps, measurement_steps)
            E_total += E_sim
            M_total += M_sim
            X_total += X_sim
            C_total += C_sim
        
        E_avg = E_total / N_runs
        M_avg = M_total / N_runs
        X_avg = X_total / N_runs
        C_avg = C_total / N_runs
        
        E_phys, M_phys, X_phys, C_phys = simulation_to_physical(E_avg, M_avg, X_avg, C_avg)
        
        energies[kT] = E_phys
        magnetization[kT] = M_phys
        susceptibility[kT] = X_phys
        specific_heat[kT] = C_phys
    

    save_path = 'D:/Egyetem/Tudományos Programozás/Ising_model_simulation/plots_and_animations/ising_model_results_16x16.png'
    plot_thermodynamics(T_phys, energies, magnetization, susceptibility, specific_heat, save_path)
    
    print(f"Results plotted and saved to: {save_path}")

if __name__ == "__main__":
    main()
