class AC3Solver:
    def __init__(self, board):
        self.board = board
        self.domains = self._initialize_domains()

    def solve(self):
        # Apply initial AC-3 constraint propagation
        if not self._ac3():
            return False  # Puzzle is unsolvable

        if not self._solve_with_mrv():
            return self.board  # Indicates the puzzle could not be fully solved
        return self.board

    def _initialize_domains(self):
        # Initialize the domains with possible values for each cell
        domains = {}
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    domains[(row, col)] = set(range(1, 10))
                else:
                    domains[(row, col)] = {self.board[row][col]} 
        return domains

    def _ac3(self):
        queue = [(cell, neighbor) for cell in self.domains for neighbor in self._get_neighbors(*cell)]
        
        while queue:
            (cell1, cell2) = queue.pop(0)
            if self._remove_inconsistent_values(cell1, cell2):
                if len(self.domains[cell1]) == 1:
                    # Directly update board if domain size is reduced to 1
                    self.board[cell1[0]][cell1[1]] = next(iter(self.domains[cell1]))
                
                for neighbor in self._get_neighbors(*cell1):
                    if neighbor != cell2:
                        queue.append((neighbor, cell1))
        
        return all(len(domain) > 0 for domain in self.domains.values())


    def _remove_inconsistent_values(self, cell1, cell2):
        removed = False
        for value in self.domains[cell1].copy():
            # Check if there is no valid value in cell2's domain to support cell1's value
            if not any(value != v for v in self.domains[cell2]):
                self.domains[cell1].remove(value)
                removed = True
        return removed

    def _solve_with_mrv(self):
        # Continues solving as long as there are cells with determined values
        while True:
            cell = self._select_unassigned_with_mrv()
            if cell is None:
                # Final check: ensure every domain is a single value to confirm a fully solved puzzle
                return all(len(domain) == 1 for domain in self.domains.values())
            
            row, col = cell
            value = next(iter(self.domains[(row, col)]))  # Assign the single possible value in MRV cell
            self.board[row][col] = value  # Update board

            # Update the domain to contain only the assigned value
            self.domains[(row, col)] = {value}

            # Propagate constraints from this assignment
            if not self._constraint_propagate():
                return False  # If inconsistency is found, stop solving

    def _constraint_propagate(self):
        # Constraint propagation by removing values from domains
        changed = True
        while changed:
            changed = False
            for (row, col), domain in self.domains.items():
                if len(domain) == 1:
                    value = next(iter(domain))  # Get the single value in the domain
                    self.board[row][col] = value  # Update board here

                    for neighbor in self._get_neighbors(row, col):
                        if value in self.domains[neighbor]:
                            self.domains[neighbor].remove(value)  # Remove the value from neighbor's domain
                            changed = True
                            if len(self.domains[neighbor]) == 0:
                                return False  # Conflict: empty domain found
        return True

    def _select_unassigned_with_mrv(self):
        # Select the unassigned cell with the smallest domain size > 1
        mrv_cell = None
        min_size = 10  
        
        for (row, col), domain in self.domains.items():
            if self.board[row][col] == 0 and 1 < len(domain) < min_size:
                mrv_cell = (row, col)
                min_size = len(domain)
        
        return mrv_cell

    def _get_neighbors(self, row, col):
        # Collect all neighbors in the same row, column, and 3x3 subgrid
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
