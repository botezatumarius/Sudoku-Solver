# Combines the backtracking approach with constraint propagation and forward checking
class CombinedSolver:
    def __init__(self, board):
        self.board = board
        self.domains = self._initialize_domains()

    def solve(self):
        # Apply constraint propagation to reduce domains
        if not self._constraint_propagate():
            return False  # If we find an inconsistency in the initial setup

        return self._solve_sudoku()

    def _initialize_domains(self):
        domains = {}
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    domains[(row, col)] = set(range(1, 10))  # Possible values 1-9
                else:
                    domains[(row, col)] = {self.board[row][col]}  # Only one possible value
        return domains

    # Reduce the domains of the cells based on current values.
    def _constraint_propagate(self):
        changed = True
        while changed:
            changed = False
            for (row, col), domain in self.domains.items():
                if len(domain) == 1:
                    value = next(iter(domain))  # Get the single value in the domain
                    for neighbor in self._get_neighbors(row, col):
                        if value in self.domains[neighbor]:
                            self.domains[neighbor].remove(value)  # Remove the value from neighbor's domain
                            changed = True
                            if len(self.domains[neighbor]) == 0:
                                return False  # Conflict: empty domain found
        return True

    def _get_neighbors(self, row, col):
        neighbors = set()
        
        # Add cells in the same row and column
        for i in range(9):
            if (row, i) != (row, col):
                neighbors.add((row, i))  # Row neighbors
            if (i, col) != (row, col):
                neighbors.add((i, col))  # Column neighbors

        # Add cells in the same 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r, c) != (row, col):
                    neighbors.add((r, c))

        return neighbors

    def _solve_sudoku(self):
        empty_cell = self._find_empty()
        if not empty_cell:
            return True  # Puzzle solved

        row, col = empty_cell

        for num in range(1, 10):
            if self._is_valid(num, row, col):
                self.board[row][col] = num
                original_domains = self._save_domains()  # Save current state of domains
                self.domains[(row, col)] = {num}  # Update the domain for the filled cell

                # Forward Checking: Eliminate the assigned value from neighbors' domains
                if self._forward_check(num, row, col):
                    if self._solve_sudoku():
                        return True

                # Backtrack
                self.board[row][col] = 0  # Reset the cell
                self.restore_domains(original_domains)  # Restore the previous state of domains

        return False

    # Eliminate the assigned value from the domains of neighboring cells.
    def _forward_check(self, num, row, col):
        for neighbor in self._get_neighbors(row, col):
            if num in self.domains[neighbor]:
                self.domains[neighbor].remove(num)  # Remove the value from neighbor's domain
                if len(self.domains[neighbor]) == 0:
                    return False  # Conflict: empty domain found
        return True

    def _find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return (row, col)
        return None

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

    def _is_solved(self):
        # Check if the board is completely filled
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return False
        return True

    def _save_domains(self):
        # Save a copy of the current state of domains
        return {key: set(value) for key, value in self.domains.items()}

    def restore_domains(self, original_domains):
        # Restore the domains from the saved state
        self.domains = original_domains




