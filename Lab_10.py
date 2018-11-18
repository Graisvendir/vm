#!/usr/bin/python3
import matplotlib.pyplot as pl
from scipy.interpolate import CubicSpline
from scipy.misc import derivative
from numpy import arange
from numpy.random import uniform


def simps(func, l, u, s, eps):
    last = 0
    if s == "auto":
        s = 1
    iter_count = arange(1, ((u - l) / s))
    while True:
        curr = func(l) + func(u)
        for i in iter_count:
            if i % 2 == 0:
                curr += 2 * func(l + i * s)
            else:
                curr += 4 * func(l + i * s)
        curr *= s/3
        if abs(curr - last) < eps:
            break
        last = curr
        s /= 2
        iter_count = arange(1, ((u - l) / s))
    return curr


def read(filename):
    x, y = [], []
    with open(filename, 'r') as f:
        line = int(f.readline())
        lines = f.readlines()
    for i in range(line):
        line = lines[i].split()
        x.append(float(line[0]))
        y.append(float(line[1]))
    return x, y


def monte_carlo(_x, _y, N):

    def inPolygon(x, y, xp, yp):
        c = 0
        for i in range(len(xp)):
            if(((yp[i] <= y < yp[i-1]) or (yp[i-1] <= y < yp[i])) and
               (x > (xp[i-1] - xp[i]) * (y - yp[i]) /
               (yp[i-1] - yp[i]) + xp[i])):
                c = 1 - c
        return True if c == 1 else False

    xy = zip(uniform(min(_x), max(_x), N), uniform(min(_y), max(_y), N))
    inside, outside = [[], []], [[], []]
    for x, y in xy:
        if inPolygon(x, y, _x, _y):
            inside[0].append(x)
            inside[1].append(y)
        else:
            outside[0].append(x)
            outside[1].append(y)
    area = (max(_x) - min(_x))*(max(_y) - min(_y))*len(inside[0]) / N
    return area, inside, outside


def main():
    step = 0.1
    precision = 0.01
    x, y = read("incar")
    spline_x = CubicSpline([i for i in range(len(x))], [el for el in x])
    spline_y = CubicSpline([i for i in range(len(y))], [el for el in y])
    new_x = list(arange(min(x), len(x) - 1 + step, step))
    __x = [spline_x(i) for i in new_x]
    __y = [spline_y(i) for i in new_x]
    points = int(input("Points: "))
    print("S(Simpson)= %f" % abs(simps(lambda x0: (spline_x(x0) *
                                 derivative(spline_y, x0, dx=1e-10)),
                                 min(x), len(x) - 1, "auto", precision)))

    s, a, b = monte_carlo(__x, __y, points)

    print("S(Monte-Carlo)= %f" % abs(s))
    pl.plot(a[0], a[1], ".", color='red')
    pl.plot(b[0], b[1], ".", color='blue')
    pl.plot(x, y, "o")
    pl.plot(spline_x(new_x), spline_y(new_x), "r", color='green')
    pl.grid(True)
    pl.show()


if __name__ == '__main__':
    main()
