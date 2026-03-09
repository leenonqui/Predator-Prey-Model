from dataclasses import dataclass
import numpy as np

@dataclass
class RabbitState:
  pos: np.ndarray
  age: np.ndarray

@dataclass
class WolfState:
  pos: np.ndarray
  hunger: np.ndarray

@dataclass
class SimState:
  rabbits: RabbitState
  wolves: WolfState
  rng: np.random.Generator

def init_state(cfg) -> SimState:
  rng = np.random.default_rng(cfg.seed)
  r_pos = rng.uniform(0, cfg.L, (cfg.Nr0, 2))
  w_pos = rng.uniform(0, cfg.L, (cfg.Nw0, 2))
  r_age = rng.integers(1, cfg.trd, cfg.Nr0, dtype=np.int32)
  w_hunger = np.zeros(cfg.Nw0, dtype=np.int32)

  rabbits = RabbitState(pos=r_pos, age=r_age)
  wolves = WolfState(pos=w_pos, hunger=w_hunger)

  return SimState(rabbits=rabbits, wolves=wolves, rng=rng)
