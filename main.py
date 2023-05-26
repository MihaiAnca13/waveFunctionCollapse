import cv2
import numpy as np
import itertools
from wfc import WaveFunctionCollapse

GRID_W = 50
GRID_H = 50
IMG_SIZE = 1080 // GRID_W


if __name__ == '__main__':
    wfc = WaveFunctionCollapse(GRID_H, GRID_W, IMG_SIZE)
    wfc.load_images('images/')
    wfc.create_tiles()
    wfc.initialise_grid()
    # here I can modify the initial grid any way I want by collapsing tiles
    wfc.run()

    print(f"Working with {len(wfc.tiles)} tiles")
    wfc.display_grid()
    cv2.waitKey(0)
