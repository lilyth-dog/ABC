---
name: neural-simulation
description: Simulate neural physics using EEG signals and magnonic reservoir computing
version: 1.0.0
author: ABC Project
tags: [neural, physics, simulation, eeg, magnonic]
---

# Neural Simulation Skill

## When to Use

Use this skill when:
- Processing EEG signals (theta/beta waves) into kinematics
- Running magnonic reservoir computing simulations
- Mapping neural states to 3D avatar movements
- Integrating with MuMax3 physics simulation

## Core Capabilities

### 1. EEG-to-Kinematics Pipeline
- **Input**: Theta power (4-8Hz), Beta power (13-30Hz)
- **Process**: Neuro-Magnetic Modulation → Magnonic Reservoir → Readout Layer
- **Output**: Joint angles, fluidity index, physics metadata

### 2. Magnonic Reservoir Computing
- 128x128 grid reservoir for high-dimensional state space
- Pre-computed MuMax3 database for physics-accurate results
- Real-time simulation support (optional)

### 3. Physics Parameters
- **Damping (Alpha)**: Theta power → High damping (relaxation)
- **External Field (B_ext)**: Beta power → High excitation (focus)
- **Magnetic State**: Complex wave patterns from magnonic dynamics

### 4. Readout Layer
- Linear transformation: `y(t) = W_out * m(t) + b`
- Hebbian learning for weight updates
- Output: 20-dimensional kinematic vector

## Implementation Details

### Causal Chain
1. **Neuro-Magnetic Modulation**
   - Theta → Damping coefficient (alpha)
   - Beta → External magnetic field (B_ext)

2. **Magnonic Reservoir Dynamics**
   - Pre-computed patterns from MuMax3
   - Real-time simulation (if enabled)
   - Fallback to mock wave patterns

3. **Spatial Readout**
   - Flatten 128x128 → 16384 vector
   - Linear projection to 20D kinematics
   - Calculate fluidity (inverse of jerk)

### Action Pattern Simulation
- **STAND**: High Theta (0.8), Low Beta (0.1) → Stability
- **WALK**: Moderate Theta (0.4), Moderate Beta (0.5) → Rhythm
- **RUN**: Low Theta (0.1), High Beta (0.9) → High drive

## Best Practices

1. **Pre-computed Database**: Use for production (fast, accurate)
2. **Real-time Simulation**: Enable only for research/demos
3. **Fallback Handling**: Always provide mock patterns for robustness
4. **Fluidity Calculation**: Use variance of kinematics as jerk proxy

## Example Usage

```python
from neuro_controller import MagnonicController

controller = MagnonicController()
result = controller.process_eeg_stream(theta_power=0.7, beta_power=0.3)
# Returns: joint_angles, fluidity_index, sim_params, physics
```

## Related Components

- `neuro_controller.py`: Main controller
- `simulation_db.py`: Pre-computed MuMax3 database
- `mumax3_integration.py`: Real-time simulation integration
- `ovf_parser.py`: OVF file format parser
