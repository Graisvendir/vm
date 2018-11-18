#!/usr/bin/python3
from math import *
from sys import argv
from time import time
from numpy import arange
from scipy.integrate import quad


def simps(func, l, u, s, eps):
    last = 0
    flag = True
    if s == "auto":
        s = 1
        flag = False
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
            if not flag:
                print("step:%0.10f" % s)
            break
        last = curr
        s /= 2
        iter_count = arange(1, ((u - l) / s))
    return curr


def rect(func, l, u, s, eps):
    last = 0
    flag = True
    if s == "auto":
        s = 1
        flag = False
    iter_count = arange(0, ((u - l) / s))
    while True:
        curr = 0
        for i in iter_count:
            curr += func(l + (i + 0.5) * s)
        curr *= s
        if abs(curr - last) < eps:
            if not flag:
                print("step:%0.10f" % s)
            break
        last = curr
        s /= 2
        iter_count = arange(0, ((u - l) / s))
    return curr


def trap(func, l, u, s, eps):
    last = 0
    flag = True
    if s == "auto":
        s = 1
        flag = False
    iter_count = arange(1, ((u - l) / s))
    while True:
        curr = 0
        for i in iter_count:
            curr += func(l + i * s)
        curr += (func(l) + func(u))/2
        curr *= s
        if abs(curr - last) < eps:
            if not flag:
                print("step:%0.10f" % s)
            break
        last = curr
        s /= 2
        iter_count = arange(1, ((u - l) / s))
    return curr


def main():
    with open(argv[1]) as file:
        func_str = file.readlines()
        func = eval("lambda x:" + func_str[0])
        low, up, step = [float(i) for i in func_str[1].split()]
        if len(func_str) >= 3:
            eps = float(func_str[2])
            step = "auto"
        else:
            eps = 999999
    if step == "auto":
        print("Lower limit: %f, upper limit:%f, accur:%f" % (low, up, eps))
    else:
        print("Lower limit: %f, upper limit:%f, step:%f" % (low, up, step))
    t = time()
    print("-"*80)
    print("Simpson method: \t%.15f" % simps(func, low, up, step, eps))
    print("-"*80)
    print("Medium rectangle method:%.15f" % rect(func, low, up, step, eps))
    print("-"*80)
    print("Trapezoidal method: \t%.15f" % trap(func, low, up, step, eps))
    print("-"*80)
    print("SciPy: \t\t\t%.15f" % quad(func, low, up)[0])
    print("Time: " + str(time() - t))


if __name__ == '__main__':
    main()
