from __future__ import division
import numpy as np
import pickle
from collections import OrderedDict
from page_rank.compress import SparseMatrix
from functools import reduce
from pprint import pprint

d1 = 0.85  # dumping factor


def estimate(ranks, siblings, matrix):
    global d_factor
    s = 0
    for i in range(len(siblings)):
        if siblings[i] != 0:
            tmp = matrix[:, i]
            i_line = np.where(tmp == 1)
            i_line = 1 if not len(i_line[0]) else i_line[0]
            s += ranks[i] / i_line
    return (1 - d1) / len(ranks) + d1 * s


def power_estimate(matrix, ranks):
    return np.transpose(matrix).dot(ranks)


def iterate(ranks, matrix, n):
    if n == 1:
        response = ranks[:]
        for index in range(len(ranks)):
            response[index] = estimate(ranks, matrix[index], matrix)
    else:
        return power_estimate(matrix, ranks)
    return response


def rebuild(matrix):
    rebuilded = np.zeros((len(matrix), len(matrix)))
    for k in range(len(matrix)):
        deg = sum(matrix[k, :])
        if deg == 0:
            rebuilded[k] = [1/len(matrix) for _ in range(len(matrix))]
        else:
            row = matrix[k, :]
            for j in range(len(row)):
                rebuilded[k][j] = (1 / len(matrix)) if row[j] != 0 else 0
    return rebuilded


def build_row(*row):
    arr = np.zeros((1, len(row)))
    for w in range(len(row)):
        arr[0, w] = row[w]
    return arr


if __name__ == "__main__":
    with open('data\\legend.txt', 'rb') as fp:
        legend = pickle.load(fp)
    with open('data\\matrix.txt', 'rb') as fp:
        smatrix = pickle.load(fp)

    previous1 = [1 / len(smatrix) for i in range(len(smatrix))]
    estimated1 = iterate(previous1, smatrix, 1)

    for i in range(10):
        previous1 = estimated1[:]
        estimated1 = iterate(estimated1, smatrix, 1)
        print(estimated1)

    print(legend[estimated1.index(max(estimated1))])
    print(max(estimated1))
    print()

    z1 = (zip(estimated1, legend))
    d_factor = OrderedDict()
    for pair in z1:
        d_factor.setdefault(pair[0], []).append(pair[1])
    for item in sorted(d_factor)[::-1]:
        for k in d_factor[item]:
            print(item, k)
