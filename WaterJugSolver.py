from collections import deque

class WaterJugSolver:
    def __init__(self, jug1_capacity, jug2_capacity, target):
        self.jug1_capacity = jug1_capacity
        self.jug2_capacity = jug2_capacity
        self.target = target
        self.visited = set()
        
    def get_next_states(self, state):
        """Generate all possible next states from current state."""
        jug1, jug2 = state
        next_states = []
        
        # Fill jug1
        next_states.append((self.jug1_capacity, jug2))
        
        # Fill jug2
        next_states.append((jug1, self.jug2_capacity))
        
        # Empty jug1
        next_states.append((0, jug2))
        
        # Empty jug2
        next_states.append((jug1, 0))
        
        # Pour from jug1 to jug2
        pour_amount = min(jug1, self.jug2_capacity - jug2)
        next_states.append((jug1 - pour_amount, jug2 + pour_amount))
        
        # Pour from jug2 to jug1
        pour_amount = min(jug2, self.jug1_capacity - jug1)
        next_states.append((jug1 + pour_amount, jug2 - pour_amount))
        
        return [(x, y) for x, y in next_states if (x, y) not in self.visited]

    def solve_bfs(self):
        """Solve using Breadth-First Search."""
        self.visited = set()
        start_state = (0, 0)
        queue = deque([(start_state, [start_state])])
        self.visited.add(start_state)

        while queue:
            current_state, path = queue.popleft()
            jug1, jug2 = current_state

            if jug1 == self.target or jug2 == self.target:
                return path

            for next_state in self.get_next_states(current_state):
                self.visited.add(next_state)
                queue.append((next_state, path + [next_state]))

        return None

    def solve_dfs(self):
        """Solve using Depth-First Search."""
        self.visited = set()
        start_state = (0, 0)
        stack = [(start_state, [start_state])]
        self.visited.add(start_state)

        while stack:
            current_state, path = stack.pop()
            jug1, jug2 = current_state

            if jug1 == self.target or jug2 == self.target:
                return path

            for next_state in self.get_next_states(current_state):
                self.visited.add(next_state)
                stack.append((next_state, path + [next_state]))

        return None

    def print_solution(self, path, method):
        """Print the solution path in a readable format."""
        if path is None:
            print(f"\n{method} Solution: No solution exists!")
            return

        print(f"\n{method} Solution:")
        print(f"Target: {self.target} units")
        print(f"Number of steps: {len(path) - 1}")
        print("\nSteps:")
        for i, (jug1, jug2) in enumerate(path):
            print(f"{i}. Jug1: {jug1} units, Jug2: {jug2} units")

def get_valid_input(prompt, min_value=1):
    """Get valid numeric input from user."""
    while True:
        try:
            value = int(input(prompt))
            if value < min_value:
                print(f"Please enter a number greater than or equal to {min_value}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")

def main():
    print("\n=== Water Jug Problem Solver ===")
    print("Enter the capacities of the jugs and the target amount.\n")

    while True:
        # Get user input with validation
        jug1_capacity = get_valid_input("Enter capacity of first jug: ")
        jug2_capacity = get_valid_input("Enter capacity of second jug: ")
        target = get_valid_input("Enter target amount: ")

        # Validate target amount
        if target > max(jug1_capacity, jug2_capacity):
            print("\nError: Target amount cannot be greater than the capacity of the largest jug!")
            continue

        # Create solver instance and find solutions
        solver = WaterJugSolver(jug1_capacity, jug2_capacity, target)
        
        # Solve using BFS
        bfs_path = solver.solve_bfs()
        solver.print_solution(bfs_path, "BFS")
        
        # Solve using DFS
        dfs_path = solver.solve_dfs()
        solver.print_solution(dfs_path, "DFS")

        # Ask if user wants to try another problem
        while True:
            try_again = input("\nWould you like to solve another problem? (yes/no): ").lower()
            if try_again in ['yes', 'no', 'y', 'n']:
                break
            print("Please enter 'yes' or 'no'")

        if try_again.startswith('n'):
            print("\nThank you for using the Water Jug Problem Solver!")
            break
        print("\n" + "="*35 + "\n")

if __name__ == "__main__":
    main()