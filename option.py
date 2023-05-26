import numpy as np


class Option:
    def __init__(self, tiles):
        self.tiles = tiles
        self.collapsed = False

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
            # pick a random tile from the list
            self.tiles = np.random.choice(self.tiles)
        else:
            self.tiles = self.tiles[idx]
