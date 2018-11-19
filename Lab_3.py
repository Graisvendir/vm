#!/usr/bin/python3
from math import sqrt
from numpy import linalg


MAX_PRECISION = 0.000000000000001


def printer(A, B, n):
    for i in range(n):
        print(
            "\t".join([
                str(i)for i in list
                    (map(lambda x: round(x, 4), A[i]))
                        + ["|", round(B[i], 4)]
            ])
        )
    print("")


def jacobi(A, B, eps, X = None):
    for i in range(len(A)):
        if (sum(A[i]) - A[i][i]) >= A[i][i]:
            print("Sufficient condition for convergence is not satisfied")
            return False
    X_temp = [0 for i in range(len(A))]
    if X is None:
        X = X_temp.copy()
    iterate = 0
    converge = False
    #
    while not converge:
        for i in range(len(A)):
            X_temp[i] = B[i] / A[i][i] - sum(
                                            A[i][j] / A[i][i] * X[j]
                                            for j in range(len(A))
                                                if j != i
                                        )
        norm = max([ abs(X_temp[i] - X[i]) for i in range(len(A)) ])
        X = X_temp.copy()
        converge = norm <= eps
        iterate += 1
    return X, iterate

def conditionOfConvergence():

    return True


def seidel(A, b, eps):
    n = len(A)
    x = [0 for i in range(n)]
    iterate = 0
    converge = False
    while not converge:
        x_new = x.copy()
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i][i]

        converge = sqrt(sum((x_new[i] - x[i]) ** 2 for i in range(n))) <= eps
        x = x_new
        iterate += 1
    return x, iterate


def main():
    with open("inja") as file:
        n = file.readline()
        n = int(n)
        A = [
            [
                float(i)for i in file.readline().split()
            ]
            for _ in range(n)
        ]
        B = [
            float(file.readline())for _ in range(n)
        ]
    printer(A, B, n)
    print("Jacobi:")

    X = jacobi(A, B, MAX_PRECISION)
    temp = 0
    if X is not False:
        for i in X[0]:
            print("X%i = %.15f" % (temp, i))
            temp += 1
        print("\nIterations: %d\n" % X[1])
        temp = 0
        for i in range(n):
            summ = sum(list(map(lambda x, y: x*y, A[i], X[0])))
            print("r%i = %.15f" % (temp, B[i] - summ))
            temp += 1
    print("\nSeidel:")
    X = seidel(A, B, MAX_PRECISION)
    temp = 0
    for i in X[0]:
        print("X%i = %.15f" % (temp, i))
        temp += 1
    print("\nIterations: %d\n" % X[1])
    temp = 0
    for i in range(n):
        summ = sum(list(map(lambda x, y: x*y, A[i], X[0])))
        print("r%i = %.15f" % (temp, B[i] - summ))
        temp += 1
    print("")


if __name__ == '__main__':
    main()
