import numpy as np

def build_cell_list(pos, cfg):
  nc = int(cfg.L / cfg.rc)

  # get individual cell positions
  ci = (pos[:,0] / cfg.rc).astype(int) % nc
  cj = (pos[:,1] / cfg.rc).astype(int) % nc

  cell_ids = cj * nc + ci # flat array of coords

  cells = {}
  for i, c in enumerate(cell_ids):
    if c not in cells:
      cells[c] = []
    cells[c].append(i)

  return cells

def get_neighbors(cells, c, nc):
  ci, cj = c % nc, c // nc
  indices = []
  for dj in [-1, 0, 1]:
    for di in [-1, 0, 1]:
      neighbor = ((cj + dj) % nc) * nc + ((ci + di) % nc)
      indices += cells.get(neighbor, [])
  return indices

def query_pairs(wolf_pos, rabbit_pos, cells, cfg):
    nc = int(cfg.L / cfg.rc)

    wolf_idx_out = []
    rabbit_idx_out = []

    # assign wolves to cells
    wci = (wolf_pos[:, 0] / cfg.rc).astype(int) % nc
    wcj = (wolf_pos[:, 1] / cfg.rc).astype(int) % nc

    for w in range(len(wolf_pos)):
      c = wcj[w] * nc + wci[w]

      # get all rabbit indices in the 9 neighboring cells
      neighbor_rabbits = get_neighbors(cells, c, nc)
      if len(neighbor_rabbits) == 0:
          continue

      # vectorized distance check against all candidate rabbits
      r_pos = rabbit_pos[neighbor_rabbits]
      d = wolf_pos[w] - r_pos
      d -= cfg.L * np.round(d / cfg.L) # minimum image convention
      dist = np.linalg.norm(d, axis=1)

      close = np.where(dist < cfg.rc)[0]
      wolf_idx_out.extend([w] * len(close))
      rabbit_idx_out.extend([neighbor_rabbits[k] for k in close])

    return np.array(wolf_idx_out, dtype=int), np.array(rabbit_idx_out, dtype=int)
