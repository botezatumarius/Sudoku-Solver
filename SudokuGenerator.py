import random
from ConstraintPropagationWithMRVSolver import ConstraintPropagationWithMRVSolver

class SudokuGenerator:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

    # Generates a fully solvable Sudoku grid
    def generate_solvable_grid(self):
        attempts = 0
        while attempts < 100:  # Limit the number of attempts to generate a grid
            self._fill_grid()  # Fill a complete valid grid
            if self._remove_numbers_while_checking_solubility():  # Try to remove numbers ensuring complete solvability
                return self.grid  # Successfully generated a solvable grid
            attempts += 1
        
        raise Exception("Unable to generate a solvable Sudoku grid after multiple attempts.")

    # Recursively fills the grid with a valid Sudoku solution.
    def _fill_grid(self):
        empty_cell = self._find_empty_location()
        if not empty_cell:
            return True  # Grid is fully filled

        row, col = empty_cell
        numbers = list(range(1, 10))
        random.shuffle(numbers)  # Shuffle to create random valid boards

        for num in numbers:
            if self._is_valid(num, row, col):
                self.grid[row][col] = num
                if self._fill_grid():  
                    return True  # If the board is filled successfully
                self.grid[row][col] = 0  # Undo assignment if it doesn't lead to a solution

        return False  # Trigger backtracking

    # Finds an empty cell in the grid
    def _find_empty_location(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return (row, col)
        return None

    # Randomly removes numbers from the grid while ensuring it remains fully solvable.
    def _remove_numbers_while_checking_solubility(self):
        attempts = 0  
        total_attempts = 0  
        max_removals = 10 # Number of cells to remove 

        while attempts < max_removals and total_attempts < 10:  
            total_attempts += 1  
            row, col = random.randint(0, 8), random.randint(0, 8)
            
            if self.grid[row][col] != 0:  # Only try to remove a number if there is one there
                saved_value = self.grid[row][col]
                self.grid[row][col] = 0  # Remove the number

                if self._can_be_solved():  # Check if the grid remains solvable
                    attempts += 1  # Count as a successful removal
                else:
                    self.grid[row][col] = saved_value  # Restore the value if it's not solvable


        return attempts >= max_removals  

    # Check if the current grid can be fully solved by the constraint propagation and MRV solver
    def _can_be_solved(self):
        solver = ConstraintPropagationWithMRVSolver([row[:] for row in self.grid])  
        solution = solver.solve()
        # Check if all cells are filled
        return all(all(cell != 0 for cell in row) for row in solution) if solution else False

    # Checks if placing a number is valid according to Sudoku rules.
    def _is_valid(self, num, row, col):
        if num in self.grid[row]:
            return False

        for i in range(9):
            if self.grid[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == num:
                    return False

        return True

