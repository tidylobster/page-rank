import numpy as np
import pickle

d = 0.85  # dumping factor


def estimate(ranks, siblings, matrix):
    global d
    s = 0
    for i in range(len(siblings)):
        if siblings[i] != 0:
            tmp = matrix[:, i]
            ii = np.where(tmp == 1)
            s += ranks[i] / len(ii[0])
    return (1 - d)/len(ranks) + d * s


def iterate(ranks, matrix):
    response = ranks[:]
    for index in range(len(ranks)):
        response[index] = estimate(ranks, matrix[index], matrix)
    return response


if __name__ == "__main__":
    matrix = np.loadtxt(open("matrix.csv", "r"), delimiter=",")
    with open('legend.txt', 'rb') as fp:
        legend = pickle.load(fp)

    print(legend)
    print(matrix)
    print()

    previous = [1/len(matrix) for i in range(len(matrix))]
    estimated = iterate(previous, matrix)

    j = 1
    pcs = int(input("Decimals: "))
    while not np.array_equal(np.round(previous, pcs), np.round(estimated, pcs)):
        previous = estimated[:]
        estimated = iterate(estimated, matrix)
        j += 1

        if j > 1000: break

    print("--- iterations: %s ---" % j)
    print()
    print(np.round(estimated, pcs))
    print()
    print(legend[estimated.index(max(estimated))])
    print(max(estimated))
    print()
