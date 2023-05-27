from tile import Tile
import cv2
import numpy as np
import os
from option import Option
import itertools


class WaveFunctionCollapse:
    def __init__(self, h, w, image_size):
        self.h = h
        self.w = w
        self.image_size = image_size
        self.images = []
        self.tiles = []
        self.grid = np.zeros((h, w), dtype=object)

    def load_images(self, load_path, resize=True):
        _, _, files = next(os.walk(load_path))
        file_count = len(files)

        # load all images from folder 'images'
        images = []
        for i in range(file_count):
            images.append(cv2.imread(load_path + str(i) + '.png', 0))

        print('Loaded ' + str(len(images)) + ' images')
        self.images = images

        if resize:
            self.resize_images()

    def resize_images(self):
        for i in range(len(self.images)):
            self.images[i] = cv2.resize(self.images[i], (self.image_size, self.image_size))
        return self.images

    def create_tiles(self, remove_duplicates=True):
        tiles = []
        for img in self.images:
            t = Tile(img)
            tiles.append(t)
            tiles.extend(t.get_all_combinations())
        self.tiles = tiles

        if remove_duplicates:
            self.remove_duplicates()

    def remove_duplicates(self):
        new_tiles = []
        for i in range(len(self.tiles)):
            identical = False
            for j in range(i + 1, len(self.tiles)):
                if self.tiles[i] == self.tiles[j]:
                    identical = True
                    break
            if not identical:
                new_tiles.append(self.tiles[i])

        self.tiles = new_tiles

    def initialise_grid(self):
        for i in range(self.h):
            for j in range(self.w):
                self.grid[i, j] = Option(self.tiles)

    def get_min_entropy_tiles(self):
        min_entropy = 1000
        min_tiles = []
        for i in range(self.h):
            for j in range(self.w):
                if not self.grid[i, j].collapsed:
                    assert self.grid[i, j].entropy > 0  # TODO: handle the case where entropy is 0 (backtrack)
                    if self.grid[i, j].entropy < min_entropy:
                        min_entropy = self.grid[i, j].entropy
                        min_tiles = [(i, j)]
                    elif self.grid[i, j].entropy == min_entropy:
                        min_tiles.append((i, j))
        return min_tiles, min_entropy

    def propagate_constraints(self, i, j):
        assert self.grid[i, j].collapsed
        # propagate constraints to the North
        if i > 0 and not self.grid[i - 1, j].collapsed:
            compatible_tiles = []
            for tile in self.grid[i - 1, j].tiles:
                if tile.compatible_S(self.grid[i, j].tile):
                    compatible_tiles.append(tile)
            self.grid[i - 1, j].update_tiles(compatible_tiles)
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
            if len(compatible_tiles) == 1:
                self.grid[i, j - 1].collapse()
                self.propagate_constraints(i, j - 1)

    def display_grid(self):
        # positions = itertools.product(range(GRID_W), range(GRID_H))
        # for (x_i, y_i) in positions:
        #     x = x_i * img_w
        #     y = y_i * img_h
        #     imgmatrix[y:y + img_h, x:x + img_w] = tiles[3].img

        grid = np.zeros((self.h * self.image_size, self.w * self.image_size), np.uint8)
        for i in range(self.h):
            for j in range(self.w):
                if self.grid[i, j].collapsed:
                    grid[i * self.image_size:(i + 1) * self.image_size, j * self.image_size:(j + 1) * self.image_size] = self.grid[i, j].tile.img
                else:
                    grid[i * self.image_size:(i + 1) * self.image_size, j * self.image_size:(j + 1) * self.image_size] = 125
        cv2.imshow('grid', grid)
        cv2.waitKey(1)

    def run(self):
        while True:
            min_tiles, min_entropy = self.get_min_entropy_tiles()
            if len(min_tiles) == 0:
                print('No tiles left to collapse')
                break
            else:
                # pick a random tile from the list
                idx = np.random.choice(len(min_tiles))
                i, j = min_tiles[idx]
                self.grid[i, j].collapse()
                # propagate constraints
                self.propagate_constraints(i, j)

            # display progress
            self.display_grid()
