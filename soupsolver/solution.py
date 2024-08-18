from soupsolver.instance import Instance
from bitarray import bitarray
from bitarray.util import count_n
import random

class Solution:
    def __init__(self, bits: bitarray, inst: Instance, rng=random.Random()):
        self.rng = rng
        self.W: int = 0
        self.T: int = 0
        self.N = inst.N
        self.inst = inst
        self.bits = bits
        self.map = bitarray(self.N*self.N)
        assert self.N == len(bits)
        for i in range(self.N):
            if bits[i]:
                self.map[i*self.N:(i+1)*self.N] = bits
                self.map[i*self.N + i] = 0 # Remove identiy
                self.W += self.inst.w[i]
                self.T += self.inst.t[i]

    @staticmethod
    def create_empty(inst: Instance, rng=random.Random()):
        return Solution(bitarray(inst.N), inst, rng)

    @staticmethod
    def create_random(inst: Instance, rng=random.Random()):
        s = Solution.create_empty(inst, rng)
        # Pick random starting ingredient
        s.add(s.rng.randint(1, inst.N))
        # While solution weight < inst.W and there are valid ingredients
        i = s.pick_random_compatible_ingredient()
        while i:
            s.add(i)
            i = s.pick_random_valid_ingredient()
        return s

    def copy(self):
        return Solution(bitarray(self.bits), self.inst)
    
    def add(self, k):
        k = k - 1
        if self.bits[k] == 1:
            return
        self.bits[k] = 1
        for i in range(self.N):
            if self.bits[i]:
                self.map[i*self.N + k] = 1
                self.map[k*self.N + i] = 1
                self.map[i*self.N + i] = 0 # Remove identiy
        self.W += self.inst.w[k]
        self.T += self.inst.t[k]

    def remove(self, k):
        k = k - 1
        if self.bits[k] == 0:
            return
        self.bits[k] = 0
        self.map[k*self.N:(k+1)*self.N] = 0
        for i in range(self.N):
            self.map[i*self.N + k] = 0

        self.W -= self.inst.w[k]
        self.T -= self.inst.t[k]

    def set(self, i, k):
        if k == 0:
            self.remove(i)
        else:
            self.add(i)

    def pick_random_compatible_ingredient(self) -> int:
        valid_ingredients = self.get_valid_ingredients()
        n = valid_ingredients.count(1)
        if n == 0:
            return 0
        rn = self.rng.randint(1,n)
        i = count_n(valid_ingredients, rn)
        return i

    def pick_random_valid_ingredient(self) -> int:
        valid_ingredients = self.get_valid_ingredients()
        n = valid_ingredients.count(1)
        while n:
            rn = self.rng.randint(1,n)
            i = count_n(valid_ingredients, rn)
            if self.W + self.inst.w[i-1] <= self.inst.W:
                return i
            valid_ingredients[i-1] = False
            n -= 1
        return 0
    
    def pick_random_ingredient_from_soup(self) -> int:
        n = self.bits.count(1)
        rn = self.rng.randint(1, n)
        i = count_n(self.bits, rn)
        return i

    def get_valid_ingredients(self) -> bitarray:
        union = bitarray(self.inst.N)
        for j in range(self.inst.N):
            if self.bits[j]:
                union |= self.inst.get_neighbors(j+1)
        union |= self.bits
        union.invert()
        return union

    def __str__(self):
        return self.bits.to01() + f"\nW: {self.W}\nT: {self.T}"
