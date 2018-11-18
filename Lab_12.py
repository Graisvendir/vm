#!/usr/bin/python3
from numpy.linalg import inv
from numpy import dot


SIZE = 2
EPS = 0.0001


def newtone(df, beg, func):
    norm = 1
    x2 = beg
    while norm > EPS:
        x1 = x2
        x2 = [i - j for i, j in zip(x1, dot(inv(jacobi(x1, df)), func(x1)))]
        norm = sum(abs(i-j)for i, j in zip(x1, x2))
    return x2


def jacobi(args, df):
    matrix = []
    for i in range(SIZE):
        matrix.append([])
        for j in range(SIZE):
            matrix[-1].append(df[i][j](args))
    return matrix


def main():
    global EPS
    EPS = float(input("Enter eps: "))
    beg = [float(i) for i in
           input("Enter the initial approximation(%d num):" % SIZE).split()]
    print("System:")
    func_1_t = "x[0]**5 - x[1]"  # "sin(x[0]+x[1]) - 1.2*x[0]"
    func_2_t = "x[0]**2 + x[1]**2 - 25"
    print(func_1_t + " = " + "0")
    print(func_2_t + " = " + "0")
    df = [[lambda x: 5*x[0]**4, lambda x: -1],
          [lambda x: 2*x[0], lambda x: 2*x[1]]]

    def func(x):
        return (eval(func_1_t), eval(func_2_t))

    dec = newtone(df, beg, func)
    print("Decision:")
    print("x[0] = %.8f, x[1] = %.8f" % (dec[0], dec[1]))
    print(func_1_t + " = %.8f" % func(dec)[0])
    print(func_2_t + " = %.8f" % func(dec)[1])


if __name__ == '__main__':
    main()
