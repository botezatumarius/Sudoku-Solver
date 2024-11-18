class ConstraintPropagationWithMRVSolver:
    def __init__(self, board):
        self.board = board
        self.domains = self._initialize_domains()

    def solve(self):
        # Apply constraint propagation to reduce domains
        if not self._constraint_propagate():
            return False  # Conflict found during initial propagation
        return self._heuristic_solve()

    def _initialize_domains(self):
        domains = {}
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    domains[(row, col)] = set(range(1, 10))  # Possible values 1-9
                else:
                    domains[(row, col)] = {self.board[row][col]}  # Only one possible value
        return domains

    # Reduce the domains of cells with a value of 0 based on the values in neighboring cells
    def _constraint_propagate(self):
        changed = True
        while changed:
            changed = False
            for (row, col), domain in self.domains.items():
                if self.board[row][col] == 0:
                    for neighbor in self._get_neighbors(row, col):
                        value_at_neighbor = self.board[neighbor[0]][neighbor[1]]
                        if value_at_neighbor != 0 and value_at_neighbor in domain:
                            domain.remove(value_at_neighbor)
                            changed = True
                            if len(domain) == 0:
                                return False  
        return True

    def _heuristic_solve(self):
        if not self._has_empty_cell():
            return True  # Puzzle solved
        
         # Choose cell using MRV (Minimum Remaining Values)
        selected_cell = self._select_mrv()
        if selected_cell is None:
            return False
        
        row, col = self._select_mrv()
        
        # Try values in LCV (Least Constraining Value) order
        values = self._least_constraining_values(row, col)
        for num in values:
            if self._is_valid(num, row, col):
                self.board[row][col] = num
                self.domains[(row, col)] = {num}  # Update domain to reflect placement
                if self._constraint_propagate() and self._heuristic_solve():
                    return True
                self.board[row][col] = 0  # Undo move
                self.domains[(row, col)] = values  # Restore domain for backtracking
        return False

    # Minimum remaining values: Select empty cell with smallest domain
    def _select_mrv(self):
        min_remaining = float('inf')
        min_cell = None
        for (row, col), domain in self.domains.items():
            if self.board[row][col] == 0 and 0 < len(domain) < min_remaining:
                min_remaining = len(domain)
                min_cell = (row, col)
        return min_cell

    def _least_constraining_values(self, row, col):
        # Sorts the possible values for the selected cell in ascending order based on how many values each one eliminates from the domains of neighboring cells.
        values = list(self.domains[(row, col)])
        values.sort(key=lambda val: self._count_constraints(val, row, col))
        return values

    def _count_constraints(self, val, row, col):
        # Count the number of constraints this value imposes on neighbors
        count = 0
        for neighbor in self._get_neighbors(row, col):
            if val in self.domains[neighbor]:
                count += 1
        return count

    def _has_empty_cell(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return True
        return False

    def _is_valid(self, num, row, col):
        if num in self.board[row]:
            return False
        if num in [self.board[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def _get_neighbors(self, row, col):
        neighbors = set()
        for i in range(9):
            if (row, i) != (row, col):
                neighbors.add((row, i))
            if (i, col) != (row, col):
                neighbors.add((i, col))
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r, c) != (row, col):
                    neighbors.add((r, c))
        return neighbors
