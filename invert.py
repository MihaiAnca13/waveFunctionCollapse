import cv2
import os

# Path where the images are stored
path = 'images'

# List all images in the folder
images = os.listdir(path)

# Loop through all images
for image_name in images:
    if image_name.endswith('.png') or image_name.endswith('.jpg'):
        print('Inverting image ' + image_name)
        # Read the image
        img = cv2.imread(path + '/' + image_name, cv2.IMREAD_GRAYSCALE)

        # Invert the image
        inverted_img = 255 - img

        # Save the inverted image
        cv2.imwrite('new_images/' + image_name, inverted_img)