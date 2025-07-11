import numpy as np
from ising_model import IsingModel

def equilibrium_check(energies, eps, window):
    if len(energies) < window:
        return False
    recent = energies[-window:]
    diffs = np.abs(np.diff(recent))
    return np.all(diffs < eps)

def monte_carlo_animation(model, steps, eps=1e-3, window=400):
    """Monte Carlo simulation for animation - single spin flips"""
    energies = []
    magnetizations = []
    spin_grids = []
    step = 0
    
    in_equilibrium = False
    while not in_equilibrium and step < steps:
        i, j = np.random.randint(0, model.grid_size, size=2)
        delta_E = model.delta_energy(i, j)
        
        if delta_E < 0 or np.random.rand() < np.exp(-delta_E / model.temperature):
            model.spins[i, j] *= -1
        
        energies.append(model.energy())
        magnetizations.append(model.magnetization())
        
        if step % 300 == 0:
            spin_grids.append(model.spins.copy())
            in_equilibrium = equilibrium_check(energies, eps, window)
        
        if in_equilibrium:
            print(f"Equilibrium reached at step {step}")
        step += 1
    
    E = np.mean(energies[-10:])
    M = np.mean(magnetizations[-10:])
    return E, M, np.array(spin_grids)

def monte_carlo_equilibrium(model, eq_steps, measurement_steps):
    """Monte Carlo simulation for physical property calculation - full lattice sweeps"""
    beta = 1.0 / model.temperature
    N = model.grid_size
    
    # Equilibration phase
    for _ in range(eq_steps):
        for i in range(N):
            for j in range(N):
                a = np.random.randint(0, N)
                b = np.random.randint(0, N)
                
                delta_E = model.delta_energy(a, b)
                
                if delta_E < 0 or np.random.rand() < np.exp(-delta_E * beta):
                    model.spins[a, b] *= -1
    
    # Measurement phase
    equilibrium_energies = []
    equilibrium_magnetizations = []
    
    for _ in range(measurement_steps):
        for i in range(N):
            for j in range(N):
                a = np.random.randint(0, N)
                b = np.random.randint(0, N)
                
                delta_E = model.delta_energy(a, b)
                
                if delta_E < 0 or np.random.rand() < np.exp(-delta_E * beta):
                    model.spins[a, b] *= -1
        
        equilibrium_energies.append(model.energy() / (N * N))
        equilibrium_magnetizations.append(model.magnetization() / (N * N))
    
    equilibrium_energies = np.array(equilibrium_energies)
    equilibrium_magnetizations = np.array(equilibrium_magnetizations)
    
    # Calculate thermodynamic quantities per spin
    E_avg = np.mean(equilibrium_energies)
    M_avg = np.mean(equilibrium_magnetizations)
    E2_avg = np.mean(equilibrium_energies**2)
    M2_avg = np.mean(equilibrium_magnetizations**2)
    
    susceptibility = beta * (M2_avg - M_avg**2)
    specific_heat = (beta**2) * (E2_avg - E_avg**2)
    
    return E_avg, M_avg, susceptibility, specific_heat
