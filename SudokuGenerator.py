import random

class SudokuGenerator:
    def __init__(self, solver_class):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solver_class = solver_class

    def generate_and_test(self, clues=30):
        """Generate grids until one is solvable by the provided solver."""
        while True:
            # Generate a fresh board
            self.board = [[0 for _ in range(9)] for _ in range(9)]
            self._fill_diagonal_boxes()
            self._fill_remaining(0, 3)
            self._remove_numbers(81 - clues)

            # Make a copy of the unsolved board to pass to the solver
            unsolved_board = [row[:] for row in self.board]
            solver = self.solver_class(unsolved_board)

            # Check if the board is solvable
            if solver.solve() and self._is_solved(solver.board):
                return self.board  # Return the unsolved grid if solvable

    def _fill_diagonal_boxes(self):
        """Fills the diagonal 3x3 boxes, which don't affect each other."""
        for i in range(0, 9, 3):
            self._fill_box(i, i)

    def _fill_box(self, row, col):
        """Fills a 3x3 box with unique values 1-9."""
        nums = random.sample(range(1, 10), 9)
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = nums.pop()

    def _fill_remaining(self, i, j):
        """Uses backtracking to fill the remaining cells ensuring a valid Sudoku."""
        if i == 9:
            return True
        if j == 9:
            return self._fill_remaining(i + 1, 0)
        if self.board[i][j] != 0:
            return self._fill_remaining(i, j + 1)

        for num in random.sample(range(1, 10), 9):
            if self._is_safe(num, i, j):
                self.board[i][j] = num
                if self._fill_remaining(i, j + 1):
                    return True
                self.board[i][j] = 0  # Backtrack
        return False

    def _is_safe(self, num, row, col):
        """Checks if it's safe to place a number in a specific cell."""
        if num in self.board[row]:
            return False
        if num in [self.board[r][col] for r in range(9)]:
            return False
        box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_start_row, box_start_row + 3):
            for j in range(box_start_col, box_start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def _remove_numbers(self, num_cells):
        """Removes a specified number of cells to create a puzzle."""
        count = num_cells
        while count > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count -= 1

    def _is_solved(self, board):
        """Check if the board is completely solved (no empty cells)."""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return False
        return True
