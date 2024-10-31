from BacktrackingSolver import BacktrackingSolver
from ConstraintPropagationSolver import ConstraintPropagationSolver
from CombinedSolver import CombinedSolver


# Sample input
puzzle = [
    [0, 0, 0, 0, 0, 4, 0, 9, 0],
    [8, 0, 2, 9, 7, 0, 0, 0, 0],
    [9, 0, 1, 2, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 4, 9, 1, 5, 7],
    [0, 1, 3, 0, 5, 0, 9, 2, 0],
    [5, 7, 9, 1, 2, 0, 0, 0, 0],
    [0, 0, 7, 0, 0, 2, 6, 0, 3],
    [0, 0, 0, 0, 3, 8, 2, 0, 5],
    [0, 2, 0, 5, 0, 0, 0, 0, 0]
]


solver = CombinedSolver(puzzle)
if solver.solve():
    for row in puzzle:
        print("".join(str(num) for num in row))
else:
    print("No solution exists")

