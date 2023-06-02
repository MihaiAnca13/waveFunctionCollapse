import numpy as np


class Option:
    def __init__(self, tiles, collapsed=False, empty=-1, land=-1, entropy=0, update=True):
        self.tiles = []
        self.collapsed = collapsed
        self.EMPTY = empty
        self.LAND = land
        self.entropy = entropy

        if update:
            self.update_tiles(tiles)
        else:
            self.tiles = tiles
        assert len(self.tiles) > 0

    def __deepcopy__(self, memodict={}):
        return Option(self.tiles, self.collapsed, self.EMPTY, self.LAND, self.entropy, update=False)

    def update_tiles(self, new_tiles):
        self.tiles = new_tiles

        self.LAND = -1
        self.EMPTY = -1
        for i, tile in enumerate(self.tiles):
            if tile.is_land:
                self.LAND = i
            elif tile.is_empty:
                self.EMPTY = i

        self.entropy = len(self.tiles)

    @property
    def tile(self):
        if self.collapsed:
            return self.tiles[0]
        else:
            raise ValueError('Option not collapsed')

    def collapse(self, idx=None):
        assert not self.collapsed
        self.collapsed = True
        self.entropy = 0
        if idx is None:
            # pick a random tile from the list based on the weights
            weights = [tile.weight for tile in self.tiles]
            # normalize weights
            weights = np.array(weights) / np.sum(weights)
            idx = np.random.choice(len(self.tiles), p=weights)
            self.tiles = [self.tiles[idx]]
        else:
            assert idx != -1
            self.tiles = [self.tiles[idx]]
