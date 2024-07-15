import time
from soupsolver.instance import Instance
from soupsolver.solution import Solution
from bitarray import *
from bitarray.util import *


ep01 = Instance("./instances/ep01.dat")
time_s = time.time_ns()
union = bitarray(ep01.N)
for i in range(500):
    union |= ep01.get_neighbors(i+1)
union.invert()
time_e = time.time_ns()
print(f"Time to check for mutually inclusive ingredients: {(time_e-time_s)/1000000}ms")

s = Solution.create_empty(ep01)
s.add(1)
time_s = time.time_ns()
union = bitarray(ep01.N)
for j in range(ep01.N):
    if s.bits[j]:
        union |= ep01.get_neighbors(j+1)
union |= s.bits
union.invert()
time_e = time.time_ns()
print(f"Time to find all valid ingredients to add to a solution: {(time_e-time_s)/1000000}ms")


# Benchmarks
time_s = time.time_ns()
valid = ep01.validate_solution(s)
time_e = time.time_ns()
print(f"Time to validate solution: {(time_e-time_s)/1000000}ms")
time_s = time.time_ns()
s.add(5)
time_e = time.time_ns()
print(f"Time to add 1 ingredient: {(time_e-time_s)/1000000}ms")
print(s)
