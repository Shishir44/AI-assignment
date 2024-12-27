from collections import deque

class State:
    def __init__(self, missionaries_left, cannibals_left, boat_position, total_missionaries, total_cannibals, missionaries_right=None, cannibals_right=None):
        self.missionaries_left = missionaries_left
        self.cannibals_left = cannibals_left
        self.boat_position = boat_position  # 'left' or 'right'
        self.total_missionaries = total_missionaries
        self.total_cannibals = total_cannibals
        
        # Calculate right bank numbers if not provided
        if missionaries_right is None:
            self.missionaries_right = total_missionaries - missionaries_left
        else:
            self.missionaries_right = missionaries_right
            
        if cannibals_right is None:
            self.cannibals_right = total_cannibals - cannibals_left
        else:
            self.cannibals_right = cannibals_right

    def is_valid(self):
        """Check if the state is valid according to problem constraints."""
        # Check for negative numbers
        if (self.missionaries_left < 0 or self.cannibals_left < 0 or
            self.missionaries_right < 0 or self.cannibals_right < 0):
            return False

        # Check if missionaries are outnumbered on either bank
        if (self.missionaries_left > 0 and self.missionaries_left < self.cannibals_left) or \
           (self.missionaries_right > 0 and self.missionaries_right < self.cannibals_right):
            return False

        return True

    def is_goal(self):
        """Check if this is the goal state (everyone on the right bank)."""
        return (self.missionaries_left == 0 and self.cannibals_left == 0 and
                self.missionaries_right == self.total_missionaries and 
                self.cannibals_right == self.total_cannibals and
                self.boat_position == 'right')

    def __eq__(self, other):
        """Define equality for states."""
        return (self.missionaries_left == other.missionaries_left and
                self.cannibals_left == other.cannibals_left and
                self.boat_position == other.boat_position)

    def __hash__(self):
        """Make State hashable for use in sets."""
        return hash((self.missionaries_left, self.cannibals_left, self.boat_position))

    def __str__(self):
        """String representation of the state."""
        left_bank = f"Left Bank: {self.missionaries_left}M {self.cannibals_left}C"
        right_bank = f"Right Bank: {self.missionaries_right}M {self.cannibals_right}C"
        boat = "Boat: " + self.boat_position
        return f"{left_bank} | {boat} | {right_bank}"

class MissionariesCannibalsGame:
    def __init__(self, total_missionaries, total_cannibals, boat_capacity):
        self.total_missionaries = total_missionaries
        self.total_cannibals = total_cannibals
        self.boat_capacity = boat_capacity
        self.initial_state = State(total_missionaries, total_cannibals, 'left', 
                                 total_missionaries, total_cannibals)
        self.moves = self.generate_possible_moves()

    def generate_possible_moves(self):
        """Generate all possible moves based on boat capacity."""
        moves = []
        # Generate all possible combinations of missionaries and cannibals
        for m in range(self.boat_capacity + 1):
            for c in range(self.boat_capacity + 1):
                if 1 <= m + c <= self.boat_capacity:
                    moves.append((m, c))
        return moves

    def get_next_states(self, current_state):
        """Generate all possible next states from current state."""
        next_states = []
        
        # Determine direction of movement based on boat position
        if current_state.boat_position == 'left':
            direction = -1  # Moving from left to right
            new_boat_position = 'right'
        else:
            direction = 1   # Moving from right to left
            new_boat_position = 'left'

        # Try each possible move
        for m, c in self.moves:
            if current_state.boat_position == 'left':
                new_state = State(
                    current_state.missionaries_left - m,
                    current_state.cannibals_left - c,
                    new_boat_position,
                    self.total_missionaries,
                    self.total_cannibals
                )
            else:
                new_state = State(
                    current_state.missionaries_left + m,
                    current_state.cannibals_left + c,
                    new_boat_position,
                    self.total_missionaries,
                    self.total_cannibals
                )

            if new_state.is_valid():
                next_states.append(new_state)

        return next_states

    def solve(self):
        """Solve the problem using BFS."""
        start_state = self.initial_state
        if start_state.is_goal():
            return [start_state]

        queue = deque([[start_state]])
        visited = {start_state}

        while queue:
            path = queue.popleft()
            current_state = path[-1]

            for next_state in self.get_next_states(current_state):
                if next_state not in visited:
                    visited.add(next_state)
                    new_path = list(path)
                    new_path.append(next_state)

                    if next_state.is_goal():
                        return new_path

                    queue.append(new_path)

        return None

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

def print_solution(solution):
    """Print the solution path in a readable format."""
    if solution is None:
        print("\nNo solution found! This configuration might be impossible to solve.")
        return

    print("\nSolution Found!")
    print(f"Number of steps: {len(solution) - 1}")
    print("\nStep-by-step solution:")
    
    for i, state in enumerate(solution):
        print(f"\nStep {i}:")
        print(state)

def main():
    while True:
        print("\n=== Missionaries and Cannibals Problem Solver ===")
        print("\nEnter the parameters for your problem:")
        
        # Get user inputs
        missionaries = get_valid_input("Enter number of missionaries: ")
        cannibals = get_valid_input("Enter number of cannibals: ")
        boat_capacity = get_valid_input("Enter boat capacity (minimum 1): ")

        print("\nInitial setup:")
        print(f"- {missionaries} missionaries and {cannibals} cannibals on the left bank")
        print(f"- Boat capacity: {boat_capacity} people")
        print("\nRules:")
        print("1. The boat cannot cross the river by itself")
        print("2. Cannibals cannot outnumber missionaries on either bank")
        print("3. All people must cross to the right bank\n")

        # Create and solve the game
        game = MissionariesCannibalsGame(missionaries, cannibals, boat_capacity)
        solution = game.solve()
        print_solution(solution)

        # Ask if user wants to try another configuration
        while True:
            try_again = input("\nWould you like to try another configuration? (yes/no): ").lower()
            if try_again in ['yes', 'no', 'y', 'n']:
                break
            print("Please enter 'yes' or 'no'")

        if try_again.startswith('n'):
            print("\nThank you for using the Missionaries and Cannibals Solver!")
            break

if __name__ == "__main__":
    main()