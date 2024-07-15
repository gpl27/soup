from soupsolver.instance import Instance
from bitarray import bitarray

class Solution:
    def __init__(self, bits: bitarray, inst: Instance):
        self.W = 0
        self.T = 0
        self.N = inst.N
        self.inst = inst
        self.bits = bits
        self.map = bitarray(self.N*self.N)
        for i in range(self.N):
            if bits[i]:
                self.map[i*self.N:(i+1)*self.N] = bits
                self.map[i*self.N + i] = 0 # Remove identiy
                self.W += self.inst.w[i]
                self.T += self.inst.t[i]

    @staticmethod
    def create_empty(inst: Instance):
        return Solution(bitarray(inst.N), inst)

    @staticmethod
    def create_random(inst: Instance):
        pass
    
    def add(self, k):
        k = k - 1
        self.bits[k] = 1
        for i in range(self.N):
            if self.bits[i]:
                self.map[i*self.N + k] = 1
                self.map[k*self.N + i] = 1
                self.map[i*self.N + i] = 0 # Remove identiy
        self.W += self.inst.w[k]
        self.T += self.inst.t[k]

    def __str__(self):
        return self.bits.to01() + f"\nW: {self.W}\nT: {self.T}"
