from soupsolver.instance import Instance
from soupsolver.solution import Solution
from soupsolver.util import Timer
from bitarray import frozenbitarray
from bitarray.util import count_and
import random
import time

VERSION = {
    "MAJOR": 1,
    "MINOR": 0,
    "PATCH": 0
}

class SoupSolver:
    def __init__(self,
                 in_filename: str,
                 out_filename: str,
                 population_size: int,
                 recombination_rate: float,
                 beta_rank: float,
                 mutation_rate: float,
                 max_generations: int|float,
                 max_non_improving_generations: int|float,
                 seq_non_improving_generations: bool,
                 max_time: int,
                 random_seed: int):
        self.inst = Instance(in_filename)
        self.out_filename = out_filename
        self.population_size = population_size
        self.recombination_rate = recombination_rate
        self.beta_rank = beta_rank
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.max_non_improving_generations = max_non_improving_generations
        self.seq_non_improving_generations = seq_non_improving_generations
        self.max_time = max_time
        
        if random_seed:
            self.random_seed = random_seed
        else:
            self.random_seed = time.time_ns()

        self.rng = random.Random(self.random_seed)
        self.population: list[Solution] = []
        self.best_solution: Solution
        self.non_improving_generations = 0
        self.improved = False
        self.timer = Timer()

        # Stats
        self.avg_population_weight = 0
        self.avg_population_taste = 0
        self.generations = 0
        self.total_non_improving_generations = 0
        self.runtime = 0.0
        self.solved = False

        print(f"SoupSolver v{VERSION['MAJOR']}.{VERSION['MINOR']}.{VERSION['PATCH']}")
        print(f"Instance: {in_filename} - {self.inst}")
        print(f"Output: {self.out_filename}")

    def validate_solution(self, s: Solution) -> bool:
        cand = count_and(self.inst.map, s.map)
        return not bool(cand) and s.W <= self.inst.W
    
    def init_population(self):
        population_map = dict()
        while len(self.population) < self.population_size:
            s = Solution.create_random(self.inst, self.rng)
            fbits = frozenbitarray(s.bits)
            if not population_map.get(fbits):
                self.population.append(s)
                population_map[fbits] = True
        self.best_solution = max(self.population, key=lambda s: s.T)
        self.initial_solution = self.best_solution.copy()

    def select_for_recombination(self) -> list[Solution]:
        # Rank Selection # https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=b61cec42e5aa997a20d563b2886c083b3e0d335c
        n = self.population_size
        beta_rank = self.beta_rank
        alpha_rank = 2 - beta_rank
        rp: list[Solution] = []
        sorted_pop = sorted(self.population, key=lambda s: s.T)
        i = 0
        while len(rp) < 2:
            pRi = (alpha_rank + (i/(n-1))*(beta_rank - alpha_rank))/n
            if self.rng.random() < pRi:
                rp.append(sorted_pop[i])
            i = (i+1) % n
        return rp[0], rp[1]

    def recombination(self, s1: Solution, s2: Solution) -> Solution:
        # Uniform Crossover factibilizado
        ns1 = Solution.create_empty(self.inst, self.rng)
        ns2 = Solution.create_empty(self.inst, self.rng)

        for ing in range(self.inst.N):
            ns1_valid = ns1.get_valid_ingredients()
            ns2_valid = ns2.get_valid_ingredients()
            if self.rng.random() < 0.5:
                if s1.bits[ing] and ns1_valid[ing] and ns1.W + self.inst.w[ing] <= self.inst.W:
                    ns1.add(ing+1)
                if s2.bits[ing] and ns2_valid[ing] and ns2.W + self.inst.w[ing] <= self.inst.W:
                    ns2.add(ing+1)
            else:
                if s2.bits[ing] and ns1_valid[ing] and ns1.W + self.inst.w[ing] <= self.inst.W:
                    ns1.add(ing+1)
                if s1.bits[ing] and ns2_valid[ing] and ns2.W + self.inst.w[ing] <= self.inst.W:
                    ns2.add(ing+1)

        return max(ns1, ns2, key=lambda s: s.T)

    def mutate(self, s: Solution):
        for _ in range(self.inst.N // 10): # TODO: Make sure we get at least one i == 0
            i = s.pick_random_valid_ingredient()
            if i:
                s.add(i)
            else:
                if s.T > self.best_solution.T:
                    self.set_new_best(s)
                i = s.pick_random_ingredient_from_soup()
                s.remove(i)
                i = s.pick_random_valid_ingredient()
                s.add(i)

    def set_new_best(self, s: Solution):
        self.best_solution = s.copy()
        self.improved = True
        print(f"[INFO] New best solution with value {self.best_solution.T} on generation {self.generations} t={self.timer.elapsed_time()}")

    def solve(self):
        print("[INFO] Solving...")
        timer = self.timer
        timer.start() 

        self.init_population()
        gen_time = 0
        non_improving_gens = 0
        while (timer.elapsed_time() + gen_time < self.max_time and 
               non_improving_gens < self.max_non_improving_generations and
               self.generations < self.max_generations):
            
            gen_time = timer.elapsed_time()
            new_population = []
            population_map = dict()
            self.improved = False
            while len(new_population) < self.population_size:
                p1, p2 = self.select_for_recombination()
                if self.rng.random() < self.recombination_rate:
                    f = self.recombination(p1, p2)
                else:
                    f = max(p1, p2, key=lambda s: s.T)
                if self.rng.random() < self.mutation_rate:
                    self.mutate(f)
                if f.T > self.best_solution.T:
                    self.set_new_best(f)
                fbits = frozenbitarray(f.bits)
                if not population_map.get(fbits):
                    new_population.append(f)
                    population_map[fbits] = True

            self.population = new_population
            self.generations += 1
            if not self.improved:
                self.total_non_improving_generations += 1
                self.non_improving_generations += 1
            else:
                self.non_improving_generations = 0
            
            non_improving_gens = self.non_improving_generations if self.seq_non_improving_generations else self.total_non_improving_generations
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
        print(f"max_generations: {self.max_generations}")
        print(f"max_non_improving_generations: {self.max_non_improving_generations}")
        print(f"seq_non_improving_generations: {self.seq_non_improving_generations}")
        print(f"max_time: {self.max_time}")
        print(f"seed: {self.random_seed}")
        # Results
        print(f"initial_solution_value: {self.initial_solution.T}")
        print(f"initial_solution_cost: {self.initial_solution.W}")
        print(f"solution_value: {self.best_solution.T}")
        print(f"solution_cost: {self.best_solution.W}")
        print(f"runtime: {self.runtime}")
        print(f"generations: {self.generations}")
        print(f"total_non_improving_generations: {self.total_non_improving_generations}")
        print("solution_bits:")
        print(self.best_solution.bits.to01())
