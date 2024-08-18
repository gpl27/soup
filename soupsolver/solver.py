from soupsolver.instance import Instance
from soupsolver.solution import Solution
from soupsolver.util import Timer
from bitarray import bitarray, frozenbitarray
from bitarray.util import count_and, zeros, urandom
import random
import time

VERSION = {
    "MAJOR": 0,
    "MINOR": 0,
    "PATCH": 1
}

class SoupSolver:
    def __init__(self,
                 filename: str,
                 out_filename: str,
                 population_size: int,
                 recombination_rate: float,
                 beta_rank: float,
                 mutation_rate: float,
                 max_non_improving_generations: int|float,
                 random_seed: int,
                 max_time: int):
        self.inst = Instance(filename)
        self.out_filename = out_filename
        self.population_size = population_size
        self.recombination_rate = recombination_rate
        self.beta_rank = beta_rank
        self.mutation_rate = mutation_rate
        self.max_non_improving_generations = max_non_improving_generations
        self.max_time = max_time
        
        if random_seed:
            self.random_seed = random_seed
        else:
            self.random_seed = time.time_ns()

        self.rng = random.Random(self.random_seed)
        self.population: list[Solution] = []
        self.new_population: list[Solution] = []
        self.best_solution: Solution
        self.non_improving_generations = 0

        # Stats
        self.avg_population_weight = 0
        self.avg_population_taste = 0
        self.generations = 0
        self.total_non_improving_generations = 0
        self.runtime = 0.0
        self.solved = False

        print(f"SoupSolver v{VERSION['MAJOR']}.{VERSION['MINOR']}.{VERSION['PATCH']}")
        print(f"Instance: {filename} - {self.inst}")
        print(f"Output: {self.out_filename}")

    def validate_solution(self, s: Solution) -> bool:
        cand = count_and(self.inst.map, s.map)
        return not bool(cand) and s.W <= self.inst.W
    
    def init_population(self):
        while len(self.population) < self.population_size:
            s = Solution.create_random(self.inst, self.rng)
            self.population.append(s)
        self.best_solution = max(self.population, key=lambda s: s.T)
        self.initial_solution = self.best_solution.copy()

    def select_for_recombination(self) -> list[Solution]:
        # Rank Selection
        # https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=b61cec42e5aa997a20d563b2886c083b3e0d335c
        n = self.population_size
        rn = int(n * self.recombination_rate)
        beta_rank = self.beta_rank
        alpha_rank = 2 - beta_rank
        rp: list[Solution] = []
        sorted_pop = sorted(self.population, key=lambda s: s.T)
        i = 0
        while len(rp) < rn:
            pRi = (alpha_rank + (i/(n-1))*(beta_rank - alpha_rank))/n
            if self.rng.random() < pRi:
                rp.append(sorted_pop[i])
            i = (i+1) % n
        return rp

    def select_for_mutation(self) -> list[Solution]:
        n = int(len(self.new_population) * self.mutation_rate)
        return self.rng.sample(self.new_population, n)

    def recombination(self, p: list[Solution]):
        # Uniform Crossover
        for i in range(len(p)):
            j = i + 1 if i + 1 < len(p) else 0
            s1 = p[i]
            s2 = p[j]
            ns1 = Solution.create_empty(self.inst, self.rng)
            ns2 = Solution.create_empty(self.inst, self.rng)

            for ing in range(self.inst.N):
                ns1_valid = ns1.get_valid_ingredients()
                ns2_valid = ns2.get_valid_ingredients()
                if self.rng.random() < 0.5:
                    if ns1_valid[ing]:
                        ns1.set(ing+1, s1.bits[ing])
                    if ns2_valid[ing]:
                        ns2.set(ing+1, s2.bits[ing])
                else:
                    if ns1_valid[ing]:
                        ns1.set(ing+1, s2.bits[ing])
                    if ns2_valid[ing]:
                        ns2.set(ing+1, s1.bits[ing])

            if self.validate_solution(ns1):
                self.new_population.append(ns1)
            if self.validate_solution(ns2):
                self.new_population.append(ns2)

    def mutate(self, p: list[Solution]):
        new_best: list[Solution] = []
        for s in p:
            for _ in range(self.inst.N // 10): # Make sure we get at least one i == 0
                i = s.pick_random_valid_ingredient()
                if i:
                    s.add(i)
                else:
                    if s.T > self.best_solution.T:
                        new_best.append(s.copy())
                    i = s.pick_random_ingredient_from_soup()
                    s.remove(i)
                    i = s.pick_random_valid_ingredient()
                    s.add(i)
        p += new_best

    def select_new_population(self):
        total_pop = self.population + self.new_population
        smax = max(total_pop, key=lambda s: s.T)
        if smax.T > self.best_solution.T:
            self.best_solution = smax.copy()
            self.non_improving_generations = 0
            print(f"[INFO] New best solution with value {self.best_solution.T} on generation {self.generations}")
        else:
            self.non_improving_generations += 1
            self.total_non_improving_generations += 1
        sorted_pop = sorted(total_pop, key=lambda s: s.T, reverse=True)
        self.population = []
        population_map = dict()
        i = 0
        while len(self.population) < self.population_size:
            s = sorted_pop[i]
            fbits = frozenbitarray(s.bits)
            if not population_map.get(fbits):
                population_map[fbits] = True
                self.population.append(s)
            i = (i + 1) % len(sorted_pop)

    def solve(self):
        print("[INFO] Solving...")
        timer = Timer()
        timer.start()

        self.init_population()
        gen_time = 0
        while (timer.elapsed_time() + gen_time < self.max_time and 
               self.non_improving_generations < self.max_non_improving_generations):
            gen_time = timer.elapsed_time()
            self.new_population = []
            rp = self.select_for_recombination()
            self.recombination(rp)
            mp = self.select_for_mutation()
            self.mutate(mp)
            self.select_new_population()
            self.generations += 1
            gen_time = timer.elapsed_time() - gen_time

        self.runtime = timer.stop()
        self.solved = True
        with open(self.out_filename, "w") as f:
            f.write(self.best_solution.bits.to01())
        print("[INFO] Done.")

    def print_info(self):
        if not self.solved:
            return
        print("[INFO] Results")
        # Parameters
        print(f"population_size: {self.population_size}")
        print(f"recombination_rate: {self.recombination_rate}")
        print(f"beta_rank: {self.beta_rank}")
        print(f"mutation_rate: {self.mutation_rate}")
        print(f"max_non_improving_generations: {self.max_non_improving_generations}")
        print(f"max_time: {self.max_time}")
        print(f"seed: {self.random_seed}")
        # Results
        print(f"initial_solution_value: {self.initial_solution.T}")
        print(f"initial_solution_cost: {self.initial_solution.W}")
        print(f"solution_value: {self.best_solution.T}")
        print(f"solution_cost: {self.best_solution.W}")
        print(f"runtime: {self.runtime}")
        print(f"generations: {self.generations}")
        print(f"non_improving_generations: {self.total_non_improving_generations}")
        print("solution_bits:")
        print(self.best_solution.bits.to01())
