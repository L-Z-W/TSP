import numpy as np
import matplotlib.pyplot as plt
import GA
import ACO
import SA
import TS

np.random.seed(114514)
c_range = (150, 150)


def city_generator(_c_num, _c_range):
    _city = []
    for i in range(_c_num):
        x = _c_range[0] * np.random.rand()
        y = _c_range[1] * np.random.rand()
        _city.append((x, y))
    return _city


def cal_distance(_city):
    _d = np.zeros([len(_city), len(_city)])
    for i in range(len(_city)):
        for j in range(len(_city)):
            _d[i][j] = np.sqrt(pow(_city[i][0] - _city[j][0], 2) + pow(_city[i][1] - _city[j][1], 2))
    return _d


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


def plot_champions(_champions):  # 显示最优适应值变化趋势
    X = []
    Y = []
    for i in range(len(_champions)):
        X.append(i)
        t = _champions[i][0]
        Y.append(t)
    plt.plot(X, Y)
    plt.show()


city5 = city_generator(5, c_range)
city8 = city_generator(7, c_range)
city11 = city_generator(11, c_range)
city14 = city_generator(13, c_range)
city17 = city_generator(19, c_range)
city150 = city_generator(150, c_range)
city500 = city_generator(500, c_range)
city1000 = city_generator(1000, c_range)
city34 = [(116.46, 39.92),
          (117.2, 39.13),
          (121.48, 31.22),
          (106.54, 29.59),
          (91.11, 29.97),
          (87.68, 43.77),
          (106.27, 38.47),
          (111.65, 40.82),
          (108.33, 22.84),
          (126.63, 45.75),
          (125.35, 43.88),
          (123.38, 41.8),
          (114.48, 38.03),
          (112.53, 37.87),
          (101.74, 36.56),
          (117, 36.65),
          (113.6, 34.76),
          (118.78, 32.04),
          (117.27, 31.86),
          (120.19, 30.26),
          (119.3, 26.08),
          (115.89, 28.68),
          (113, 28.21),
          (114.31, 30.52),
          (113.23, 23.16),
          (121.5, 25.05),
          (110.35, 20.02),
          (103.73, 36.03),
          (108.95, 34.27),
          (104.06, 30.67),
          (106.71, 26.57),
          (102.73, 25.04),
          (114.1, 22.2),
          (113.33, 22.13)
          ]

city = city34
d = cal_distance(city)

aco_round = 5000
ga_round = 5000
ts_round = 5000
sa_round = 5000
aco_champions, aco_best, aco_t = ACO.tsp_aco(city, d, aco_round)
ga_champions, ga_best, ga_t = GA.tsp_ga(city, d, ga_round)
ts_champions, ts_best, ts_t = TS.tsp_ts(city, d, ts_round)
sa_champions, sa_best, sa_t = SA.tsp_sa(city, d, sa_round)


# sa result
plot_champions(sa_champions)
plot_current_best(city, sa_best)
print("sa best", sa_best[0], "spend", sa_t, "round", sa_round)

# ts result
plot_champions(ts_champions)
plot_current_best(city, ts_best)
print("ts best", ts_best[0], "spend", ts_t, "round", ts_round)

# ga result
plot_champions(ga_champions)
plot_current_best(city, ga_best)
print("ga best", ga_best[0], "spend", ga_t, "round", ga_round)

# aco result
plot_champions(aco_champions)
plot_current_best(city, aco_best)
print("aco best", aco_best[0], "spend", aco_t, "round", aco_round)
