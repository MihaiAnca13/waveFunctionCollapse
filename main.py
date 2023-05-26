import cv2
import numpy as np
import itertools
from wfc import WaveFunctionCollapse

GRID_W = 5
GRID_H = 5
IMG_SIZE = 1080 // GRID_W


def display_grid(tiles):
    img_h, img_w = tiles[0].img.shape

    # define how many images per row and column
    imgmatrix = np.zeros((img_h * GRID_H, img_w * GRID_W), np.uint8)

    positions = itertools.product(range(GRID_W), range(GRID_H))
    for (x_i, y_i) in positions:
        x = x_i * img_w
        y = y_i * img_h
        imgmatrix[y:y + img_h, x:x + img_w] = tiles[3].img

    # show the image
    cv2.imshow('imgmatrix', imgmatrix)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    wfc = WaveFunctionCollapse(GRID_H, GRID_W, IMG_SIZE)
    wfc.load_images('images/')
    wfc.create_tiles()
    wfc.initialise_grid()
    # here I can modify the initial grid any way I want by collapsing tiles
    wfc.run()

    print(f"Working with {len(wfc.tiles)} tiles")
    display_grid(wfc.tiles)
