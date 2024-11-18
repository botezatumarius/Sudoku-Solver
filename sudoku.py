import argparse
from BacktrackingSolver import BacktrackingSolver
from ConstraintPropagationSolver import ConstraintPropagationSolver
from ConstraintPropagationWithMRVSolver import ConstraintPropagationWithMRVSolver
from SudokuGenerator import SudokuGenerator
from AC3Solver import AC3Solver

def is_valid_sudoku(grid):
    """
    Validates whether the given Sudoku grid satisfies all Sudoku rules.
    """
    def is_unique(block):
        """Helper function to check if all non-zero numbers in a block are unique."""
        nums = [num for num in block if num != 0]
        return len(nums) == len(set(nums))

    # Check all rows
    for row in grid:
        if not is_unique(row):
            return False

    # Check all columns
    for col in range(9):
        if not is_unique([grid[row][col] for row in range(9)]):
            return False

    # Check all 3x3 sub-grids
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = [
                grid[row][col]
                for row in range(box_row, box_row + 3)
                for col in range(box_col, box_col + 3)
            ]
            if not is_unique(box):
                return False

    return True

def main():
    parser = argparse.ArgumentParser(description="Solve Sudoku using a specified solver.")
    parser.add_argument(
        "solver",
        choices=["Backtracking", "ConstraintPropagation", "ConstraintPropagationWithMRV", "AC3"],
        help="The Sudoku solver to use.",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate a new Sudoku grid instead of using a predefined puzzle.",
    )
    args = parser.parse_args()

    # Map the string argument to the corresponding solver class
    solver_classes = {
        "Backtracking": BacktrackingSolver,
        "ConstraintPropagation": ConstraintPropagationSolver,
        "ConstraintPropagationWithMRV": ConstraintPropagationWithMRVSolver,
        "AC3": AC3Solver,
    }

    # Get the solver class based on the first argument
    solver_class = solver_classes[args.solver]

    # Generate or use a predefined grid
    if args.generate:
        print(f"Generating a new Sudoku puzzle using {args.solver} solver...")
        generator = SudokuGenerator(solver_class)
        puzzle = generator.generate_and_test(clues=30)
        for row in puzzle:
            print(" ".join(map(str, row)))
    else:
        print("Using a predefined puzzle...")
        puzzle = [
            [0, 0, 0, 0, 0, 4, 0, 9, 0],
            [8, 0, 2, 9, 7, 0, 0, 0, 0],
            [9, 0, 1, 2, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 4, 9, 1, 5, 7],
            [0, 1, 3, 0, 5, 0, 9, 2, 0],
            [5, 7, 9, 1, 2, 0, 0, 0, 0],
            [0, 0, 7, 0, 0, 2, 6, 0, 3],
            [0, 0, 0, 0, 3, 8, 2, 0, 5],
            [0, 2, 0, 5, 0, 0, 0, 0, 0],
        ]

    # Solve the puzzle
    solver = solver_class(puzzle)

    if solver.solve():
        print("Solved puzzle:")
        for row in puzzle:
            print(" ".join(map(str, row)))
    else:
        print("Puzzle could not be solved.")

if __name__ == "__main__":
    main()
