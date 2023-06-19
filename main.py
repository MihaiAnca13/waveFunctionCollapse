import cv2
from wfc import WaveFunctionCollapse
from option import Option
import numpy as np

GRID_W = 15
GRID_H = 15
TILES_FROM_EDGE = 1
LAND_SIZE = 3
IMG_SIZE = 720 // GRID_W

assert GRID_H // 2 - TILES_FROM_EDGE > LAND_SIZE

if __name__ == '__main__':
    wfc = WaveFunctionCollapse(GRID_H, GRID_W, IMG_SIZE, num_workers=4)
    wfc.load_images('new_set/')
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

    # display starting state
    wfc.display_grid()
    cv2.waitKey(0)

    wfc.run()

    wfc.display_grid()
    cv2.waitKey(0)

    image = wfc.remove_holes()
    # scale image up
    image = cv2.resize(image, (512, 512), interpolation=cv2.INTER_CUBIC)
    # image = wfc.blur_image(image)
    wfc.display_grid(image)

    # image = image.astype('float32')
    # image /= 255
    # image *= 65535
    # image = image.astype('uint16')

    # create new image where 255 is given sand color and 0 is given water color
    image[image < 125] = 0
    image[image >= 125] = 255
    new_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    new_image[image == 0] = (225, 200, 177)  # water
    mask = image == 255
    new_image[mask] = (191, 223, 242)  # sand
    new_image = cv2.GaussianBlur(new_image, (0, 0), sigmaX=3, sigmaY=3, borderType=cv2.BORDER_DEFAULT)

    cv2.imwrite("output.png", image)
    cv2.imwrite("output_c.png", new_image)
    cv2.waitKey(0)
