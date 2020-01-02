import numpy as np
import time

np.random.seed(114514)

alpha = 1.0  # 信息启发因子
beta = 2.0  # 期望启发因子
rho = 0.3  # 信息挥发因子
q = 100  # 信息素常量
ant_num = 10  # 蚂蚁数量
ants = []
ants_path = []
path_len = []
champions = []


def init_ants_and_path(_ant_num, _city_num):
    _ants = []
    _ants_path = []
    _ants = [0 for i in range(_ant_num)]
    _ants_path = [[0 for j in range(_city_num)] for i in range(_ant_num)]
    return _ants, _ants_path


def cal_dis(_ants_path, _d):
    _path_len = []
    _ants_num = len(_ants_path[0])
    for i in _ants_path:
        dis = _d[i[0]][i[_ants_num - 1]]
        for j in range(len(_ants_path[0]) - 1):
            dis += _d[i[j]][i[j + 1]]
        _path_len.append(dis)
    return _path_len


def find_champion(_ants_path, _path_len):
    min_f = _path_len[0]
    _champion = _ants_path[0]
    for i in range(len(_path_len)):
        if _path_len[i] < min_f:
            min_f = _path_len[i]
            _champion = _ants_path[i]
    return min_f, _champion


def find_path(_i, _ants, _ants_path, _uv, _p, _d, _e, _alpha, _beta):

    trans = 0
    _len = len(_uv)
    for j in range(_len):
        # 制作轮盘转移表
        trans_list = []
        for k in range(len(_uv)):
            trans += np.power(_p[_ants[_i]][_uv[k]], _alpha) * np.power(_e[_ants[_i]][_uv[k]], _beta)
            trans_list.append(trans)

        rand = np.random.random() * (trans_list[-1] - trans_list[0]) + trans_list[0]  # 产生随机数

        for k in range(len(_uv)):
            if rand <= trans_list[k]:
                _ants[_i] = _uv[k]
                break
            else:
                continue

        _uv.remove(_ants[_i])
        _ants_path[_i][j] = _ants[_i]  # 填路径矩阵


def update_pheromone(_ants_path, _ant_num, _city_num, _p, _rho, _d, _q):

    _pd = [[0 for j in range(_city_num)] for i in range(_city_num)]

    for i in range(_ant_num):
        for j in range(_city_num - 1):
            _pd[_ants_path[i][j]][_ants_path[i][j + 1]] += q / _d[_ants_path[i][j]][_ants_path[i][j + 1]]
        _pd[_ants_path[i][_city_num - 1]][_ants_path[i][0]] += q / _d[_ants_path[i][_city_num - 1]][_ants_path[i][0]]
    _p = (1 - _rho) * _p + _pd
    return _p


def tsp_aco(_city, _d, _round):
    global alpha, beta, rho, q, ant_num, ants, ants_path, path_len, champions
    city_num = len(_city)
    p = np.ones((city_num, city_num))  # 信息素浓度
    # ant_num = int(0.5 * city_num)
    ants, ants_path = init_ants_and_path(ant_num, city_num)
    # 期望矩阵
    e_mat_init = 1.0 / (_d + np.diag([10000] * city_num))
    diag = np.diag([1.0 / 10000] * city_num)
    e = e_mat_init - diag

    t = time.time()
    for r in range(_round):
        for i in range(ant_num):
            ants[i] = 0
            uv = list(range(1, city_num))  # 未访问列表
            find_path(i, ants, ants_path, uv, p, _d, e, alpha, beta)
        path_len = cal_dis(ants_path, _d)
        champion = find_champion(ants_path, path_len)
        print("aco round", r, "best", champion[0])
        champions.append(champion)
        p = update_pheromone(ants_path, ant_num, city_num, p, rho, _d, q)
    t = time.time() - t

    return champions, min(champions), t
