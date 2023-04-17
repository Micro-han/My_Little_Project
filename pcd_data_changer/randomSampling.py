import os
import random


def write_file(points, file_path, file_name):
    print(file_path, file_name)
    file = open(file_path + "\\" + file_name, "w")
    for point in points:
        file.write(point + "\n")
    file.close()


def random_drop(file, dir_path, file_name):
    lines = []
    cnt = 0
    with open(file, 'r') as f:
        for line in f:
            one_line = line.strip()
            cnt += 1
            tmp = 0
            if cnt > 50:
                tmp = random.randint(0, 100)
            if tmp >= 25:
                continue
            lines.append(one_line)
    write_file(lines, dir_path + "\\" + file_name.split(".")[0], file_name.split(".")[0] + ".txt")


if __name__ == '__main__':
    path = "D:\\MyProjects\\pythonProject\\Finished"
    PCD = "pcd"
    PTS = "pts"
    for file in os.listdir(path):
        file_type = file.split(".")[-1]
        print(file_type)
        if file_type == PTS:
            random_drop(path + "\\" + file, path, file)