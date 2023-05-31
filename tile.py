import cv2
import numpy as np


# assumes that the image is a square
class Tile:
    def __init__(self, base_img):
        self.img = base_img
        self.adjacency = None
        self.weight = 0
        self.compute_adjacency()

    @property
    def is_land(self):
        return np.all(self.adjacency == 1)

    @property
    def is_empty(self):
        return np.all(self.adjacency == 0)

    def compute_adjacency(self):
        self.adjacency = []
        size = self.img.shape[0]
        positions = [size // 4, size // 2, size * 3 // 4]
        self.adjacency = np.array([
            self.img[0, positions[0]],
            self.img[0, positions[1]],
            self.img[0, positions[2]],
            self.img[positions[0], size - 1],
            self.img[positions[1], size - 1],
            self.img[positions[2], size - 1],
            self.img[size - 1, positions[2]],
            self.img[size - 1, positions[1]],
            self.img[size - 1, positions[0]],
            self.img[positions[2], 0],
            self.img[positions[1], 0],
            self.img[positions[0], 0]
        ], dtype=bool)

        if self.is_land:
            self.weight = 1000
        elif self.adjacency.sum() >= 9:
            self.weight = 100
        else:
            self.weight = 1

    def invert(self):
        return Tile(cv2.bitwise_not(self.img))

    def rotate_90(self):
        return Tile(cv2.rotate(self.img, cv2.ROTATE_90_CLOCKWISE))

    def flip_horizontal(self):
        return Tile(cv2.flip(self.img, 1))

    def flip_vertical(self):
        return Tile(cv2.flip(self.img, 0))

    def flip_twice(self):
        return Tile(cv2.flip(self.img, -1))

    def show_tile(self, name='tile'):
        cv2.imshow(name, self.img)

    def get_all_combinations(self):
        return [
            self.rotate_90(),
            self.rotate_90().rotate_90(),
            self.rotate_90().rotate_90().rotate_90(),
            self.flip_vertical(),
            self.flip_vertical().rotate_90(),
            self.flip_vertical().rotate_90().rotate_90(),
            self.flip_vertical().rotate_90().rotate_90().rotate_90(),
            self.invert(),
            self.invert().rotate_90(),
            self.invert().rotate_90().rotate_90(),
            self.invert().rotate_90().rotate_90().rotate_90(),
            self.invert().flip_vertical(),
            self.invert().flip_vertical().rotate_90(),
            self.invert().flip_vertical().rotate_90().rotate_90(),
            self.invert().flip_vertical().rotate_90().rotate_90().rotate_90(),
        ]

    def __eq__(self, other):
        return np.equal(self.img, other.img).all()

    def compatible_N(self, other):
        return np.equal(self.adjacency[:3], other.adjacency[8:5:-1]).all()

    def compatible_E(self, other):
        return np.equal(self.adjacency[3:6], other.adjacency[11:8:-1]).all()

    def compatible_S(self, other):
        return np.equal(self.adjacency[6:9], other.adjacency[2::-1]).all()

    def compatible_W(self, other):
        return np.equal(self.adjacency[9:], other.adjacency[5:2:-1]).all()


if __name__ == '__main__':
    t = Tile(cv2.imread('new_images/14.png', 0))
    t.show_tile()
    t.rotate_90().show_tile('rotated 1')
    t.rotate_90().rotate_90().show_tile('rotated 2')
    t.rotate_90().rotate_90().rotate_90().show_tile('rotated 3')
    t.flip_vertical().show_tile('flipped V')
    t.flip_vertical().rotate_90().show_tile('flipped V 1')
    t.flip_vertical().rotate_90().rotate_90().show_tile('flipped V 2')
    t.flip_vertical().rotate_90().rotate_90().rotate_90().show_tile('flipped V 3')
    cv2.waitKey(0)
    cv2.destroyAllWindows()
