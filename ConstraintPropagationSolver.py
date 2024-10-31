class ConstraintPropagationSolver:
    def __init__(self, board):
        self.board = board
        self.domains = self._initialize_domains()

    def solve(self):
        # Apply constraint propagation to reduce domains
        if not self._constraint_propagate():
            return False  # If we find an inconsistency in the initial setup

        return self._is_solved()

    # Set up domains for each cell: possible values for each empty cell.
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

    # Get all neighboring cells that are affected by the current cell.
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

    def _is_solved(self):
        # Check if the board is completely filled
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return False
        return True

