# Ising Model Simulation - Modular Python Code

## Project Structure

```
codes/
├── ising_model.py          # IsingModel class
├── unit_converter.py       # Physical/simulation unit conversion
├── monte_carlo.py          # Monte Carlo simulation algorithms
└── visualization.py        # Plotting and animation functions

Main scripts:
├── animation_main.py       # Creates spin evolution animation
├── thermodynamics_main.py  # Calculates thermodynamic properties
└── grid_comparison_main.py # Compares different grid sizes
```

## Usage

### Create Animation
```bash
python animation_main.py
```

### Calculate Thermodynamic Properties
```bash
python thermodynamics_main.py
```

### Compare Grid Sizes
```bash
python grid_comparison_main.py
```

## Key Features

- **Modular Design**: Each functionality is separated into its own module
- **Unit Conversion**: Automatic conversion between physical and simulation units
- **Optimized Algorithms**: Different Monte Carlo approaches for animation vs. thermodynamics
- **Per-spin Calculations**: All quantities calculated per spin for proper comparison
- **Clean Interface**: Simplified function signatures with only necessary parameters

## Changes from Original

1. **Modularized**: Code split into logical modules
2. **Unit Conversion**: Added automatic physical/simulation unit conversion
3. **Simplified Functions**: Removed unnecessary parameters
4. **Better Names**: Function names now clearly indicate their purpose
5. **Per-spin Quantities**: All calculations normalized per spin
6. **Optimized Algorithms**: Full lattice sweeps for thermodynamics, single flips for animation
