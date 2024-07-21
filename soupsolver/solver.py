from soupsolver.instance import Instance
from soupsolver.solution import Solution
from soupsolver.util import Timer
from bitarray import bitarray
from bitarray.util import count_and, zeros
import random

# IDEA: Keep a hashtable of seen solutions

class SoupSolver:
    def __init__(self,
                 filename: str,
                 population_size: int,
                 recombination_rate: float,
                 mutation_rate: float,
                 fitness_selection_rate: float,
                 max_non_improving_generation: int,
                 random_seed: int,
                 max_time: int):
        self.inst = Instance(filename)
        self.population_size = population_size
        self.recombination_rate = recombination_rate
        self.mutation_rate = mutation_rate
        self.fitness_selection_rate = fitness_selection_rate
        self.max_non_improving_generations = max_non_improving_generation
        self.max_time = max_time
        self.random_seed = random_seed

        if random_seed:
            random.seed(random_seed)

        self.population: list[Solution] = []
        self.best_solution: Solution
        self.non_improving_generations = 0

        # Stats
        self.avg_population_weight = 0
        self.avg_population_taste = 0
        self.generations = 0
        self.total_non_improving_generations = 0
        self.runtime = 0.0
        self.solved = False

        print("SoupSolver v0.0.1")
        print(f"Instance: {filename} - {self.inst}")

    def validate_solution(self, s: Solution) -> bool:
        cand = count_and(self.inst.map, s.map)
        return not bool(cand) and s.W <= self.inst.W
    
    def init_population(self):
        while len(self.population) < self.population_size:
            s = Solution.create_random(self.inst)
            self.population.append(s)
        self.best_solution = max(self.population, key=lambda s: s.T)

    def select_for_recombination(self) -> list[Solution]:
        n = int(len(self.population) * self.recombination_rate)
        return random.sample(self.population, n)

    def select_for_mutation(self) -> list[Solution]:
        n = int(len(self.population) * self.mutation_rate)
        return random.sample(self.population, n)

    def recombination(self, p: list[Solution]):
        # Simple Crossover
        for i in range(len(p)):
            j = i + 1 if i + 1 < len(p) else 0
            s1 = p[i]
            s2 = p[j]
            k = random.randint(1, self.inst.N - 1)

            tmp = s1.bits[:k]
            tmp.extend(zeros(self.inst.N - k))
            c1s1 = Solution(tmp, self.inst)
            tmp = zeros(k)
            tmp.extend(s1.bits[k:])
            c2s1 = Solution(tmp, self.inst)

            tmp = s2.bits[:k]
            tmp.extend(zeros(self.inst.N - k))
            c1s2 = Solution(tmp, self.inst)
            tmp = zeros(k)
            tmp.extend(s2.bits[k:])
            c2s2 = Solution(tmp, self.inst)

            ns1 = Solution(c1s1.bits | (c1s1.get_valid_ingredients() & c2s2.bits), self.inst)
            ns2 = Solution(c1s2.bits | (c1s2.get_valid_ingredients() & c2s1.bits), self.inst)
            if self.validate_solution(ns1):
                self.population.append(ns1)
            if self.validate_solution(ns2):
                self.population.append(ns2)

    def mutate(self, p: list[Solution]):
        for s in p:
            i = s.pick_random_valid_ingredient()
            if i:
                s.add(i)
            else:
                i = s.pick_random_ingredient_from_soup()
                s.remove(i)

    def select_new_population(self):
        k = int(self.population_size * self.fitness_selection_rate)
        sortedpop = sorted(self.population, key=lambda s: s.T, reverse=True)
        toppop = sortedpop[:k]
        samplepop = random.sample(sortedpop[k:], self.population_size - k)
        smax = toppop[0]
        npop = toppop + samplepop
        if smax.T <= self.best_solution.T:
            self.non_improving_generations += 1
            self.total_non_improving_generations += 1
        else:
            self.best_solution = smax
            self.non_improving_generations = 0
        self.population = npop

    def solve(self):
        print("Solving...")
        timer = Timer()
        timer.start()

        self.init_population()
        while (timer.elapsed_time() < self.max_time and 
               self.non_improving_generations < self.max_non_improving_generations):

            p = self.select_for_recombination()
            self.recombination(p)
            p = self.select_for_mutation()
            self.mutate(p)
            self.generations += 1
            self.select_new_population()

        self.runtime = timer.stop()
        self.solved = True
        print("Done.")

    def print_info(self):
        if not self.solved:
            return
        print("[INFO]")
        # Parameters
        print(f"population_size: {self.population_size}")
        print(f"recombination_rate: {self.recombination_rate}")
        print(f"mutation_rate: {self.mutation_rate}")
        print(f"fitness_selection_rate: {self.fitness_selection_rate}")
        print(f"max_non_improving_generations: {self.max_non_improving_generations}")
        print(f"max_time: {self.max_time}")
        if self.random_seed:
            print(f"seed: {self.random_seed}")
        # Results
        print(f"solution_value: {self.best_solution.T}")
        print(f"solution_cost: {self.best_solution.W}")
        print(f"runtime: {self.runtime}")
        print(f"generations: {self.generations}")
        print(f"non_improving_generations: {self.total_non_improving_generations}")
        pass