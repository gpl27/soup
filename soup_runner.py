import argparse
from soupsolver.solver import SoupSolver

parser = argparse.ArgumentParser(description="Run SoupSolver for a given problem instance.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("instance",
                    help="path to the problem instance",
                    type=str)
parser.add_argument("-p", metavar="POPULATION_SIZE",
                    help="size of the initial population",
                    default=100,
                    type=int)
parser.add_argument("-r", metavar="RECOMBINATION_RATE",
                    help="what percentage of the population should recombine",
                    default=1.0,
                    type=float)
parser.add_argument("-m", metavar="MUTATION_RATE",
                    help="what percentage of the population, after recombination, should mutate",
                    default=1.0,
                    type=float)
parser.add_argument("-f", metavar="FITNESS_RATE",
                    help="f percent of the new population (with size -p) will receive the best solutions, the rest will be randomly sampled",
                    default=0.5,
                    type=float)
parser.add_argument("-g", metavar="GENERATIONS",
                    help="max number of generations where the BKV does not improve before stopping",
                    default=100,
                    type=int)
parser.add_argument("--SEED", metavar="SEED",
                    help="seed for RNG",
                    type=int)
parser.add_argument("-t", metavar="TIME",
                    help="max time",
                    default=300,
                    type=int)

args = parser.parse_args()

solver = SoupSolver(
    args.instance,
    args.p,
    args.r,
    args.m,
    args.f,
    args.g,
    args.SEED,
    args.t
)
solver.solve()
solver.print_info()


