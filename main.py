#!/usr/bin/env python3.9
from math import dist
from random import random
import numpy as np
from PIL import Image
import pickle
import time
startTime = time.time()

size = 100
depth = 3000
max_box = 13
box_increment = 3

# initialize with random values
image = [[[[0, 0, 0] for i in range(size)] for y in range(size)] for r in range(size)]
for i in range(size):
    for y in range(size):
        for r in range(size):
            val = random()
            image[i][y][r] = val

# adjust values
for box in range(box_increment, max_box, box_increment):
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

                    cur_dist =  abs(dist([box_x, box_y, box_z], [cur_x, cur_y, cur_z])) / box/2
                    image[box_x][box_y][box_z] = image[cur_x][cur_y][cur_z]*(1-cur_dist) + image[box_x][box_y][box_z]*cur_dist

# smooth
def blur(box):
    for cur_x in range(size):
        for cur_y in range(size):
            for cur_z in range(size):
                vals = []
                for x in range(int(-box/2), int(box/2)):
                    for y in range(int(-box/2), int(box/2)):
                        for z in range(int(-box/2), int(box/2)):

                            box_x = cur_x + x
                            box_y = cur_y + y
                            box_z = cur_z + z

                            if box_x > size - 1 or box_y > size - 1 or box_z > size - 1 or box_x < 0 or box_y < 0 or box_z < 0:
                                continue

                            vals.append(image[box_x][box_y][box_z])
                
                image[cur_x][cur_y][cur_z] = sum(vals)/len(vals)

blur(box_increment)

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

with open('data.pickle', 'wb') as handle:
    pickle.dump(image, handle, protocol=pickle.HIGHEST_PROTOCOL)

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
