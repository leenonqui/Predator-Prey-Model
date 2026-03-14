import matplotlib.pyplot as plt
from utils.config import SimConfig, case_a, case_b, case_c
from utils.recorder import HistoryRecorder, record, to_array
from simulation.state import init_state
from simulation.systems import (
  movement_sys, interaction_sys, vital_sys
)

def run_simulation(cfg: SimConfig) -> HistoryRecorder:
  state = init_state(cfg)
  print(f"Initial wolves: {len(state.wolves.pos)}")  # should be 100
  print(f"Initial rabbits: {len(state.rabbits.pos)}")  # should be 900
  rec = HistoryRecorder(steps=[], n_rabbits=[], n_wolves=[])

  for step in range(cfg.n_steps):
    state = vital_sys(state, cfg)
    state = movement_sys(state, cfg)
    state = interaction_sys(state, cfg)
    record(rec, step, state)

    if len(state.rabbits.pos) == 0 or len(state.wolves.pos) == 0:
      print(f"Extinction at step {step}.")
      break

  return rec

def plot_results(rec, title):
    steps, n_rabbits, n_wolves = to_array(rec)
    plt.figure()
    plt.plot(steps, n_rabbits, label='Rabbits')
    plt.plot(steps, n_wolves,  label='Wolves')
    plt.xlabel('Step')
    plt.ylabel('Population')
    plt.title(title)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    for cfg, label in [(case_a(), "Case A"), (case_b(), "Case B"), (case_c(), "Case C")]: # , (case_b(), "Case B"), (case_c(), "Case C")
      rec = run_simulation(cfg)
      plot_results(rec, label)
