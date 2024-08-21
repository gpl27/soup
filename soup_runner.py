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
                    help="population size",
                    default=100,
                    type=int)
parser.add_argument("-r", metavar="RECOMBINATION_RATE",
                    help="what percentage of the population should recombine",
                    default=0.8,
                    type=float)
parser.add_argument("-b", metavar="BETA_RANK",
                    help="selection pressure to be used in Linear Rank Selection for recombination",
                    default=2.0,
                    type=float)
parser.add_argument("-m", metavar="MUTATION_RATE",
                    help="what percentage of the population, after recombination, should mutate",
                    default=0.45,
                    type=float)
parser.add_argument("-g", metavar="GENERATIONS",
                    help="max number of generations",
                    default=float('inf'),
                    type=int)
parser.add_argument("-ng", metavar="NON_IMPROVING_GENERATIONS",
                    help="max number of non improving generations, by default it is the total number of non improving generations",
                    default=float('inf'),
                    type=int)
parser.add_argument("--seq",
                    help="if max non improving generations should be sequential non improving generations",
                    action="store_true")
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
    args.ng,
    args.seq,
    args.t,
    args.s
)
solver.solve()
solver.print_info()


