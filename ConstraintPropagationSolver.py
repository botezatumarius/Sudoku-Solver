class ConstraintPropagationSolver:
    def __init__(self, board):
        self.board = board
        self.domains = self._initialize_domains()
        self.history = []  # Stack to track domain changes

    def solve(self):
        # Apply constraint propagation to reduce domains
        if not self._constraint_propagate():
            return False  # Conflict found during initial propagation
        return self._backtracking_solve()

    #  Set up the domains for each cell, dictionary where keys are cell coordinates, tuples, values are sets holding the possible values 
    def _initialize_domains(self):
        domains = {}
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    domains[(row, col)] = set(range(1, 10))  # Possible values 1-9
                else:
                    domains[(row, col)] = {self.board[row][col]}  # Only one possible value
        return domains

    # Perform constraint propagation to reduce the domains of cells by removing values already present in neighboring cells.
    def _constraint_propagate(self):
        changed = True
        while changed:
            changed = False
            # Iterate through all empty cells in the grid
            for (row, col), domain in self.domains.items():
                if self.board[row][col] == 0:
                    # Check each neighbor of the current cell
                    for neighbor in self._get_neighbors(row, col):
                        # Get the value at the neighbor cell
                        value_at_neighbor = self.board[neighbor[0]][neighbor[1]]

                        # If the neighbor's value is in the current cell's domain, remove it
                        if value_at_neighbor != 0 and value_at_neighbor in domain:
                            domain.remove(value_at_neighbor)
                            changed = True

                            # If domain becomes empty, return False due to a conflict
                            if len(domain) == 0:
                                return False
                    
        return True

    # Uses a history stack to revert domain changes for backtracking.
    def _backtracking_solve(self):
        empty_cell = self._find_empty()
        if not empty_cell:
            return True  # Puzzle solved
        
        row, col = empty_cell
        for num in list(self.domains[(row, col)]): 
            if self._is_valid(num, row, col):
                # Save the current domains as a snapshot and push it to the stack
                self.history.append(self._save_domains())
                self.board[row][col] = num

                if self._forward_check(row, col, num):  # Perform forward checking
                    if self._backtracking_solve():
                        return True

                # Backtrack: Restore the domains to the previous snapshot
                self._restore_domains(self.history.pop())  # Pop the last snapshot
                self.board[row][col] = 0  # Undo move

        return False

    # Perform forward checking by updating domains of neighboring cells after assigning a value to the current cell.
    def _forward_check(self, row, col, num):
        affected_domains = []
        for neighbor in self._get_neighbors(row, col):
            if num in self.domains[neighbor]:
                # Record the change for backtracking
                affected_domains.append((neighbor, num))
                self.domains[neighbor].remove(num)
                # If a neighbor's domain becomes empty, backtrack
                if len(self.domains[neighbor]) == 0:
                    # Restore changes before returning
                    for cell, val in affected_domains:
                        self.domains[cell].add(val)
                    return False

        return True

    def _save_domains(self):
        # Save a snapshot of the current domains
        return {cell: set(domain) for cell, domain in self.domains.items()}

    def _restore_domains(self, previous_domains):
        # Restore domains from the previous snapshot
        self.domains = previous_domains

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

    # Get the coordinates of all neighboring cells that share the same row, column, or 3x3 subgrid with the cell at (row, col).
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
