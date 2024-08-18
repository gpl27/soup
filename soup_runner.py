import argparse
from soupsolver.solver import SoupSolver

parser = argparse.ArgumentParser(description="Run SoupSolver for a given problem instance.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("output",
                    help="path to output file",
                    type=str)
parser.add_argument("instance",
                    help="path to the problem instance",
                    type=str)
parser.add_argument("-p", metavar="POPULATION_SIZE",
                    help="size of the initial population",
                    default=50,
                    type=int)
parser.add_argument("-r", metavar="RECOMBINATION_RATE",
                    help="what percentage of the population should recombine",
                    default=1.0,
                    type=float)
parser.add_argument("-b", metavar="BETA_RANK",
                    help="selection pressure to be used in Linear Rank Selection for recombination",
                    default=1.5,
                    type=float)
parser.add_argument("-m", metavar="MUTATION_RATE",
                    help="what percentage of the population, after recombination, should mutate",
                    default=1.0,
                    type=float)
parser.add_argument("-g", metavar="GENERATIONS",
                    help="max number of non improving generations",
                    default=float('inf'),
                    type=int)
parser.add_argument("-s", metavar="SEED",
                    help="seed for RNG",
                    type=int)
parser.add_argument("-t", metavar="TIME",
                    help="max time in seconds",
                    default=300,
                    type=int)

args = parser.parse_args()

solver = SoupSolver(
    args.instance,
    args.output,
    args.p,
    args.r,
    args.b,
    args.m,
    args.g,
    args.s,
    args.t
)
solver.solve()
solver.print_info()


