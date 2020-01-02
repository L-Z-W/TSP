import numpy as np
import matplotlib.pyplot as plt
import copy
import time

np.random.seed(114514)
pop_size = 10  # 种群数量
pc = 0.9  # 交叉概率 0.9
pm = 0.1  # 变异概率 0.1
pe = 0.1  # 精英占比 0.1 pe * pop_size >= 1
pop = []  # 种群
pop_fit = []  # 种群适应度
champions = []  # 每代最佳个体


def init_pop(_pop_size, _gene_len):
    _pop = []
    one = list(range(_gene_len))
    for i in range(_pop_size):
        np.random.shuffle(one)
        _pop.append(one.copy())
    return _pop


def cal_fit(_pop, _d):
    _pop_fit = []
    _gene_len = len(_pop[0])
    for i in _pop:
        dis = _d[i[0]][i[_gene_len - 1]]
        for j in range(len(_pop[0]) - 1):
            dis += _d[i[j]][i[j + 1]]
        _pop_fit.append(dis)
    return _pop_fit


def find_elites(_pop, _pop_fit, _pe):
    pop_len = len(_pop)
    _elites = []
    candidate = []
    for i in range(pop_len):
        candidate.append([_pop_fit[i], _pop[i]])
    candidate.sort()
    for i in range(int(pop_len * _pe)):
        _elites.append(copy.deepcopy(candidate[i][1]))
    return _elites


def update_elites(_pop, _pop_fit, _old_elites, _old_elites_fit, _pe):
    pop_len = len(_pop)
    _new_elites = []
    candidate = []
    for i in range(pop_len):
        candidate.append([_pop_fit[i], _pop[i]])
    candidate.sort()
    candidate = copy.deepcopy(candidate[0:int(pop_len * _pe)])
    for i in range(int(pop_len * _pe)):
        candidate.append([_old_elites_fit[i], _old_elites[i]])
    candidate.sort()

    _elites = []
    for i in range(int(pop_len * _pe)):
        _elites.append(copy.deepcopy(candidate[i][1]))

    return _elites


def find_champion(_pop, _pop_fit):
    min_f = _pop_fit[0]
    _champion = _pop[0]
    for i in range(len(_pop_fit)):
        if _pop_fit[i] < min_f:
            min_f = _pop_fit[i]
            _champion = _pop[i]
    return min_f, _champion


def selection(_pop, _pop_fit, elites, _champion):
    pop_len = len(_pop)
    p_fit = []
    fit = []
    for i in _pop_fit:
        fit.append(_champion[0] / i)
    total_fit = sum(fit)
    for i in fit:
        p_fit.append(i / total_fit)
    # mean_fit = sum(_pop_fit) / pop_len
    sum_f = 0
    for i in range(len(p_fit) - 1):
        p_fit[i + 1] += sum_f
        sum_f += p_fit[i]
    random_choose = sorted([np.random.random() for i in range(pop_len)])
    fitone = 0
    newone = 0
    next_pop = _pop[:]
    for i in elites:
        next_pop[newone] = i
        newone += 1
    while newone < pop_len:
        if random_choose[newone % pop_len] < p_fit[fitone % pop_len]:
            # if _pop_fit[fitone % pop_len] > mean_fit:
            #     fitone += 1
            #     continue
            next_pop[newone % pop_len] = pop[fitone % pop_len]
            newone += 1
        else:
            fitone += 1

    _pop = next_pop[:]


def crossover(_pop, _pc, _champion):
    pop_len = len(_pop)
    gene_len = len(_pop[0])
    for i in range(pop_len):
        if np.random.random() < _pc:
            f1 = i
            c1 = np.random.randint(0, len(_pop[0]) - 2)
            c2 = np.random.randint(c1 + 1, len(_pop[0]) - 1)
            temp1 = _pop[f1]
            temp2 = _champion[1]
            rest1 = []
            rest2 = []
            for j in temp1:
                if j not in temp2[c1:c2 + 1]:
                    rest1.append(j)
            for j in temp2:
                if j not in temp1[c1:c2 + 1]:
                    rest2.append(j)
            temp1[c1:c2 + 1], temp2[c1:c2 + 1] = temp2[c1:c2 + 1], temp1[c1:c2 + 1]
            temp1[0:c1] = rest1[0:c1]
            temp1[c2 + 1:gene_len + 1] = rest1[c1:gene_len + 1]
            temp2[0:c1] = rest2[0:c1]
            temp2[c2 + 1:gene_len + 1] = rest2[c1:gene_len + 1]
            _pop[f1] = temp1
    # for i in range(pop_len):
    #     if np.random.random() < _pc:
    #         f1 = i
    #         f2 = np.random.randint(0, len(_pop))
    #         c1 = np.random.randint(0, len(_pop[0]) - 2)
    #         c2 = np.random.randint(c1 + 1, len(_pop[0]) - 1)
    #         temp1 = _pop[f1]
    #         temp2 = _pop[f2]
    #         rest1 = []
    #         rest2 = []
    #         for j in temp1:
    #             if j not in temp2[c1:c2 + 1]:
    #                 rest1.append(j)
    #         for j in temp2:
    #             if j not in temp1[c1:c2 + 1]:
    #                 rest2.append(j)
    #         temp1[c1:c2 + 1], temp2[c1:c2 + 1] = temp2[c1:c2 + 1], temp1[c1:c2 + 1]
    #         temp1[0:c1] = rest1[0:c1]
    #         temp1[c2 + 1:gene_len + 1] = rest1[c1:gene_len + 1]
    #         temp2[0:c1] = rest2[0:c1]
    #         temp2[c2 + 1:gene_len + 1] = rest2[c1:gene_len + 1]
    #         _pop[f1] = temp1
    #         _pop[f2] = temp2


def mutation(_pop, _pm):
    _gene_len = len(_pop[0])
    for i in _pop:
        if np.random.random() < _pm:
            m1 = np.random.randint(0, _gene_len - 2)
            m2 = np.random.randint(m1+1, _gene_len - 1)
            i[m1:m2+1] = reversed(i[m1:m2+1])
            # i[m1], i[m2] = i[m2], i[m1]
    return


def plot_current_best(_city, _champion):
    X = []
    Y = []
    for i in _champion[1]:
        X.append(_city[i][0])
    X.append(_city[_champion[1][0]][0])
    for i in _champion[1]:
        Y.append(_city[i][1])
    Y.append(_city[_champion[1][0]][1])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.plot(X, Y, '-o')

    plt.show()


def tsp_ga(_city, _d, _round):
    global pc, pm, pe, pop, pop_size, pop_fit, champions
    gene_len = len(_city)
    generation = _round
    pop = init_pop(pop_size, gene_len)
    pop_fit = cal_fit(pop, _d)
    elites = find_elites(pop, pop_fit, pe)

    t = time.time()
    for i in range(generation):
        pop_fit = cal_fit(pop, _d)
        elites_fit = cal_fit(elites, _d)
        champion = find_champion(pop + elites, pop_fit + elites_fit)
        # champion = find_champion(pop, pop_fit)
        champions.append(copy.deepcopy(champion))
        elites = update_elites(pop, pop_fit, elites, elites_fit, pe)
        print("ga generation", i, "best", champion[0])
        selection(pop, pop_fit, elites, champion)
        crossover(pop, pc, champion)
        mutation(pop, pm)
    t = time.time() - t
    # plot_current_best(_city, champions[-1])
    return champions, min(champions), t

