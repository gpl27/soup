from bitarray.util import *
from bitarray import *
# TODO: Where should this go?? Need to fix circular import
# from soupsolver.solution import Solution 

class Instance:
    def __init__(self, filename: str):
        self.t: list[int] = []
        self.w: list[int] = []
        self.i: list[tuple[int, int]] = []
        self.ibits: list[bitarray] = []
        with open(filename) as f:
            [N, I, W] = f.readline().strip().split(' ')
            self.N = int(N)
            self.I = int(I)
            self.W = int(W)
            f.readline()
            # Le os sabores t
            line = f.readline().strip()
            while line:
                self.t += map(lambda x: int(x), line.split(' '))
                line = f.readline().strip()
            # Le os pesos w
            line = f.readline().strip()
            while line:
                self.w += map(lambda x: int(x), line.split(' '))
                line = f.readline().strip()
            # Le as incompatibilidades
            line = f.readline().strip()
            while line:
                self.i.append(tuple(map(lambda x: int(x), line.split(' '))))
                line = f.readline().strip()
        self.map = bitarray(self.N * self.N)
        for i in self.i:
            j = i[0]-1
            k = i[1] - 1
            tmp = bitarray(self.N)
            tmp[j] = 1
            tmp[k] = 1
            self.map[j*self.N + k] = 1
            self.map[k*self.N + j] = 1
            self.ibits.append(tmp)
        self.cmap = ~self.map

    def validate_solution(self, s) -> bool:
        return not bool(count_and(self.map, s.map)) and s.W <= self.W

    def is_incompatible_solution(self, s) -> bool:
        return not bool(count_and(self.map, s.map))

    def check(self, i, j) -> bool:
        return bool(self.map[(i-1)*self.N + (j-1)])
    
    def get_neighbors(self, i) -> int:
        return self.map[(i-1)*self.N:i*self.N]
