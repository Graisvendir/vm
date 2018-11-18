#!/usr/bin/python3
from numpy import dot, identity, sign
from math import sqrt

# Constats
MAX_PRECISION = 0.000001
MAX_ITER = 1000000


def is_symmetric(A, n):
    """Check matrix is symmetric"""
    for i in range(n):
        for j in range(n):
            if A[i][j] != A[j][i]:
                return False
    return True


def uKL(k, l, a1, b1, size):
    """Get U - matrix of rotation"""
    result = identity(size)
    result[k, k] = result[l, l] = a1
    result[k, l] = -b1
    result[l, k] = b1
    return result


def get_R(A, l, e):
    """Get the discrepancy"""
    return [i-j for i, j in zip(dot(A, e), [k*l for k in e])]


def compare(B):
    for l, i in enumerate(B):
        for k, j in enumerate(i):
            if k == l:
                continue
            elif abs(j) > MAX_PRECISION:
                return False
    return True


def print_vec(V, round_value, delim="\t"):
    """Print vector elements with dilimiter"""
    print(delim.join([str(round(i, round_value))for i in V]))


def printer(A):
    for i in range(len(A)):
        print("\t".join([str(round(k, 10))for k in A[i]]))
    print("")


def main():
    with open(input("Input filename: ")) as file:
        n = int(file.readline())
        A = [[float(i)for i in file.readline().split()]for _ in range(n)]
    printer(A)

    if not is_symmetric(A, n):
        print("Non symmetric!")
        return -1

    iterates = 0
    E = identity(n)
    A_C = A.copy()
    k, l = 0, 1

    while iterates < MAX_ITER:
        maximum = A[0][1]
        for i, x in enumerate(A):
            for j, y in enumerate(x):
                if i != j and abs(y) > abs(maximum):
                    maximum, k, l = y, i, j

        if abs(A[k][k] - A[l][l]) < MAX_PRECISION:
            a = b = sqrt(0.5)
        else:
            nq = 2 * A[k][l] / (A[k][k] - A[l][l])
            temp = 1 / sqrt(1 + nq**2)
            a = sqrt(0.5 * (1 + temp))
            b = sign(nq) * sqrt(0.5 * (1 - temp))

        D = uKL(k, l, a, b, n)
        DT = uKL(k, l, a, b, n)
        DT[k][l], DT[l][k] = b, -b
        B = dot(dot(DT, A), D)

        if compare(B):
            break
        A = B.copy()
        E = dot(E, D)

        iterates += 1

    print("Answer: ")
    [print("Lambda %d: " % i, A[i][i]) for i in range(n)]
    print("\nIterates: ", iterates)

    print("Eigenvectors: ")

    for i in range(n):
        print("Vector %d:" % i)
        e = [E[j][i] for j in range(n)]
        print_vec(e, 10)
        print("Discrepancy:")
        print_vec(get_R(A_C, A[i][i], e), 10)
        print("")


if __name__ == '__main__':
    main()
