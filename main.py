from utils.config import SimConfig
from utils.recorder import HistoryRecorder, record
from simulation.state import init_state
from simulation.systems import (
  movement_sys, interaction_sys, vital_sys
)

def run_simulation(cfg: SimConfig) -> HistoryRecorder:
  state = init_state(cfg)
  rec = HistoryRecorder(steps=[], n_rabbits=[], n_wolves=[])

  for step in range(cfg.n_steps):
    state = movement_sys(state, cfg)
    state = interaction_sys(state, cfg)
    state = vital_sys(state, cfg)
    record(rec, step, state)

    if len(state.rabbits.pos) == 0 or len(state.wolves.pos) == 0:
      print(F"Extinction at step {step}.")
      break

  return rec

