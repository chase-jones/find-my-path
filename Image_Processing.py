#!/usr/bin/env python
# coding: utf-8

"""
Translates images into IDing pixels as 1s and 0s.

Right now only works for purely white pixels
"""


import imageio
import pandas as pd


def is_walkable(pixel):
    # If pixel is white
    if (pixel[0] == 255) and (pixel[1] == 255) and (pixel[2] == 255):
        return True
    return False


def get_walkable_matrix(pixel_matrix):
    walkable_matrix = []

    # For each row of pixels in the image
    for row in pixel_matrix:
        new_row = []
        # For each pixel in that row
        for pixel in row:
            if is_walkable(pixel):
                new_row.append(1)
            else:
                new_row.append(0)
        walkable_matrix.append(new_row)

    return walkable_matrix


# Read image in, store as 3D pixel matrix.
# Convert matrix into one where each entry is whether that spot on the floor floorplan
# is walkable or not.

def picture_to_df(csv_path):
    pixel_matrix = imageio.imread(csv_path)
    return pd.DataFrame(get_walkable_matrix(pixel_matrix))

def main():
    pass


if __name__ == "__main__":
    main()

