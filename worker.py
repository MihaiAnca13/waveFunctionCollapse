import multiprocessing
import numpy as np
from copy import deepcopy


class Worker(multiprocessing.Process):
    def __init__(self, h, w, queue, result_queue):
        super().__init__()
        self.h = h
        self.w = w
        self.queue = queue
        self.result_queue = result_queue
        self.grid = None
        self.changes = None

    def run(self):
        while True:
            grid, i, j = self.queue.get()
            if grid is None:
                self.queue.task_done()
                break
            self.grid = grid
            self.changes = np.zeros((self.h, self.w), dtype=np.bool)
            self.grid[i, j].collapse()
            self.propagate_constraints(i, j)
            self.queue.task_done()
            self.result_queue.put((self.grid, self.changes, i, j))

    def propagate_constraints(self, i, j):
        assert self.grid[i, j].collapsed
        self.changes[i, j] = True

        # propagate constraints to the North
        if i > 0 and not self.grid[i - 1, j].collapsed:
            compatible_tiles = []
            for tile in self.grid[i - 1, j].tiles:
                if tile.compatible_S(self.grid[i, j].tile):
                    compatible_tiles.append(tile)
            self.grid[i - 1, j].update_tiles(compatible_tiles)
            self.changes[i - 1, j] = True
            if len(compatible_tiles) == 1:
                self.grid[i - 1, j].collapse()
                self.propagate_constraints(i - 1, j)

        # propagate constraints to the East
        if j < self.w - 1 and not self.grid[i, j + 1].collapsed:
            compatible_tiles = []
            for tile in self.grid[i, j + 1].tiles:
                if tile.compatible_W(self.grid[i, j].tile):
                    compatible_tiles.append(tile)
            self.grid[i, j + 1].update_tiles(compatible_tiles)
            self.changes[i, j + 1] = True
            if len(compatible_tiles) == 1:
                self.grid[i, j + 1].collapse()
                self.propagate_constraints(i, j + 1)

        # propagate constraints to the South
        if i < self.h - 1 and not self.grid[i + 1, j].collapsed:
            compatible_tiles = []
            for tile in self.grid[i + 1, j].tiles:
                if tile.compatible_N(self.grid[i, j].tile):
                    compatible_tiles.append(tile)
            self.grid[i + 1, j].update_tiles(compatible_tiles)
            self.changes[i + 1, j] = True
            if len(compatible_tiles) == 1:
                self.grid[i + 1, j].collapse()
                self.propagate_constraints(i + 1, j)

        # propagate constraints to the West
        if j > 0 and not self.grid[i, j - 1].collapsed:
            compatible_tiles = []
            for tile in self.grid[i, j - 1].tiles:
                if tile.compatible_E(self.grid[i, j].tile):
                    compatible_tiles.append(tile)
            self.grid[i, j - 1].update_tiles(compatible_tiles)
            self.changes[i, j - 1] = True
            if len(compatible_tiles) == 1:
                self.grid[i, j - 1].collapse()
                self.propagate_constraints(i, j - 1)
