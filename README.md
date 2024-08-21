# SoupSolver
SoupSolver is a genetic algorithm implementation for the 0-1 knapsack problem
with choice restrictions. It was the final project for
[INF5010](https://www.inf.ufrgs.br/~mrpritt/doku.php?id=inf05010:homepage).  A
comparison with GLPK on the instances in `instances/` can be found in sections 7
and 8 of our report `EP20241.pdf` (in Portuguese). The IP formulation used in
GLPK can be found in section 2.

## How to run
Run `python soup_runner.py --help` for information on all parameters.

Example usage:

`python soup_runner.py sep01.dat instances/ep01.dat -r 0.8 -b 2.0 -m 0.45 -p 100 -t 300`
