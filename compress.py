import numpy as np
import time


class SparseMatrix:
    def __init__(self, matrix):
        self.a = [j for i in matrix for j in i if j != 0]
        self.lj = [j for i in matrix for j in range(len(i)) if i[j] != 0]
        self.li = self._packing(matrix)
        self._n = len(matrix)
        self._m = len(matrix[0])

    def __getitem__(self, tt):
        searched = 0
        i, j = tt
        n1 = int(self.li[i])
        n2 = int(self.li[i + 1])
        for k in range(n1, n2):
            if self.lj[k] == j:
                searched = self.a[k]
                break
        return int(searched)

    def __len__(self):
        return self._n

    def __repr__(self):
        s = ""
        # for i in range(len(self)):
        #     for j in range(len(self)):
        #         s += str(self[i, j]) + ' '
        #     s += '\n'
        s += 'a' + str(self.a) + '\n'
        s += 'i' + str(self.li) + '\n'
        s += 'j' + str(self.lj) + '\n'
        return s

    def _packing(self, matrix):
        response = []
        counter = 0
        for i in range(len(matrix)):
            s = sum(matrix[i])
            if s == 0:
                response.append(counter)
                continue
            for j in range(len(matrix[i])):
                if matrix[i][j] != 0:
                    response.append(counter)
                    break
            counter += s
        response.append(counter)
        return response


if __name__ == "__main__":
    n, m = 5, 5
    matrix = np.zeros((n, m))

    for _ in range(np.random.randint(m)):
        y, z = np.random.randint(m, size=2)
        matrix[y, z] = 1

    print(matrix)

    time.sleep(1)
    smatrix = SparseMatrix(matrix)
    for i in range(len(smatrix)):
        for j in range(len(smatrix)):
            print(smatrix[i, j], end=' ')
        print()
