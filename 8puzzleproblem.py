import heapq
import copy
import time

class PuzzleState:
    def __init__(self, board, parent=None, move=None, depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = self.depth + self.manhattan_distance()
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(str(self.board))
    
    def get_blank_pos(self):
        """Find the position of the blank tile (0)."""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j
    
    def manhattan_distance(self):
        """Calculate Manhattan distance heuristic."""
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    x_goal, y_goal = divmod(self.board[i][j] - 1, 3)
                    distance += abs(x_goal - i) + abs(y_goal - j)
        return distance
    
    def is_goal(self):
        """Check if current state is the goal state."""
        return self.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    
    def get_neighbors(self):
        """Generate all possible next states."""
        neighbors = []
        x, y = self.get_blank_pos()
        moves = [
            ('UP', -1, 0),
            ('DOWN', 1, 0),
            ('LEFT', 0, -1),
            ('RIGHT', 0, 1)
        ]
        
        for move, dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_board = [row[:] for row in self.board]
                new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
                neighbors.append(PuzzleState(new_board, self, move, self.depth + 1))
        
        return neighbors

class PuzzleSolver:
    def __init__(self, initial_board):
        self.initial_state = PuzzleState(initial_board)
        self.moves_made = []
    
    def is_solvable(self):
        """Check if the puzzle is solvable using inversion count."""
        flat_board = [num for row in self.initial_state.board for num in row if num != 0]
        inversions = 0
        for i in range(len(flat_board)):
            for j in range(i + 1, len(flat_board)):
                if flat_board[i] > flat_board[j]:
                    inversions += 1
        return inversions % 2 == 0
    
    def solve(self):
        """Solve the puzzle using A* search."""
        if not self.is_solvable():
            return None
        
        start_time = time.time()
        
        open_set = []
        closed_set = set()
        
        heapq.heappush(open_set, self.initial_state)
        
        while open_set:
            current_state = heapq.heappop(open_set)
            
            if current_state.is_goal():
                end_time = time.time()
                self.get_solution_path(current_state)
                return {
                    'moves': self.moves_made,
                    'nodes_explored': len(closed_set),
                    'time_taken': end_time - start_time,
                    'solution_depth': current_state.depth
                }
            
            closed_set.add(current_state)
            
            for neighbor in current_state.get_neighbors():
                if neighbor in closed_set:
                    continue
                
                heapq.heappush(open_set, neighbor)
        
        return None
    
    def get_solution_path(self, final_state):
        """Reconstruct the solution path."""
        current = final_state
        while current.parent:
            self.moves_made.insert(0, current.move)
            current = current.parent

def print_board(board):
    """Print the puzzle board in a readable format."""
    print("\n-------------")
    for row in board:
        print("|", end=" ")
        for num in row:
            if num == 0:
                print(" ", end=" |")
            else:
                print(num, end=" |")
        print("\n-------------")

def get_user_input():
    """Get the initial board configuration from user."""
    print("\nEnter the initial board configuration (0-8, where 0 represents the blank tile)")
    print("Enter each row as space-separated numbers (e.g., '1 2 3')")
    
    board = []
    used_numbers = set()
    
    for i in range(3):
        while True:
            try:
                row = list(map(int, input(f"Enter row {i + 1}: ").strip().split()))
                if len(row) != 3:
                    print("Please enter exactly 3 numbers")
                    continue
                    
                for num in row:
                    if num < 0 or num > 8:
                        raise ValueError("Numbers must be between 0 and 8")
                    if num in used_numbers:
                        raise ValueError(f"Number {num} is already used")
                    used_numbers.add(num)
                
                board.append(row)
                break
            except ValueError as e:
                print(f"Invalid input: {e}")
    
    return board

def main():
    print("\n=== 8-Puzzle Solver using A* Search ===")
    print("\nGoal State:")
    print_board([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    
    while True:
        # Get initial configuration
        initial_board = get_user_input()
        print("\nInitial State:")
        print_board(initial_board)
        
        # Solve puzzle
        solver = PuzzleSolver(initial_board)
        print("\nSolving...")
        
        if not solver.is_solvable():
            print("\nThis puzzle configuration is not solvable!")
        else:
            result = solver.solve()
            
            print("\nSolution found!")
            print(f"Number of moves: {len(result['moves'])}")
            print(f"Nodes explored: {result['nodes_explored']}")
            print(f"Time taken: {result['time_taken']:.3f} seconds")
            print("\nSolution path:")
            print(" -> ".join(result['moves']))
        
        # Ask if user wants to try another puzzle
        while True:
            try_again = input("\nWould you like to solve another puzzle? (yes/no): ").lower()
            if try_again in ['yes', 'no', 'y', 'n']:
                break
            print("Please enter 'yes' or 'no'")
        
        if try_again.startswith('n'):
            print("\nThank you for using the 8-Puzzle Solver!")
            break
        print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main()