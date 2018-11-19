#!/usr/bin/python3
import matplotlib.pyplot as plt
from numpy import arange
from collections import defaultdict
from math import sinh
import bisect


class Dot:
    def __init__(self, x, y): self.x, self.y = [x, y]


class Tuple:
    a, b, c, d, x = [0., 0., 0., 0., 0.]


def buildSpline(dots):
    splines = defaultdict(lambda: Tuple())
    for i in range(len(dots)):
        splines[i].x, splines[i].a = dots[i].x, dots[i].y

    alpha, beta = [defaultdict(lambda: 0.), defaultdict(lambda: 0.)]

    for i in range(1, len(dots)-1):
        hi1 = abs(dots[i].x - dots[i - 1].x)
        hi2 = abs(dots[i + 1].x - dots[i].x)

        C = 4. * (hi1 + hi2)
        F = 6. * ((dots[i + 1].y - dots[i].y) / hi1 - (dots[i].y - dots[i - 1].y) / hi2)
        z = (hi1 * alpha[i - 1] + C)
        alpha[i] = - hi2 / z
        beta[i] = (F - hi1 * beta[i - 1]) / z

    for i in reversed(range(1, len(dots) - 1)):
        splines[i].c = alpha[i] * splines[i+1].c + beta[i]

    for i in reversed(range(1, len(dots))):
        hi = dots[i].x - dots[i-1].x
        splines[i].d = (splines[i].c - splines[i-1].c) / hi
        splines[i].b = (hi * (2.0 * splines[i].c + splines[i - 1].c) / 6.0 +
                        (dots[i].y - dots[i-1].y) / hi)
    return splines


def calc(splines, x):
    distribution = sorted([t[1].x for t in splines.items()])
    indx = bisect.bisect_left(distribution, x)
    if indx == len(distribution):
        return 0
    dx = x - splines[indx].x
    return (splines[indx].a + splines[indx].b * dx +
            splines[indx].c * dx**2 / 2 +
            splines[indx].d * dx**3 / 6)

def main():
    x, y, t = [], [], []
    variant = int(input("Type: "))
    with open("inspline") as file:
        if variant == 1:
            func = eval("lambda x:"+file.readline().replace("\n", ""))
            x = [float(i)for i in file.readline().split()]
            y = [func(i) for i in x]
        elif variant == 2:
            n = int(file.readline().replace("\n", ""))
            x, y = [], []
            for i in range(n):
                temp = [float(i)for i in file.readline().split()]
                x.append(temp[0])
                y.append(temp[1])
        elif variant == 3:
            n = int(file.readline().replace("\n", ""))
            x, y = [], []
            for i in range(n):
                temp = [float(i)for i in file.readline().split()]
                t.append(temp[0])
                x.append(temp[1])
                y.append(temp[2])

    if variant == 3:
        spline_x = buildSpline([Dot(i, x[i]) for i in range(len(x))])
        spline_y = buildSpline([Dot(i, y[i]) for i in range(len(x))])
        tTemp = list(arange(min(t), len(t) - 1, 0.1))
        new_x = [calc(spline_x, i)for i in tTemp]
        new_y = [calc(spline_y, i)for i in tTemp]
        plt.plot(x, y, "o", label="point")
        plt.plot(new_x, new_y, label="splines")
    else:
        temp = sorted(zip(x, y), key = lambda c: c[0])
        x, y = [i[0]for i in temp], [i[1]for i in temp]
        splines = buildSpline([Dot(x[i], y[i]) for i in range(len(x))])

        for i in splines:
            print(splines[i].a, splines[i].b, splines[i].c, splines[i].d, splines[i].x)

        new_x = list(arange(min(x), max(x), 0.1))
        new_y_s = [calc(splines, i)for i in new_x]

        plt.plot(x, y, "o", label="point")
        if variant == 1:
            temp_y = [func(i) for i in new_x]
            plt.plot(new_x, temp_y, label="natural")
        plt.plot(new_x, new_y_s, label="splines")

    plt.legend()

    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
