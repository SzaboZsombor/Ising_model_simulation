"""
Ising Model Simulation - Main Example Usage

This script demonstrates all the available functionality of the Ising model simulation.
Choose which simulation to run by uncommenting the desired function call.
"""

import sys
import os
import numpy as np
from ising_model import IsingModel
from unit_converter import physical_to_simulation, simulation_to_physical
from monte_carlo import monte_carlo_animation, monte_carlo_equilibrium
from visualization import create_animation, plot_thermodynamics, plot_grid_comparison

def example_single_animation():
    """Create animation of spin evolution at a single temperature"""
    print("=== Single Temperature Animation ===")
    
    T_phys = 50  # K
    h_phys = 0.0  # T
    grid_size = 16
    
    T_sim, h_sim, mu_sim = physical_to_simulation(T_phys, h_phys)
    model = IsingModel(grid_size, T_sim, h=h_sim, mu=mu_sim)
    
    print(f"Running animation simulation: T={T_phys}K, grid={grid_size}x{grid_size}")
    E_sim, M_sim, spin_grids = monte_carlo_animation(model, steps=5000)
    
    E_phys, M_phys, _, _ = simulation_to_physical(E_sim, M_sim, 0, 0)
    print(f"Final energy: {E_phys:.4e} J")
    print(f"Final magnetization: {M_phys:.4e} J/T")
    
    save_path = '../plots_and_animations/example_animation.gif'
    create_animation(spin_grids, T_phys, h_phys, save_path=save_path)
    print(f"Animation saved to: {save_path}")

def example_thermodynamics():
    """Calculate thermodynamic properties vs temperature"""
    print("\n=== Thermodynamic Properties ===")
    
    nT = 20  # Reduced for faster execution
    T_phys = np.linspace(250, 400, nT)  # K
    h_phys = 0.0  # T
    grid_size = 16
    
    eq_steps = 100
    measurement_steps = 1000
    N_runs = 50
    
    energies = np.zeros(nT)
    magnetization = np.zeros(nT)
    susceptibility = np.zeros(nT)
    specific_heat = np.zeros(nT)
    
    print(f"Calculating thermodynamics: {nT} temperatures from {T_phys[0]:.0f}K to {T_phys[-1]:.0f}K")
    
    for kT in range(nT):
        print(f"  Temperature {kT+1}/{nT}: {T_phys[kT]:.1f}K")
        
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
    
    save_path = '../plots_and_animations/example_thermodynamics.png'
    plot_thermodynamics(T_phys, energies, magnetization, susceptibility, specific_heat, save_path)
    print(f"Thermodynamic plot saved to: {save_path}")

def example_grid_comparison():
    """Compare different grid sizes"""
    print("\n=== Grid Size Comparison ===")
    
    nT = 15  # Reduced for faster execution
    T_phys = np.linspace(280, 380, nT)  # K
    h_phys = 0.0  # T
    
    grid_sizes = [12, 16, 32]  # Reduced for faster execution
    
    eq_steps = 100
    measurement_steps = 800
    N_runs = 30
    
    energies_dict = {}
    magnetization_dict = {}
    susceptibility_dict = {}
    specific_heat_dict = {}
    
    print(f"Comparing grid sizes: {grid_sizes}")
    print(f"Temperature range: {T_phys[0]:.0f}K to {T_phys[-1]:.0f}K ({nT} points)")
    
    for grid_size in grid_sizes:
        print(f"\nGrid size {grid_size}x{grid_size}:")
        
        energies = np.zeros(nT)
        magnetization = np.zeros(nT)
        susceptibility = np.zeros(nT)
        specific_heat = np.zeros(nT)
        
        for kT in range(nT):
            print(f"  Temperature {kT+1}/{nT}: {T_phys[kT]:.1f}K")
            
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
        
        energies_dict[grid_size] = energies.copy()
        magnetization_dict[grid_size] = magnetization.copy()
        susceptibility_dict[grid_size] = susceptibility.copy()
        specific_heat_dict[grid_size] = specific_heat.copy()
    
    save_path = '../plots_and_animations/example_grid_comparison.png'
    plot_grid_comparison(T_phys, energies_dict, magnetization_dict, susceptibility_dict, 
                        specific_heat_dict, grid_sizes, save_path)
    print(f"Grid comparison plot saved to: {save_path}")

def example_unit_conversion():
    """Demonstrate unit conversion functionality"""
    print("\n=== Unit Conversion Examples ===")
    
    # Physical parameters
    T_phys = 300  # K
    h_phys = 0.1  # T
    
    # Convert to simulation units
    T_sim, h_sim, mu_sim = physical_to_simulation(T_phys, h_phys)
    
    print(f"Physical units:")
    print(f"  Temperature: {T_phys} K")
    print(f"  Magnetic field: {h_phys} T")
    
    print(f"Simulation units:")
    print(f"  Temperature: {T_sim:.6f} (dimensionless)")
    print(f"  Magnetic field: {h_sim:.6f} (dimensionless)")
    print(f"  Magnetic moment: {mu_sim:.6f} (dimensionless)")
    
    # Example simulation values
    E_sim = -1.5  # per spin
    M_sim = 0.8   # per spin
    X_sim = 0.1   # per spin
    C_sim = 0.5   # per spin
    
    # Convert back to physical units
    E_phys, M_phys, X_phys, C_phys = simulation_to_physical(E_sim, M_sim, X_sim, C_sim)
    
    print(f"\nExample simulation results (per spin):")
    print(f"  Energy: {E_sim} (sim) → {E_phys:.4e} J (phys)")
    print(f"  Magnetization: {M_sim} (sim) → {M_phys:.4e} J/T (phys)")
    print(f"  Susceptibility: {X_sim} (sim) → {X_phys:.4e} A²·m⁴/J (phys)")
    print(f"  Specific heat: {C_sim} (sim) → {C_phys:.4e} J/K (phys)")

def main():
    """Main function demonstrating all available functionality"""
    print("Ising Model Simulation - Example Usage")
    print("=" * 50)
    
    # Choose which examples to run
    print("\nAvailable examples:")
    print("1. Single temperature animation")
    print("2. Thermodynamic properties calculation")
    print("3. Grid size comparison")
    print("4. Unit conversion demonstration")
    
    choice = input("\nEnter your choice (1-4, or 'all' for all examples): ").strip()
    
    if choice == '1' or choice == 'all':
        example_single_animation()
    
    if choice == '2' or choice == 'all':
        example_thermodynamics()
    
    if choice == '3' or choice == 'all':
        example_grid_comparison()
    
    if choice == '4' or choice == 'all':
        example_unit_conversion()
    
    print("\n" + "=" * 50)
    print("Example completed!")
    print("\nFor more detailed simulations, use the specific main files:")
    print("  - animation_main.py: Full animation simulation")
    print("  - thermodynamics_main.py: Detailed thermodynamic analysis")
    print("  - grid_comparison_main.py: Comprehensive grid size comparison")

if __name__ == "__main__":
    main()
