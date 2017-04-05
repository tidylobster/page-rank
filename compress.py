

class SparseMatrix:
    def __init__(self, matrix):
        self.a = [j for i in matrix for j in i if j != 0]
        self.lj = [j for i in matrix for j in range(len(i)) if i[j] != 0]
        self.li = [i for i in range(len(matrix)) for j in range(len(matrix[i])) if matrix[i][j] != 0]
        self._n = len(matrix)

    def __getitem__(self, tt):
        if not isinstance(tt, tuple):
            return self[tt, :]
        ii, jj = tt
        searched = .0

        if isinstance(ii, slice):
            resp1 = []
            for i in range(self._n):
                if ii.start is not None and i < ii.start:
                    continue
                if ii.start is not None and i >= ii.stop:
                    break
                resp1.append(self[i, jj])
            return resp1

        if isinstance(jj, slice):
            resp2 = []
            for j in range(self._n):
                if jj.start is not None and j < jj.start:
                    continue
                if jj.start is not None and j >= jj.stop:
                    break
                resp2.append(self[ii, j])
            return resp2

        for i in range(len(self.li)):
            if ii == self.li[i] and jj == self.lj[i]:
                searched = float(self.a[i])
                break
        return searched

    def __len__(self):
        return self._n

    def __repr__(self):
        s = ""
        for i in range(len(self)):
            for j in range(len(self)):
                s += str(self[i, j]) + ' '
            s += '\n'
        # s += 'a' + str(self.a) + '\n'
        # s += 'i' + str(self.li) + '\n'
        # s += 'j' + str(self.lj) + '\n'
        return s
