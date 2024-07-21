from soupsolver.solver import SoupSolver

solver = SoupSolver("./instances/ep01.dat")

solver.solve()

print(f"Runtime: {solver.runtime}s")
print(f"Generations: {solver.generations}")
print(f"Nonimproving: {solver.total_non_improving_generations}")
print(solver.best_solution)

