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

    def run(self):
        pass
