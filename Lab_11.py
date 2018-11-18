#!/usr/bin/python3
from numpy import arange
from numpy import sign
from math import *
from time import time


MAX_ITER = 10000


def split(a, b, step, f, df):
    steps = int((b-a)/step)
    second = f(a)
    for i in arange(0, steps+1):
        first, second = second, f(a + (i+1) * step)
        if sign(first) != sign(second):
            temp = [df(i)for i in arange(a + i * step, a + (i+1) * step)]
            if sign(min(temp)) == sign(max(temp)):
                yield (a + i * step, a + (i+1) * step)


def comb(a, b, f, df, ddf, eps):
    if ddf(a) > 0 and ddf(b) > 0:
        a, b = b, a
    a0, fa0, i, fb = a, f(a), 0, f(b)
    while abs(a - b) > eps:
        if i == MAX_ITER:
            break
        else:
            i += 1
        b -= fb * (a0 - b) / (fa0 - fb)
        fb = f(b)
        a -= f(a) / df(a)
    return (a + b) / 2


def main():
    text_f = "sin(x) + 0.5"
    text_df = "cos(x)"
    text_ddf = "-sin(x)"

    def f(x):
        return eval(text_f)

    def df(x):
        return eval(text_df)

    def ddf(x):
        return eval(text_ddf)

    with open("incomb") as file:
        a, b, step, eps = [float(i)for i in file.readline().split()]
    x = []
    t = time()
    for i, j in split(a - eps, b + eps, step, f, df):
        x.append(((i, j), comb(i, j, f, df, ddf, eps)))

    print("Function: " + text_f)
    print("Range: %.3f..%.3f" % (a, b))
    print("Step: %.4f" % step)
    print("Eps: %.10f" % eps)
    print("Root:"if len(x) == 1 else
          "Roots(%d): " % len(x) if len(x) > 1 else "No roots")
    for i, j in x:
        print("\tRange: %.4f..%.4f   \tValue of x: %.8f" % (i[0], i[1], j))
    print("Time: %.4f" % (time() - t))


if __name__ == '__main__':
    main()
