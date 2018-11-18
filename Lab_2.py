import numpy as np
from math import sqrt


def solve(A, B, n, order=False):
    if order:
        temp = list(range(n))
    else:
        temp = list(range(n))[::-1]
    X = []
    for i in temp:
        if order:
            temp_1 = A[i][:i]
        else:
            temp_1 = A[i][n-len(X):]

        element = ((B[i] - sum(map(lambda x, y: x*y, temp_1, X)))
                   / A[i][i])
        if order:
            X.append(element)
        else:
            X.insert(0, element)
    return X


def printer(A, B, n):
    for i in range(n):
        print("\t".join([str(i)for i in list(map(lambda x: round(x, 4), A[i]))
              + ["|", round(B[i], 4)]]))


def printers(A, n):
    for i in range(n):
        print("\t".join([str(i)for i in map(lambda x: round(x, 4), A[i])]))


def norma(matr, size):
    values = []
    for i in range(size):
        values.append(0)
        for j in range(size):
            values[i] += abs(matr[i][j])
    return max(values)


def gilbert(n):
    h = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            h[i, j] = 1/(i+j+1)
    return norma(h, n)*norma(np.linalg.inv(h), n)


def main():
    with open(input("Input filename: ")) as file:
        n = file.readline()
        n = int(n)
        A = [[float(i)for i in file.readline().split()]for _ in range(n)]
        B = [float(file.readline())for _ in range(n)]
    print("Input:")
    printer(A, B, n)

    for i in range(n):
        for j in range(n):
            if A[i][j] != A[j][i]:
                print("Non symmetric")
                return

    D = [[0.0 for j in range(n)]for i in range(n)]
    S = [[0.0 for j in range(n)]for i in range(n)]
    for i in range(n):
        temp = A[i][i]
        if i != 0:
            temp -= sum([S[l][i]**2 * D[l][l] for l in range(i)])
        D[i][i] = np.sign(temp)
        S[i][i] = sqrt(abs(temp))
        temp = D[i][i] * S[i][i]
        for j in range(i+1, n):
            S[i][j] = (A[i][j] - sum([S[l][i] * S[l][j] * D[l][l]
                                      for l in range(i)])) / temp

    ST = list(np.array(S).transpose())
    temp = np.matmul(np.matmul(np.array(ST), np.array(D)), np.array(S))

    print("")
    print("S:")
    printers(S, n)
    print("")
    print("D:")
    printers(D, n)
    print("")
    print("St:")
    printers(ST, n)
    print("")
    print("StDS:")
    printers(temp, n)

    X = solve(S, solve(D, solve(ST, B, n, True), n), n)
    print("")
    print("Answer:")
    temp = 0
    for i in X:
        print("X%i = %.15f" % (temp, i))
        temp += 1
    print("")
    for i in range(n):
        summ = sum(list(map(lambda x, y: x*y, A[i], X)))
        print("r%i = %.15f" % (temp, B[i] - summ))
        temp += 1

    print("")
    print("Inverse")
    printers(np.linalg.inv(A), n)

    print("")
    print("Hilbert:")
    for i in range(2, 100):
        print("n = %d, cond = %40.15f" % (i, gilbert(i)))


if __name__ == '__main__':
    main()
