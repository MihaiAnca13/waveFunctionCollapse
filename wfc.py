from tile import Tile
import cv2
import numpy as np
import os
from option import Option
from collections import deque
from copy import deepcopy
import hashlib


class WaveFunctionCollapse:
    def __init__(self, h, w, image_size):
        self.h = h
        self.w = w
        self.image_size = image_size
        self.images = []
        self.tiles = []
        self.grid = np.zeros((h, w), dtype=object)
        self.backtracking_stack = deque(maxlen=h * w * 10)

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

    def hash_grid(self, grid=None):
        if grid is None:
            grid = self.grid
        arr_str = str(grid.flatten()).encode('utf-8')
        return hashlib.sha256(arr_str).hexdigest()

    def get_min_entropy_tiles(self):
        min_entropy = 1000
        min_tiles = []
        for i in range(self.h):
            for j in range(self.w):
                if not self.grid[i, j].collapsed:
                    if self.grid[i, j].entropy == 0:
                        # backtrack
                        print(f"Backtracking with {len(self.backtracking_stack)} items on stack")
                        return None, None
                    if self.grid[i, j].entropy < min_entropy:
                        min_entropy = self.grid[i, j].entropy
                        min_tiles = [(i, j)]
                    elif self.grid[i, j].entropy == min_entropy:
                        min_tiles.append((i, j))
        return np.array(min_tiles), min_entropy

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

    def create_image(self, grid_lines=False):
        if grid_lines:
            image = np.zeros((self.h * self.image_size + self.h - 1, self.w * self.image_size + self.w - 1), dtype=np.uint8) + 70
        else:
            image = np.zeros((self.h * self.image_size, self.w * self.image_size), dtype=np.uint8) + 70

        for i in range(self.h):
            for j in range(self.w):
                if self.grid[i, j].collapsed:
                    if grid_lines:
                        image[i * self.image_size + i:(i + 1) * self.image_size + i, j * self.image_size + j:(j + 1) * self.image_size + j] = self.grid[i, j].tile.img
                    else:
                        image[i * self.image_size:(i + 1) * self.image_size, j * self.image_size:(j + 1) * self.image_size] = self.grid[i, j].tile.img
                else:
                    if grid_lines:
                        image[i * self.image_size + i:(i + 1) * self.image_size + i, j * self.image_size + j:(j + 1) * self.image_size + j] = 125
                    else:
                        image[i * self.image_size:(i + 1) * self.image_size, j * self.image_size:(j + 1) * self.image_size] = 125
        return image

    def display_grid(self, image=None):
        if image is None:
            image = self.create_image(grid_lines=True)
        cv2.imshow('grid', image)
        cv2.waitKey(1)

    def remove_holes(self, radius_in_tiles):
        image = self.create_image()
        image = np.where(image > 200, 255, 0).astype(np.uint8)

        image_w = image.shape[1]
        image_h = image.shape[0]

        count = 1
        # remove holes in the grid
        for i in range(image_h):
            for j in range(image_w):
                if image[i, j] == 0:
                    cv2.floodFill(image, None, (j, i), count)
                    count += 1

        image[image == 1] = 0
        image[image > 1] = 255

        return image

    def run(self):
        i, j = None, None
        while True:
            min_tiles, min_entropy = self.get_min_entropy_tiles()
            if min_tiles is None:
                # backtracking
                new_grid, i, j = self.backtracking_stack.pop()
                self.grid = new_grid
            elif len(min_tiles) == 0:
                print('No tiles left to collapse')
                break
            else:
                np.random.shuffle(min_tiles)
                for (i, j) in min_tiles[:-1]:
                    self.backtracking_stack.append((deepcopy(self.grid), i, j))

                i, j = min_tiles[-1]

            # collapse a tile
            self.grid[i, j].collapse()
            # propagate constraints
            self.propagate_constraints(i, j)

            # display progress
            self.display_grid()
