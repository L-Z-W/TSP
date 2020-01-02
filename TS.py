import time
import numpy as np

taboo_len = 1000  # 禁忌长度
taboo_table = []  # 禁忌表
champions = []  # 每代最佳个体


def init_path(_path_len):
    _path = list(range(_path_len))
    np.random.shuffle(_path)
    return _path


def cal_dis(_path, _d):
    i = _path.copy()
    _dis = _d[i[0]][i[len(_path)-1]]
    for j in range(len(_path) - 1):
        _dis += _d[i[j]][i[j + 1]]
    return _dis


def get_neighbour(_taboo_table, _taboo_len, _path):
    _neighbour = []
    _len = len(_path)
    # for i in range(1, _len - 1):
    #     for j in range(i + 1, _len):
    #         temp = _path.copy()
    #         temp[i:j] = reversed(temp[i:j])
    #         # temp[i], temp[j] = temp[j], temp[i]
    #         if temp not in _taboo_table:
    #             _neighbour.append(temp)
    for i in range(_taboo_len):
        temp = _path.copy()
        m1 = np.random.randint(0, _len - 2)
        m2 = np.random.randint(m1 + 1, _len - 1)
        temp[m1:m2 + 1] = reversed(temp[m1:m2 + 1])
        if temp not in _taboo_table:
            _neighbour.append(temp)
    while not _neighbour:
        temp = _path.copy()
        m1 = np.random.randint(0, _len - 2)
        m2 = np.random.randint(m1 + 1, _len - 1)
        temp[m1:m2 + 1] = reversed(temp[m1:m2 + 1])
        if temp not in _taboo_table:
            _neighbour.append(temp)
    return _neighbour


def find_champion(_neighbour, _d):
    d_min = cal_dis(_neighbour[0], _d)
    champion = _neighbour[0]
    for i in _neighbour:
        if cal_dis(i, _d) < d_min:
            d_min = cal_dis(i, _d)
            champion = i
    return d_min, champion


def update_taboo(_taboo_table, _taboo_len, _path):
    _taboo_table.append(_path)
    if len(_taboo_table) > _taboo_len:
        del _taboo_table[0]


def tsp_ts(_city, _d, _round):
    global taboo_len, taboo_table, champions
    path = init_path(len(_city))
    t = time.time()
    taboo_len = len(_city)
    for i in range(_round):
        neighbour = get_neighbour(taboo_table, taboo_len, path)
        champion = find_champion(neighbour, _d)
        champions.append(champion)
        path = champion[1]
        print("ts round", i, "best", champion[0])
        update_taboo(taboo_table, taboo_len, path)
    t = time.time() - t

    return champions, min(champions), t

