# Ising Model Simulation with External Field

This project simulates the two-dimensional Ising model in the presence of an external magnetic field using the Metropolis Monte Carlo method. All parameters are expressed in physical units (Kelvin, Tesla, Joules).

## Physical Model

The system consists of discrete spins $S_i = \pm 1$ on a 2D lattice with Hamiltonian:

$$ H = -J \sum_{\langle i,j \rangle} S_i S_j - \mu B \sum_i S_i $$

where:
- $J$ = spin-spin coupling [J] (ferromagnetic when $J > 0$)
- $\mu$ = magnetic moment [J/T] (typically $\mu_B = 9.27 \times 10^{-24}$ J/T)
- $B$ = external field [T]
- $\langle i,j \rangle$ = nearest neighbor pairs

## Key Quantities

### Magnetization
$$ M = \mu \sum_i S_i $$

### Heat Capacity
$$ C = \frac{\langle E^2 \rangle - \langle E \rangle^2}{k_B T^2} $$

### Magnetic Susceptibility
$$ \chi = \frac{\langle M^2 \rangle - \langle M \rangle^2}{k_B T} $$

## Algorithm

1. Initialize $N \times N$ lattice with random spins
2. For each Monte Carlo step:
   - Select random spin $S_i$
   - Calculate energy change $\Delta E = 2S_i(J\sum_{nn}S_j + \mu B)$
   - Flip spin if $\Delta E \leq 0$ or with probability $e^{-\Delta E/(k_B T)}$

## Implementation

```python
class IsingModel:
    def __init__(self, size, J, mu, B, T):
        self.spins = np.random.choice([-1,1], size=(size,size))
        self.J = J  # Coupling [J]
        self.mu = mu  # Moment [J/T]
        self.B = B  # Field [T]
        self.T = T  # Temp [K]
