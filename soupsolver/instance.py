from bitarray import bitarray

class Instance:
    """
        self.t
        self.w
        self.i
        self.map
        self.cmap
    """
    def __init__(self, filename: str):
        self.t: list[int] = []
        self.w: list[int] = []
        self.i: list[tuple[int, int]] = []
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
            self.map[j*self.N + k] = 1
            self.map[k*self.N + j] = 1
        self.cmap = ~self.map

    def check(self, i, j) -> bool:
        return bool(self.map[(i-1)*self.N + (j-1)])
    
    def get_neighbors(self, i) -> int:
        return self.map[(i-1)*self.N:i*self.N]
