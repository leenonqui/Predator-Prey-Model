# Predator-Prey Simulation

Agent-based prey-predator simulation in 2D implementing a variation of the Lotka-Volterra model.
Built for the Particle Methods course, Spring 2026.

## Model

Two species of agents move on a periodic 2D square domain of size `L`:

- **Rabbits** perform a random walk, replicate stochastically, and die of old age
- **Wolves** perform a random walk, eat nearby rabbits, replicate when they eat, and die of hunger

## Project Structure

```
├── simulation/
│   ├── state.py       # Data containers (RabbitState, WolfState, SimState)
│   ├── grid.py        # Cell list for O(N) neighbor search
│   └── systems.py     # vital_sys, movement_sys, interaction_sys, replication_sys
├── utils/
│   ├── config.py      # SimConfig dataclass and case factories (A, B, C)
│   └── recorder.py    # Population history logging
└── main.py            # Simulation loop and population plots
```

## Usage

Install dependencies:
```bash
pip install -r requirements.txt
```

Run all three cases and plot population dynamics and habitat final state:
```bash
python main.py
```

## Cases

| Case | sigma | trd | Description |
|------|-------|-----|-------------|
| A    | 0.5   | 100 | Baseline — well-mixed, Lotka-Volterra-like oscillations |
| B    | 0.5   | 50  | Shorter rabbit lifespan — stochastic extinction risk |
| C    | 0.05  | 100 | Small step size — spatial clustering, Lotka-Volterra breaks down |

## Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| L         | 10    | Domain size |
| Nr0       | 900   | Initial rabbits |
| Nw0       | 100   | Initial wolves |
| rc        | 0.5   | Interaction radius |
| pr_rep    | 0.02  | Rabbit replication probability per step |
| pw_eat    | 0.02  | Wolf eat probability per rabbit in range |
| pw_rep    | 0.02  | Wolf replication probability per eat event |
| twd       | 50    | Wolf starvation limit (steps) |
