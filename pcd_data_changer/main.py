import os


def write_file(points, file_path, file_name):
    print(file_path, file_name)
    file = open(file_path + "\\" + file_name, "w")
    for point in points:
        file.write(point + "\n")
    file.close()


def check_file(file, dir_path, file_name):
    # read pcd file
    lines = []
    num_points = 0
    print(file)
    with open(file, 'r') as f:
        for line in f:
            lines.append(line.strip())
            if line.startswith('POINTS'):
                num_points = int(line.split()[-1])
    # change data
    points, mp_ty, mp_points, mp_idx = [], [{} for i in range(30)], [[] for i in range(30)], [0 for i in range(30)]
    for line in lines[-num_points:]:
        x, y, z, rgb, ty, ty_num = list(map(str, line.split()))
        x = float(x)
        y = float(y)
        z = float(z)
        rgb = int(rgb)
        r, g, b = rgb // 256 // 256 % 256, rgb // 256 % 256, rgb % 256
        ty = int(ty)
        ty_num = int(ty_num)
        str_point = (str)(x) + " " + (str)(y) + " " + (str)(z) + " " + (str)(r) + " " + (str)(g) + " " + (str)(b)
        points.append(str_point)
        if ty == 0 or ty_num == -1:
            continue
        if mp_ty[ty].get(ty_num) is None:
            mp_ty[ty][ty_num] = mp_idx[ty]
            mp_idx[ty] += 1
            mp_points[ty].append([])
        mp_points[ty][mp_ty[ty][ty_num]].append(str_point)
    # save
    os.mkdir(dir_path + "\\" + file_name.split(".")[0])
    os.mkdir(dir_path + "\\" + file_name.split(".")[0] + "\\" + "Annotations")
    write_file(points, dir_path + "\\" + file_name.split(".")[0], file_name.split(".")[0] + ".txt")
    for idx in range(30):
        for ty in range(len(mp_ty[idx])):
            file_name_ = (str)(idx) + "_" + (str)(ty) + ".txt"
            dir_path_ = dir_path + "\\" + file_name.split(".")[0] + "\\" + "Annotations"
            print(dir_path_, file_name_)
            write_file(mp_points[idx][ty], dir_path_, file_name_)


if __name__ == '__main__':
    # data path
    path = "D:\\MyProjects\\pythonProject\\Finished"
    PCD = "pcd"
    for file in os.listdir(path):
        file_type = file.split(".")[-1]
        print(file_type)
        if file_type == PCD:
            check_file(path + "\\" + file, path, file)