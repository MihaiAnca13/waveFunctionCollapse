import cv2
import numpy as np
import itertools
from wfc import WaveFunctionCollapse
from option import Option

GRID_W = 10
GRID_H = 10
TILES_FROM_EDGE = 1
LAND_SIZE = 3
IMG_SIZE = 720 // GRID_W

assert GRID_H // 2 - TILES_FROM_EDGE > LAND_SIZE


if __name__ == '__main__':
    wfc = WaveFunctionCollapse(GRID_H, GRID_W, IMG_SIZE)
    wfc.load_images('images/')
    wfc.create_tiles()
    print(f"Working with {len(wfc.tiles)} tiles")
    wfc.initialise_grid()

    # here I can modify the initial grid any way I want by collapsing tiles
    for i in range(GRID_H):
        for j in range(GRID_W):
            # check if i and j are outside a circle
            if ((i - GRID_H // 2) ** 2 + (j - GRID_W // 2) ** 2) > (GRID_H // 2 - TILES_FROM_EDGE) ** 2:
                wfc.grid[i, j].collapse(wfc.grid[i, j].EMPTY)
                wfc.propagate_constraints(i, j)
            elif ((i - GRID_H // 2) ** 2 + (j - GRID_W // 2) ** 2) < LAND_SIZE ** 2:
                if wfc.grid[i, j].collapsed and not wfc.grid[i, j].tile.is_land:
                    wfc.grid[i, j] = Option(wfc.tiles)
                wfc.grid[i, j].collapse(wfc.grid[i, j].LAND)
                wfc.propagate_constraints(i, j)

    wfc.run()

    wfc.display_grid()
    cv2.waitKey(0)
