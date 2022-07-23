#!/usr/bin/env python3.9
from math import dist
from random import random
import numpy as np
from PIL import Image
import pickle
import time
from tqdm import tqdm

def create_noise(size: int, filename: str, chunk_x: int, chunk_y: int, chunk_z: int):
    # initialize with random values
    image = [[[[0] for i in range(size)] for y in range(size)] for r in range(size)]
    for i in range(size):
        for y in range(size):
            for r in range(size):
                val = random()
                image[i][y][r] = val

    for i in range(size):
        with open(f'{filename}/{chunk_x}_{chunk_y}_{chunk_z}.pickle', 'wb') as handle:
            pickle.dump(image[i], handle, protocol=pickle.HIGHEST_PROTOCOL)

    return image

def adjust_values(size_large: int, size_small: int, depth: int, max_box: int, box_increment: int, filename: str, chunk_x: int, chunk_y: int, chunk_z: int):
    # adjust values
    for box in range(max_box, box_increment, -box_increment):
        for i in range(depth):
            cur_x = int(random() * size)
            cur_y = int(random() * size)
            cur_z = int(random() * size)
            for x in range(int(-box/2), int(box/2)):
                for y in range(int(-box/2), int(box/2)):
                    for z in range(int(-box/2), int(box/2)):

                        box_x = cur_x + x
                        box_y = cur_y + y
                        box_z = cur_z + z

                        if box_x > size - 1 or box_y > size - 1 or box_z > size - 1 or box_x < 0 or box_y < 0 or box_z < 0:
                            continue

                        # cur_dist =  abs(dist([box_x, box_y, box_z], [cur_x, cur_y, cur_z])) / box/2
                        image[box_x][box_y][box_z] = (image[cur_x][cur_y][cur_z] + image[box_x][box_y][box_z])/2

    # smooth
    def blur(box):
        box_half = int(box/2)
        for z in tqdm(range(size)):
            for x in range(size):
                for y in range(size):
                    box_x = [image[box_i + x][y][z] for box_i in range(-box_half, box_half) if box_i + x > 0 and box_i + x < size]
                    box_y = [image[x][box_i + y][z] for box_i in range(-box_half, box_half) if box_i + y > 0 and box_i + y < size]
                    box_z = [image[x][y][box_i + z] for box_i in range(-box_half, box_half) if box_i + z > 0 and box_i + z < size]
                    vals = box_x + box_y + box_z
                    image[x][y][z] = np.mean(vals) if vals else image[x][y][z]

    print('blurring')
    blur(box_increment)
    for i in range(size):
        with open(filename + '/' + str(i + chunk_i*size) + '.pickle', 'wb') as handle:
            pickle.dump(image[i], handle, protocol=pickle.HIGHEST_PROTOCOL)


def write_frames(image_data, size):
    for r in range(size):
        image_data = [[[0, 0, 0] for i in range(size)] for y in range(size)]
        # prep for output
        for i in range(size):
            for y in range(size):
                val = image[i][y][r]*256
                if val > 256:
                    val = 256
                
                image_data[i][y] = [
                    int(val),
                    int(val),
                    int(val)
                ]

        np_data = np.array(image_data)
        im = Image.fromarray(np_data.astype(np.uint8))
        im.save("images/result" + str(r) + ".jpg")

chunk_dim = 5
chunk_count = int(chunk_dim*chunk_dim*chunk_dim)
size = 100
depth = 1500
max_box = 20
box_increment = 5
# print("initializing")
# for chunk_x in tqdm(list(range(chunk_dim))):
#     for chunk_y in list(range(chunk_dim)):
#         for chunk_z in list(range(chunk_dim)):
#             create_noise(size, 'random1', chunk_x, chunk_y, chunk_z)
#             create_noise(size, 'random2', chunk_x, chunk_y, chunk_z)
#             create_noise(size, 'random3', chunk_x, chunk_y, chunk_z)

print("bluring")
for chunk_x in tqdm(list(range(chunk_dim))):
    for chunk_y in list(range(chunk_dim)):
        for chunk_z in list(range(chunk_dim)):
            adjust_values(int(size*chunk_dim), size, depth, max_box, box_increment, 'noise1', chunk_x, chunk_y, chunk_z)
            adjust_values(int(size*chunk_dim), size, depth, max_box, box_increment, 'noise2', chunk_x, chunk_y, chunk_z)
            adjust_values(int(size*chunk_dim), size, depth, max_box, box_increment, 'noise3', chunk_x, chunk_y, chunk_z)

# size = 100
# depth = 1500
# max_box = 20
# box_increment = 5
# image = create_noise(size, depth, max_box, box_increment, 'test', 0)
# write_frames(image, size)
