import numpy as np
import time
np.random.seed(114514)
temperature = 1e99  # 初始温度
pt = 0.99  # 降温率
champions = []  # 每代最佳个体


def init_path(_path_len):
    _path = list(range(_path_len))
    np.random.shuffle(_path)
    return _path


def cal_dis(_path, _d):
    i = _path.copy()
    _dis = _d[i[0]][i[len(_path)-1]]
    for j in range(len(_path)-1):
        _dis += _d[i[j]][i[j + 1]]
    return _dis


def change_path(_path):
    i = _path.copy()
    m1 = np.random.randint(0, len(_path) - 2)
    m2 = np.random.randint(m1 + 1, len(_path) - 1)
    i[m1:m2 + 1] = reversed(i[m1:m2 + 1])
    return i


def update_path(_new_path, _new_dis, _path, _dis, _pt, _temperature):
    if _new_dis < _dis:
        _path = _new_path
        _dis = _new_dis
    elif np.random.random() > np.exp(-(_new_dis-_dis)/_temperature):
        _path = _new_path
        _dis = _new_dis
    _temperature = _pt * _temperature
    return _dis, _path, _temperature


def tsp_sa(_city, _d, _round):
    global temperature, champions
    path = init_path(len(_city))
    dis = cal_dis(path, _d)
    t = time.time()
    for i in range(_round):
        new_path = change_path(path)
        new_dis = cal_dis(new_path, _d)
        dis, path, temperature = update_path(new_path, new_dis, path, dis, pt, temperature)
        print("sa round", i, "best", dis)
        champions.append((dis, path))
    t = time.time() - t

    return champions, min(champions), t
