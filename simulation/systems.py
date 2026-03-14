import numpy as np
from simulation.state import SimState, WolfState, RabbitState
from simulation.grid import build_cell_list, query_pairs

def movement_sys(state, cfg) -> SimState:
  r_angles = state.rng.uniform(0, 2*np.pi, len(state.rabbits.pos))
  w_angles = state.rng.uniform(0, 2*np.pi, len(state.wolves.pos))

  r_lengths = state.rng.normal(0, cfg.sigma, len(state.rabbits.pos))
  w_lengths = state.rng.normal(0, cfg.sigma, len(state.wolves.pos))

  r_dx = r_lengths * np.cos(r_angles)
  r_dy = r_lengths * np.sin(r_angles)
  r_delta = np.column_stack([r_dx, r_dy])

  w_dx = w_lengths * np.cos(w_angles)
  w_dy = w_lengths * np.sin(w_angles)
  w_delta = np.column_stack([w_dx, w_dy])

  nr_pos = (state.rabbits.pos + r_delta) % cfg.L
  nw_pos = (state.wolves.pos + w_delta) % cfg.L

  return SimState(
     rabbits = RabbitState(pos=nr_pos, age=state.rabbits.age),
     wolves = WolfState(pos=nw_pos, hunger=state.wolves.hunger),
     rng = state.rng
  )

def interaction_sys(state, cfg):
  r_cl = build_cell_list(state.rabbits.pos, cfg)
  w_idx, r_idx = query_pairs(state.wolves.pos, state.rabbits.pos, r_cl, cfg)

  # Bernoulli eat interaction
  interaction_mask = state.rng.random(len(w_idx)) < cfg.pw_eat
  w_ate = w_idx[interaction_mask]
  r_eaten = r_idx[interaction_mask]

  Nr = len(state.rabbits.pos)
  Nw = len(state.wolves.pos)

  r_alive = np.ones(Nr, dtype=bool)
  r_alive[r_eaten] = False # flag eaten rabbits as dead

  eat_counts = np.bincount(w_ate, minlength=Nw) # count of eaten for each wolf
  # update hunger
  new_hunger = state.wolves.hunger.copy()
  new_hunger[eat_counts > 0] = 0

  state = SimState(
    rabbits = RabbitState(pos=state.rabbits.pos[r_alive], age=state.rabbits.age[r_alive]),
    wolves  = WolfState(pos=state.wolves.pos, hunger=new_hunger),
    rng     = state.rng
    )
  return replication_sys(state, eat_counts, cfg)

def replication_sys(state, eat_counts, cfg):
    rng = state.rng

    # rabbit replication
    r_rep_mask = rng.random(len(state.rabbits.pos)) < cfg.pr_rep
    new_r_pos  = state.rabbits.pos[r_rep_mask]
    new_r_age  = np.zeros(r_rep_mask.sum(), dtype=np.int32)

    # wolf replication
    wolf_repeat_idx  = np.repeat(np.arange(len(state.wolves.pos)), eat_counts)
    w_rep_mask       = rng.random(len(wolf_repeat_idx)) < cfg.pw_rep
    new_w_pos        = state.wolves.pos[wolf_repeat_idx[w_rep_mask]]
    new_w_hunger     = np.zeros(w_rep_mask.sum(), dtype=np.int32)

    return SimState(
        rabbits = RabbitState(
            pos = np.concatenate([state.rabbits.pos, new_r_pos]),
            age = np.concatenate([state.rabbits.age, new_r_age])
        ),
        wolves = WolfState(
            pos    = np.concatenate([state.wolves.pos, new_w_pos]),
            hunger = np.concatenate([state.wolves.hunger, new_w_hunger])
        ),
        rng = state.rng
    )

def vital_sys(state, cfg) -> SimState:
  new_age    = state.rabbits.age + 1
  new_hunger = state.wolves.hunger + 1

  r_alive = new_age    < cfg.trd
  w_alive = new_hunger < cfg.twd

  return SimState(
      rabbits = RabbitState(pos=state.rabbits.pos[r_alive], age=new_age[r_alive]),
      wolves  = WolfState(pos=state.wolves.pos[w_alive],   hunger=new_hunger[w_alive]),
      rng     = state.rng
  )

