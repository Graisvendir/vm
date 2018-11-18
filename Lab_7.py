#!/usr/bin/python3
import matplotlib.pyplot as plt
from numpy import arange
from scipy.interpolate import CubicSpline
from sys import argv
from collections import defaultdict
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
        hi1 = abs(dots[i].x - dots[i + 1].x)
        hi2 = abs(dots[i + 1].x - dots[i].x)
        a = hi1
        b = 2. * ( hi1 + hi2 )
        c = hi2
        d = 6. * ((dots[i + 1].y - dots[i].y) / hi2 - (dots[i].y - dots[i - 1].y) / hi1)
        alpha[i] = c / (b - a * alpha[i - 1])
        beta[i] = (a * beta[i - 1] - d) / (b - a * alpha[i - 1])

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
    x, y = [], []
    variant = int(input("Type: "))
    with open("insline") as file:
        if variant == 1:
            func = eval("lambda x:"+file.readline().replace("\n", ""))
            x = [float(i)for i in file.readline().split()]
            y = [func(i) for i in x]
        elif variant == 2 or variant == 3:
            n = int(file.readline().replace("\n", ""))
            x, y = [], []
            for i in range(n):
                temp = [float(i)for i in file.readline().split()]
                x.append(temp[0])
                y.append(temp[1])

    if variant == 3:
        spline_x = CubicSpline([i for i in range(len(x))], [el for el in x])
        spline_y = CubicSpline([i for i in range(len(y))], [el for el in y])
        lib_x = list(arange(min(x), len(x) - 1.1, 0.1))
        plt.plot(spline_x(lib_x), spline_y(lib_x), label="splines")
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

        plt.plot(new_x, new_y_s, label="splines")

    plt.legend()

    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
