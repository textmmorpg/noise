#!/usr/bin/env python3.9
import chunk
from math import dist
from random import random
import numpy as np
from PIL import Image
import pickle
import time
from tqdm import tqdm

def create_noise(size: int, depth: int, max_box: int, box_increment: int, filename: str, chunk_x: int, chunk_y: int, chunk_z: int):
    startTime = time.time()
    # initialize with random values
    # print('initializing')
    image = [[[[0] for i in range(size)] for y in range(size)] for r in range(size)]
    for i in range(size):
        for y in range(size):
            for r in range(size):
                val = random()
                image[i][y][r] = val

    # adjust values
    # print('running adjustment')
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

    def blur(box):
        box_half = int(box/2)
        for z in range(size):
            for x in range(size):
                for y in range(size):
                    box_x = [image[box_i + x][y][z] for box_i in range(-box_half, box_half) if box_i + x > 0 and box_i + x < size]
                    box_y = [image[x][box_i + y][z] for box_i in range(-box_half, box_half) if box_i + y > 0 and box_i + y < size]
                    box_z = [image[x][y][box_i + z] for box_i in range(-box_half, box_half) if box_i + z > 0 and box_i + z < size]
                    vals = box_x + box_y + box_z
                    image[x][y][z] = np.mean(vals) if vals else image[x][y][z]

    # print('blurring')
    blur(box_increment)
    # executionTime = (time.time() - startTime)
    # print('Execution time in seconds: ' + str(executionTime))

    with open(f'{filename}/{chunk_x}_{chunk_y}_{chunk_z}.pickle', 'wb') as handle:
        pickle.dump(image, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return image

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

def create_chunks(chunk_grid_size, size, i):
    for chunk_x in tqdm(range(chunk_grid_size)):
        for chunk_y in range(chunk_grid_size):
            for chunk_z in range(chunk_grid_size):

                depth = 3000
                max_box = 13
                box_increment = 3

                create_noise(size, depth, max_box, box_increment, f'noise{i+1}', chunk_x, chunk_y, chunk_z)


def blur_chunk_side(box, xyz, side, chunk1, chunk2, chunk_size):
    box_half = int(box/2)
    for z in range(size):
        for x in range(size):
            for y in range(size):
                box_x = [chunk1[box_i + x][y][z] for box_i in range(-box_half, box_half) if box_i + x > 0 and box_i + x < size]
                box_y = [chunk1[x][box_i + y][z] for box_i in range(-box_half, box_half) if box_i + y > 0 and box_i + y < size]
                box_z = [chunk1[x][y][box_i + z] for box_i in range(-box_half, box_half) if box_i + z > 0 and box_i + z < size]
                vals = box_x + box_y + box_z
                chunk1[x][y][z] = np.mean(vals) if vals else chunk1[x][y][z]
    
    return chunk1
                
def blur_chunks(chunk1, chunk2, filename1, filename2, xyz, side):
    chunk1 = blur_chunk_side(13, xyz, side, chunk1, chunk2)
    chunk1 = blur_chunk_side(5, xyz, side, chunk1, chunk2)
    chunk2 = blur_chunk_side(13, xyz, side, chunk2, chunk1)
    chunk2 = blur_chunk_side(5, xyz, side, chunk2, chunk1)

    with open(filename1, 'wb') as handle:
        pickle.dump(chunk1, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(filename2, 'wb') as handle:
        pickle.dump(chunk2, handle, protocol=pickle.HIGHEST_PROTOCOL)


def blur_chunks_together(i, chunk_grid_size, chunk_size):
    for chunk_x in tqdm(range(chunk_grid_size)):
        for chunk_y in range(chunk_grid_size):
            for chunk_z in range(chunk_grid_size):

                cur_filename = f'noise{i+1}/{chunk_x}_{chunk_y}_{chunk_z}.pickle'
                with open(cur_filename, 'rb') as f:
                    cur_chunk = pickle.load(f)

                if chunk_x != 0:
                    chunk_filename = f'noise{i+1}/{chunk_x-1}_{chunk_y}_{chunk_z}.pickle'
                    with open(chunk_filename, 'rb') as f:
                        blur_chunks(cur_chunk, pickle.load(f), cur_filename, chunk_filename, 'x', -1)

                if chunk_x != chunk_grid_size-1:
                    chunk_filename = f'noise{i+1}/{chunk_x+1}_{chunk_y}_{chunk_z}.pickle'
                    with open(chunk_filename, 'rb') as f:
                        blur_chunks(cur_chunk, pickle.load(f), cur_filename, chunk_filename, 'x', 1)

                if chunk_y != 0:
                    chunk_filename = f'noise{i+1}/{chunk_x}_{chunk_y-1}_{chunk_z}.pickle'
                    with open(chunk_filename, 'rb') as f:
                        blur_chunks(cur_chunk, pickle.load(f), cur_filename, chunk_filename, 'y', -1)

                if chunk_y != chunk_grid_size-1:
                    chunk_filename = f'noise{i+1}/{chunk_x}_{chunk_y+1}_{chunk_z}.pickle'
                    with open(chunk_filename, 'rb') as f:
                        blur_chunks(cur_chunk, pickle.load(f), cur_filename, chunk_filename, 'y', 1)

                if chunk_z != 0:
                    chunk_filename = f'noise{i+1}/{chunk_x}_{chunk_y}_{chunk_z-1}.pickle'
                    with open(chunk_filename, 'rb') as f:
                        blur_chunks(cur_chunk, pickle.load(f), cur_filename, chunk_filename, 'z', -1)

                if chunk_z != chunk_grid_size-1:
                    chunk_filename = f'noise{i+1}/{chunk_x}_{chunk_y}_{chunk_z+1}.pickle'
                    with open(chunk_filename, 'rb') as f:
                        blur_chunks(cur_chunk, pickle.load(f), cur_filename, chunk_filename, 'z', 1)
                
if __name__ == "__main__":
    size = 100
    chunk_grid_size = 5
    for i in range(1,3):
        # create_chunks(chunk_grid_size, size, i)
        blur_chunks_together(i, chunk_grid_size, size)
