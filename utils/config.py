from dataclasses import dataclass

@dataclass
class SimConfig:
  L:        float   # domain size
  sigma:    float   # step std for both species
  Nr0:      int     # initial rabbits
  Nw0:      int     # initial wolves
  rc:       float   # interaction radius
  pr_rep:   float   # rabbit replication prob per step
  pw_eat:   float   # wolf eat prob per rabbit in range
  pw_rep:   float   # wolf replication prob per eat event
  trd:      int     # rabbit max age
  twd:      int     # wolf starvation steps
  n_steps:  int     # total steps to run
  seed:     int     # RNG seed for reproducibility

def case_a() -> SimConfig:
  return SimConfig(
    L=10, sigma=0.5, Nr0=900, Nw0=100, rc=0.5,
    pr_rep=0.02, pw_eat=0.02, pw_rep=0.02,
    trd=100, twd=50, n_steps=3000, seed=42
    )

def case_b() -> SimConfig:
  return SimConfig(
    L=10, sigma=0.5, Nr0=900, Nw0=100, rc=0.5,
    pr_rep=0.02, pw_eat=0.02, pw_rep=0.02,
    trd=50, twd=50, n_steps=3000, seed=42
    )

def case_c() -> SimConfig:
  return SimConfig(
    L=10, sigma=0.05, Nr0=900, Nw0=100, rc=0.5,
    pr_rep=0.02, pw_eat=0.02, pw_rep=0.02,
    trd=100, twd=50, n_steps=3000, seed=42
    )
