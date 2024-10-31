from BacktrackingSolver import BacktrackingSolver
from ConstraintPropagationSolver import ConstraintPropagationSolver
from CombinedSolver import CombinedSolver
from ConstraintPropagationWithMRVSolver import ConstraintPropagationWithMRVSolver
from SudokuGenerator import SudokuGenerator


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



generator = SudokuGenerator()
solvable_grid = generator.generate_solvable_grid()

# Print the generated grid
for row in solvable_grid:
    print(row)


solver2 = ConstraintPropagationWithMRVSolver(solvable_grid)
if solver2.solve():
    for row in solvable_grid:
        print("".join(str(num) for num in row))
else:
    print("No solution exists")

