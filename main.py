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

    with open(f'{filename}/{chunk_x}_{chunk_y}_{chunk_z}.pickle', 'wb') as handle:
        pickle.dump(image, handle, protocol=pickle.HIGHEST_PROTOCOL)

def adjust_values(size_large: int, size_small: int, depth: int, max_box: int, box_increment: int, filename: str, chunk_x: int, chunk_y: int, chunk_z: int):

    cur_image = pickle.load(open(f'{filename}/{chunk_x}_{chunk_y}_{chunk_z}.pickle', 'rb'))

    images = {
        f'{chunk_x}_{chunk_y}_{chunk_z}': cur_image,
    }

    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                images[f'{chunk_x+x}_{chunk_y+y}_{chunk_z+z}'] = pickle.load(open(f'{filename}/{chunk_x}_{chunk_y}_{chunk_z}.pickle', 'rb'))

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

                        real_x = box_x + size_small * chunk_x
                        real_y = box_y + size_small * chunk_y
                        real_z = box_z + size_small * chunk_z

                        cur_chunk_x = int(real_x / size_small)
                        cur_chunk_y = int(real_y / size_small)
                        cur_chunk_z = int(real_z / size_small)

                        # if box_x > size - 1 or box_y > size - 1 or box_z > size - 1 or box_x < 0 or box_y < 0 or box_z < 0:
                        #     continue

                        if real_x > size_large - 1 or real_y > size_large - 1 or real_z > size_large - 1 or real_x < 0 or real_y < 0 or real_z < 0:
                            continue

                        box_image = images[f'{cur_chunk_x}_{cur_chunk_y}_{cur_chunk_z}']

                        # cur_dist =  abs(dist([box_x, box_y, box_z], [cur_x, cur_y, cur_z])) / box/2
                        box_image[box_x % size_small][box_y % size_small][box_z % size_small] = (cur_image[cur_x][cur_y][cur_z] + box_image[box_x % size_small][box_y % size_small][box_z % size_small])/2

    # # smooth
    # def blur(box):
    #     box_half = int(box/2)
    #     for z in range(size):
    #         for x in range(size):
    #             for y in range(size):
    #                 box_x = [image[box_i + x][y][z] for box_i in range(-box_half, box_half) if box_i + x > 0 and box_i + x < size]
    #                 box_y = [image[x][box_i + y][z] for box_i in range(-box_half, box_half) if box_i + y > 0 and box_i + y < size]
    #                 box_z = [image[x][y][box_i + z] for box_i in range(-box_half, box_half) if box_i + z > 0 and box_i + z < size]
    #                 vals = box_x + box_y + box_z
    #                 image[x][y][z] = np.mean(vals) if vals else image[x][y][z]

    # print('blurring')
    # blur(box_increment)

    for image in images:
        with open(f'{filename}/{image}.pickle', 'wb') as handle:
            pickle.dump(images[image], handle, protocol=pickle.HIGHEST_PROTOCOL)

chunk_dim = 5
chunk_count = int(chunk_dim*chunk_dim*chunk_dim)
size = 100
depth = 1500
max_box = 20
box_increment = 5
print("initializing")
for chunk_x in tqdm(list(range(chunk_dim))):
    for chunk_y in list(range(chunk_dim)):
        for chunk_z in list(range(chunk_dim)):
            create_noise(size, 'noise1', chunk_x, chunk_y, chunk_z)
            create_noise(size, 'noise2', chunk_x, chunk_y, chunk_z)
            create_noise(size, 'noise3', chunk_x, chunk_y, chunk_z)

print("bluring")
for chunk_x in tqdm(list(range(chunk_dim))):
    for chunk_y in list(range(chunk_dim)):
        for chunk_z in list(range(chunk_dim)):
            adjust_values(int(size*chunk_dim), size, depth, max_box, box_increment, 'noise1', chunk_x, chunk_y, chunk_z)
            adjust_values(int(size*chunk_dim), size, depth, max_box, box_increment, 'noise2', chunk_x, chunk_y, chunk_z)
            adjust_values(int(size*chunk_dim), size, depth, max_box, box_increment, 'noise3', chunk_x, chunk_y, chunk_z)
