from dataclasses import dataclass
import numpy as np

@dataclass
class HistoryRecorder:
  steps: list
  n_rabbits: list
  n_wolves: list

def record(rec, step, state):
  rec.steps.append(step)
  rec.n_rabbits.append(len(state.rabbits.pos))
  rec.n_wolves.append(len(state.wolves.pos))

def to_array(rec) -> tuple:
  return_items = (
    np.array(rec.steps),
    np.array(rec.n_rabbits),
    np.array(rec.n_wolves)
  )

  return return_items

def save_csv(rec, path):
    data = np.column_stack(to_array(rec))
    np.savetxt(path, data, delimiter=',', header='step,n_rabbits,n_wolves')
    
