#!/usr/bin/python3
from sys import argv
import numpy as np
from math import *
from prettytable import PrettyTable
from random import random, choice, randint


def diff1(x, y, step):
    res = [(-3 * y[0] + 4 * y[1] - y[2]) / (2 * step)]
    for i in range(1, len(y) - 1):
        res.append((y[i + 1] - y[i - 1]) / (2 * step))
    return res + [(y[-1] - y[-2]) / (x[-1] - x[-2])]


def diff2(x, y, step):
    res = [float('nan')]
    for i in range(1, len(y) - 1):
        res.append((y[i - 1] - 2 * y[i] + y[i + 1]) / (step ** 2))
    return res + [float('nan')]


def diff3(x, y, step):
    res = [float('nan'), float('nan')]
    step = step**3 * 2
    for i in range(2, len(y) - 2):
        res.append((2*y[i - 1] - y[i - 2] - 2*y[i + 1] + y[i + 2]) / step)
    return res + [float('nan'), float('nan')]


def print_xy(x, y):
    table = PrettyTable(field_names=('x', 'y'))
    for i in zip(x, y):
        i = ["%.8f" % round(j, 8) for j in i]
        table.add_row(i)
    print(table)


def print_xydiff(x, y, diff1, diff2, diff3):
    table = PrettyTable(field_names=('x', 'y', 'diff1', 'diff2', 'diff3'))
    for i in zip(x, y, diff1, diff2, diff3):
        i = ["%.5f" % round(j, 5) for j in i]
        table.add_row(i)
    print(table)


def main():
    with open(argv[1]) as file:
        func_str = file.readline()
        func = eval("lambda x:" + func_str)
        beg, end, step = [float(i) for i in file.readline().split()]
    x, y = [], []
    for i in np.arange(beg, end, step):
        x.append(i)
        y.append(func(i))
    print("Function: " + func_str)
    print("Without perturbation:")
    print_xydiff(x, y, diff1(x, y, step), diff2(x, y, step), diff3(x, y, step))
    y1 = []
    d = float(input("Maximum perturbation value: "))
    for i in y:
        y1.append(i + d * randint(-10, 10) * 0.1)
    print("With perturbation(Max val:%f):" % d)
    print_xydiff(x, y1,
                 diff1(x, y1, step),
                 diff2(x, y1, step),
                 diff3(x, y1, step))


if __name__ == '__main__':
    main()
