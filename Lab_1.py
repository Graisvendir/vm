from functools import reduce


def solve(A, B, n):
    X = []
    for i in list(range(n))[::-1]:
        element = ((B[i] - sum(map(lambda x, y: x*y, A[i][n-len(X):], X)))
                   / A[i][i])
        X.insert(0, element)
    return X


def norma(matr, size):
    values = []
    for i in range(size):
        values.append(0)
        for j in range(size):
            values[i] += abs(matr[i][j])
    return max(values)


def main():
    with open(input("Input filename: ")) as file:
        n = int(file.readline())
        A = [[float(i)for i in file.readline().split()]for _ in range(n)]
        B = [float(file.readline())for _ in range(n)]
    A_c = A.copy()
    B_c = B.copy()
    for i in range(n):
        print("\t".join([str(i)for i in A[i]+["|", B[i]]]))

    sign = 1
    for i in range(n-1):
        ai = [a[i] for a in A]
        try:
            temp = ai.index(max(map(abs, ai[i:])))
        except ValueError:
            temp = ai.index(-max(map(abs, ai[i:])))
        if temp > i:
            A.insert(i, A.pop(temp))
            B.insert(i, B.pop(temp))
            ai = [a[i] for a in A]
            sign *= -1
        for j in range(i+1, n):
            try:
                u = ai[j]/ai[i]
            except ZeroDivisionError:
                u = 0
            B[j] = B[j] - B[i]*u
            A[j] = list(map(lambda x, y: x-y, A[j], map(lambda x: u*x, A[i])))

    print("\nTriangle view")
    for i in range(n):
        print("\t".join([str(i)for i in list(map(lambda x: round(x, 4), A[i]))
              + ["|", round(B[i], 4)]]))

    determinant = reduce(lambda x, y: x*y, [A[i][i]for i in range(n)])*sign

    if determinant == 0:
        print("Degenerate system")
        return

    X = solve(A, B, n)
    temp = 0
    print("\nAnswer:")
    for i in X:
        print("X%i = %.3f" % (temp, i))
        temp += 1
    temp = 0
    print()
    reverse = []
    for i in range(n):
        summ = sum(list(map(lambda x, y: x*y, A_c[i], X)))
        print("r%i = %.3f" % (temp, B_c[i] - summ))
        temp += 1
        reverse.append([])

    print("\nDeterminant = %i" % determinant)
    print("\nInverse matrix:")
    for i in range(n):
        spec_B = list(map(int, list("0"*n)))
        spec_B[i] = 1
        temp = solve(A, spec_B, n)
        for j in range(n):
            reverse[j].append(temp[j])
    for i in range(n):
        print("\t".join([str(round(i, 4))for i in reverse[i]]))

    print("\nCond = %.4f" % (norma(A_c, n)*norma(reverse, n)))


if __name__ == '__main__':
    main()
