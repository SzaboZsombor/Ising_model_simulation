import numpy as np

class IsingModel:
    def __init__(self, grid_size, temperature, J=1.0, h=0.0, mu=1.0):
        self.grid_size = grid_size
        self.temperature = temperature
        self.spins = np.random.choice([-1, 1], size=(grid_size, grid_size))
        self.J = J
        self.h = h
        self.mu = mu

    def energy(self):
        right = np.roll(self.spins, -1, axis=1)
        down = np.roll(self.spins, -1, axis=0)
        interaction_energy = -self.J * np.sum(self.spins * (right + down)) / 2.0
        field_energy = -self.h * self.mu * np.sum(self.spins)
        return interaction_energy + field_energy
    
    def delta_energy(self, i, j):
        s = self.spins[i, j]
        s_neighbors = (
            self.spins[(i + 1) % self.grid_size, j] +
            self.spins[i, (j + 1) % self.grid_size] +
            self.spins[(i - 1) % self.grid_size, j] +
            self.spins[i, (j - 1) % self.grid_size]
        )
        return 2 * s * (self.J * s_neighbors + self.h * self.mu)

    def magnetization(self):
        return np.sum(self.spins)
