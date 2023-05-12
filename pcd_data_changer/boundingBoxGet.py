import os
import random


N = float(1e9)


def getBoundingBox(file):
    min_x, max_x, min_y, max_y, min_z, max_z = N, -N, N, -N, N, -N
    with open(file, 'r') as f:
        for line in f:
            one_line = line.strip().split()
            min_x = min(min_x, float(one_line[0]))
            max_x = max(max_x, float(one_line[0]))
            min_y = min(min_y, float(one_line[1]))
            max_y = max(max_y, float(one_line[1]))
            min_z = min(min_z, float(one_line[2]))
            max_z = max(max_z, float(one_line[2]))
    return min_x, min_y, min_z, max_x, max_y, max_z


if __name__ == '__main__':
    path = os.getcwd()
    for file in os.listdir(path):
        if file.split('.')[-1] == 'txt':
            boundingBox = getBoundingBox(file)
            print(file, boundingBox)