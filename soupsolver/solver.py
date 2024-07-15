from soupsolver.instance import Instance
from soupsolver.solution import Solution
from soupsolver.util import Timer
from bitarray import bitarray
from bitarray.util import count_and
import time

class SoupSolver:
    def __init__(self, filename: str, l: int):
        self.inst = Instance(filename)
        self.population_size = 200
        self.recombination_rate = 0.2
        self.mutation_rate = 0.1
        self.max_non_improving_generations = 100
        self.max_time = 600
        self.random_seed = 27

        self.population: list[Solution] = []
        self.best_solution: Solution
        self.non_improving_generations = 0

    def validate_solution(self, s: Solution) -> bool:
        return not bool(count_and(self.map, s.map)) and s.W <= self.W
    
    def get_valid_ingredients(self, s: Solution) -> bitarray:
        union = bitarray(self.inst.N)
        for j in range(self.inst.N):
            if s.bits[j]:
                union |= self.inst.get_neighbors(j+1)
        union |= s.bits
        union.invert()

    def init_population(self):
        pass

    def select_for_recombination(self) -> list[Solution]:
        pass

    def recombination(self, p: list[Solution]) -> list[Solution]:
        pass

    def select_new_population(self):
        pass

    def solve(self):
        timer = Timer()
        timer.start()

        self.init_population()

        while (timer.elapsed_time() < self.max_time and 
               self.non_improving_generations < self.max_non_improving_generations):

            p = self.select_for_recombination()
            n = self.recombination(p)
            self.population += n
            self.select_new_population()

        runtime = timer.stop()
