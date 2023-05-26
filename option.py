import numpy as np


class Option:
    def __init__(self, tiles):
        self.tiles = tiles
        self.collapsed = False

    @property
    def entropy(self):
        return len(self.tiles)

    def collapse(self, id=None):
        self.collapsed = True
        if id is None:
            # pick a random tile from the list
            self.tiles = np.random.choice(self.tiles)
        else:
            self.tiles = self.tiles[id]
