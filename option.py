import numpy as np


class Option:
    def __init__(self, tiles):
        self.tiles = []
        self.collapsed = False
        self.EMPTY = -1
        self.LAND = -1

        self.update_tiles(tiles)

    def update_tiles(self, new_tiles):
        self.tiles = new_tiles

        self.LAND = -1
        self.EMPTY = -1
        for i, tile in enumerate(self.tiles):
            if np.all(tile.adjacency == 1):
                self.LAND = i
            elif np.all(tile.adjacency == 0):
                self.EMPTY = i

    @property
    def entropy(self):
        return len(self.tiles)

    @property
    def tile(self):
        if self.collapsed:
            return self.tiles
        else:
            raise ValueError('Option not collapsed')

    def collapse(self, idx=None):
        self.collapsed = True
        if idx is None:
            # pick a random tile from the list based on the weights
            weights = [tile.weight for tile in self.tiles]
            # normalize weights
            weights = np.array(weights) / np.sum(weights)
            idx = np.random.choice(len(self.tiles), p=weights)
            self.tiles = self.tiles[idx]
        else:
            assert idx != -1
            self.tiles = self.tiles[idx]
