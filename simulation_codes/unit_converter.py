import numpy as np

k_B = 1.380649e-23       # J/K
J_phys = 2.0e-21         # J
mu_phys = 9.2740100783e-24      # J/T

def physical_to_simulation(T_phys, h_phys=0.0):
    #Converting the physical parameters to simulation units
    T = T_phys * (k_B / J_phys)
    h = h_phys * (mu_phys / J_phys)
    mu = mu_phys / J_phys
    return T, h, mu

def simulation_to_physical(E_sim, M_sim, susceptibility_sim, specific_heat_sim):
    #Converting the simulation results back to physical units
    E_phys = E_sim * J_phys
    M_phys = M_sim * mu_phys
    susceptibility_phys = susceptibility_sim * mu_phys**2 / J_phys
    specific_heat_phys = specific_heat_sim * J_phys**2 / k_B
    return E_phys, M_phys, susceptibility_phys, specific_heat_phys
