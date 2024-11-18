class AC3Solver:
    def __init__(self, board):
        self.board = board
        self.domains = self._initialize_domains()

    def solve(self):
        # Apply AC-3 for initial constraint propagation
        if not self._ac3():
            return False  # Conflict found during propagation
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

    # Arc Consistency Algorithm (AC-3). Ensures that the domains of variables are consistent with their neighbors.
    def _ac3(self):
        queue = [(var, neighbor) for var in self.domains for neighbor in self._get_neighbors(*var)]
        
        while queue:
            var, neighbor = queue.pop(0)
            if self._revise(var, neighbor):
                if len(self.domains[var]) == 0:
                    return False  # Domain wipeout indicates inconsistency
                for neighbor_of_var in self._get_neighbors(*var):
                    if neighbor_of_var != neighbor:
                        queue.append((neighbor_of_var, var))
        return True

    # Revises the domain of var to ensure consistency with neighbor. Returns True if the domain of var was modified.
    def _revise(self, var, neighbor):
        revised = False
        for value in self.domains[var].copy():
            if not any(value != neighbor_value for neighbor_value in self.domains[neighbor]):
                self.domains[var].remove(value)
                revised = True
        return revised

    def _heuristic_solve(self):
        if not self._has_empty_cell():
            return True  # Puzzle solved

        # Choose cell using MRV (Minimum Remaining Values)
        row, col = self._select_mrv()
        if (row, col) is None:
            return True

        # Try values in LCV (Least Constraining Value) order
        values = self._least_constraining_values(row, col)
        for num in values:
            if self._is_valid(num, row, col):
                self.board[row][col] = num
                self.domains[(row, col)] = {num}  # Update domain to reflect placement
                if self._ac3() and self._heuristic_solve():
                    return True
                self.board[row][col] = 0  # Undo move
                self.domains[(row, col)] = set(range(1, 10))  # Restore domain for backtracking
        return False

    # Select empty cell with smallest domain
    def _select_mrv(self):
        min_remaining = float('inf')
        min_cell = None
        for (row, col), domain in self.domains.items():
            if self.board[row][col] == 0 and 0 < len(domain) < min_remaining:
                min_remaining = len(domain)
                min_cell = (row, col)
        return min_cell

    def _least_constraining_values(self, row, col):
        # Sort values by how few restrictions they place on neighbors
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
