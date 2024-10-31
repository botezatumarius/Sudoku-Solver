class BacktrackingSolver:
    def __init__(self, board):
        self.board = board

    def solve(self):
        return self._solve_sudoku()

    def _solve_sudoku(self):
        empty_cell = self._find_empty()
        if not empty_cell:
            return True  # Puzzle solved

        row, col = empty_cell

        for num in range(1, 10):
            if self._is_valid(num, row, col):
                self.board[row][col] = num

                if self._solve_sudoku():
                    return True

                self.board[row][col] = 0  # Backtrack

        return False
    
    # Search for an empty cell (represented by 0) in the Sudoku board.
    def _find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return (row, col)
        return None

    # Check if 'num' can be placed in the specified (row, col).
    def _is_valid(self, num, row, col):
        # Check row
        if num in self.board[row]:
            return False

        # Check column
        if num in [self.board[i][col] for i in range(9)]:
            return False

        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False

        return True