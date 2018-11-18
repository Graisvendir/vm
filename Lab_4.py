#!/usr/bin/python3
from numpy import dot, empty, array
from numpy.linalg import inv

MAX_PRECISION = 0.00000000000001
MAX_ITER = 100000


def norm(vector):
    m = -9999999999
    for i in vector:
        if i > m:
            m = i
    return m


def scalar(a, b):
    return sum(i[0]*i[1] for i in zip(a, b))


def printer(A):
    for i in range(len(A)):
        print("\t".join([str(i)for i in
              list(map(lambda x: round(x, 4), A[i]))]))
    print("")


def calcAdjacentEigenValue(A, vector, size, initial):
    """Calculate an eigen value for 'matrix', adjacent to 'initial'"""
    tmp = range(size)
    B = inv([[A[i][j]-initial if i == j else A[i][j]for j in tmp]for i in tmp])
    x = array(vector).transpose().reshape(size)
    xn = empty(size)
    lam, adj_lambda, last, i = 0, 0, 1, 0
    while abs(last-lam) >= MAX_PRECISION:
        last = lam
        xn = dot(B, x)
        lam = sum(xn*x) / sum(x*x)
        adj_lambda = initial + sum(x*x) / sum(xn*x)
        x = xn[:]
        i += 1
    return adj_lambda


def max_lambda(A, base_vector):
    L0, L1 = 0, 1
    X0 = base_vector
    iterates = 0

    while abs(L0-L1) > MAX_PRECISION:
        L0 = L1

        if not iterates % 10:
            _norm = norm(X0)
            X0 = [i / _norm for i in X0]

        X1 = list(dot(A, X0))
        L1 = scalar(X1, X0) / scalar(X0, X0)
        X0 = X1.copy()
        iterates += 1
        if iterates >= MAX_ITER:
            raise ValueError("Iterates > MAX")

    _norm = norm(X0)
    X0 = [i / _norm for i in X0]

    return L1, X0, iterates


def sec_lambda(A, base_vector, eVector):
    g = []
    n = len(A)
    for i in range(n):
        g.append(0)
        for j in range(n):
            g[i] += A[j][i] * base_vector[j]

    count = scalar(base_vector, g) / scalar(eVector, g)
    Y0 = [i - j for i, j in zip(base_vector, [k * count for k in eVector])]
    L0, L1 = 0, 100
    iterates = 0

    while abs(L0-L1) > MAX_PRECISION:
        L0 = L1
        Y1 = Y0.copy()

        Y0 = dot(A, Y1)

        count = scalar(Y0, g) / scalar(eVector, g)
        Y0 = [(j - count*eVector[i]) for i, j in enumerate(Y0)]
        L1 = scalar(Y0, Y1) / scalar(Y1, Y1)

        _norm = norm(Y0)
        Y0 = [i / _norm for i in Y0]

        iterates += 1

    return L1, Y0, iterates


def main():
    with open(input("Input filename: ")) as file:
        n = int(file.readline())
        A = [[float(i)for i in file.readline().split()]for _ in range(n)]
    printer(A)

    print("enter approximation:")
    base = [float(i)for i in input().split()]
    try:
        l0, e0, i0 = max_lambda(A, base)
        l1, e1, i1 = sec_lambda(A, base, e0)
        print("Iteratve method:")
        print("First: ", l0)
        print("E: ", e0, "\nIter: ", i0)
        print("")
        print("Second: ", l1)
        print("E: ", e1, "\nIter: ", i1)
        print("\nMax and min lambda")
    except ValueError:
        print("Does not converge!!!")
    L0 = -9999
    tmp = range(n)
    new_A = [[A[i][j] + L0 if i == j else A[i][j] for j in tmp] for i in tmp]
    Lmin = max_lambda(new_A, base)[0] - L0
    L0 = 9999
    tmp = range(n)
    new_A = [[A[i][j] + L0 if i == j else A[i][j] for j in tmp] for i in tmp]
    Lmax = max_lambda(new_A, base)[0] - L0
    print("Lambda max: ", Lmax, " min: ", round(Lmin, 5))
    print("")
    l = float(input("Enter l:"))
    print("Lambda: ", calcAdjacentEigenValue(A, base, n, l))


if __name__ == '__main__':
    main()
