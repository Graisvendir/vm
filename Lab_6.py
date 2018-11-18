#!/usr/bin/python3
import matplotlib.pyplot as plt
from numpy import arange
from sys import argv


def lagranz(x_list, y_list, x):
    if len(x_list) != len(y_list):
        raise ValueError("Len X != Len Y")
    y = 0
    for j in range(len(y_list)):
        p1, p2 = 1, 1
        for i in range(len(x_list)):
            if i != j:
                p1 *= x-x_list[i]
                p2 *= x_list[j]-x_list[i]
        y += y_list[j] * p1 / p2
    return y


def main():
    f, c = False, False
    if len(argv) > 1 and "f" in argv:
        f = True
    if len(argv) > 1 and "c" in argv:
        c = True
    with open(input("File: ")) as file:
        if f:
            func = eval("lambda x:"+file.readline().replace("\n", ""))
            x = [float(i)for i in file.readline().split()]
        else:
            n = int(file.readline())
            x, y = [], []
            for i in range(n):
                temp = [float(i)for i in file.readline().split()]
                x.append(temp[0])
                y.append(temp[1])
    if f:
        y = [func(i)for i in x]
    print("X = " + " ".join([str(i)for i in x]))
    print("Y = " + " ".join([str(i)for i in y]))
    temp = sorted(zip(x, y), key=lambda c: c[0])
    x, y = [i[0]for i in temp], [i[1]for i in temp]
    print("")
    print("X(sort) = " + " ".join([str(i)for i in x]))
    print("Y(sort) = " + " ".join([str(i)for i in y]))
    if c:
        while True:
            a = input("Enter x(! for exit)")
            if a == "!":
                return
            if f:
                print("y = " + str(lagranz(x, y, float(a))))
                print("y(func) = " + str(func(float(a))))
            else:
                print("y = " + str(lagranz(x, y, float(a))))
    new_x = list(arange(-10, 11, 0.1))
    new_y = [lagranz(x, y, i) for i in new_x]
    if f:
        temp_y = [func(i) for i in new_x]
        plt.plot(x, y, "o", new_x, temp_y, "g", new_x, new_y, "r")
    else:
        plt.plot(x, y, "o", new_x, new_y, "r")
    plt.axis([-10, 10, -10, 10])
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
