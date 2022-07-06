#!/usr/bin/env python3.9
from math import dist
from random import random
import numpy as np
from PIL import Image

size = 500
depth = 500
max_box = 60
box_increment = 15

# initialize with random values
image = [[[0, 0, 0] for i in range(size)] for y in range(size)]
for i in range(size):
    for y in range(size):
        val = random()
        image[i][y] = val

# adjust values
for box in range(box_increment, max_box, box_increment):
    for i in range(depth):
        cur_x = int(random() * size)
        cur_y = int(random() * size)
        for x in range(int(-box/2), int(box/2)):
            for y in range(int(-box/2), int(box/2)):

                box_x = cur_x + x
                box_y = cur_y + y

                if cur_x == box_x and cur_y == box_y:
                    continue

                if box_x > size - 1 or box_y > size - 1 or box_x < 0 or box_y < 0:
                    continue

                cur_dist =  abs(dist([box_x, box_y], [cur_x, cur_y])) / box/2
                image[box_x][box_y] = image[cur_x][cur_y]*(1-cur_dist) + image[box_x][box_y]*cur_dist

# smooth
def blur(box):
    for cur_x in range(size):
        for cur_y in range(size):
            vals = []
            for x in range(int(-box/2), int(box/2)):
                for y in range(int(-box/2), int(box/2)):

                    box_x = cur_x + x
                    box_y = cur_y + y

                    if box_x > size - 1 or box_y > size - 1 or box_x < 0 or box_y < 0:
                        continue

                    vals.append(image[box_x][box_y])
            
            image[cur_x][cur_y] = sum(vals)/len(vals)

blur(box_increment)

# prep for output
for i in range(size):
    for y in range(size):
        val = image[i][y]*256
        if val > 256:
            val = 256
        
        image[i][y] = [
            int(val),
            int(val),
            int(val)
        ]

np_data = np.array(image)
im = Image.fromarray(np_data.astype(np.uint8))
im.save("result.jpg")

# plt.imshow(noise)
# plt.savefig("result.png")
