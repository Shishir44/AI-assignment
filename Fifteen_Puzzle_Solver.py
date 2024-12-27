from collections import deque
import time
import random

class PuzzleState:
    GOAL_STATE = tuple(tuple(i * 4 + j + 1 if i * 4 + j < 15 else 0 
                     for j in range(4)) for i in range(4))
    
    def __init__(self, board=None):
        self.board = board if board else self.GOAL_STATE
        self._hash = None
        self._blank_pos = None
        self._manhattan = None
    
    def get_blank_position(self):
        """Find position of blank (0) tile with caching."""
        if self._blank_pos is None:
            for i in range(4):
                for j in range(4):
                    if self.board[i][j] == 0:
                        self._blank_pos = (i, j)
                        break
        return self._blank_pos
    
    def manhattan_distance(self):
        """Calculate Manhattan distance with caching."""
        if self._manhattan is None:
            distance = 0
            for i in range(4):
                for j in range(4):
                    tile = self.board[i][j]
                    if tile != 0:
                        goal_row, goal_col = (tile - 1) // 4, (tile - 1) % 4
                        distance += abs(goal_row - i) + abs(goal_col - j)
            self._manhattan = distance
        return self._manhattan
    
    def get_neighbors(self):
        """Generate all possible next states efficiently."""
        i, j = self.get_blank_position()
        moves = [
            (0, 1, "LEFT"), 
            (0, -1, "RIGHT"),
            (1, 0, "UP"), 
            (-1, 0, "DOWN")
        ]
        
        neighbors = []
        board_list = [list(row) for row in self.board]
        
        for di, dj, move in moves:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < 4 and 0 <= new_j < 4:
                # Create new board state
                new_board = [row[:] for row in board_list]
                new_board[i][j], new_board[new_i][new_j] = \
                    new_board[new_i][new_j], new_board[i][j]
                neighbors.append((
                    PuzzleState(tuple(tuple(row) for row in new_board)),
                    move
                ))
        
        return neighbors
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self.board)
        return self._hash

class IDSSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = PuzzleState()
        self.visited_states = set()
        self.current_path = set()
        self.solution = []
    
    def is_solvable(self):
        """Check if the puzzle is solvable."""
        flat_board = []
        blank_row = 0
        for i, row in enumerate(self.initial_state.board):
            for num in row:
                if num != 0:
                    flat_board.append(num)
                else:
                    blank_row = i
        
        inversions = sum(1 for i in range(len(flat_board))
                        for j in range(i + 1, len(flat_board))
                        if flat_board[i] > flat_board[j])
        
        blank_row_from_bottom = 3 - blank_row
        return (blank_row_from_bottom % 2 == 0) == (inversions % 2 == 0)
    
    def dls(self, state, depth, path):
        """Depth-limited search with optimizations."""
        if depth < 0:
            return False
        
        if state.board == self.goal_state.board:
            self.solution = path
            return True
        
        # Prune if Manhattan distance exceeds remaining depth
        if state.manhattan_distance() > depth:
            return False
        
        # Use current_path set for cycle detection in current path
        state_hash = hash(state)
        if state_hash in self.current_path:
            return False
        
        self.current_path.add(state_hash)
        
        for next_state, move in state.get_neighbors():
            next_hash = hash(next_state)
            
            # Skip if we've seen this state in a better path
            if next_hash in self.visited_states:
                continue
            
            if self.dls(next_state, depth - 1, path + [move]):
                return True
        
        self.current_path.remove(state_hash)
        return False
    
    def solve(self, max_depth=31):
        """Solve using Iterative Deepening Search with optimizations."""
        if not self.is_solvable():
            return None
        
        for depth in range(max_depth):
            print(f"\rSearching depth: {depth}", end="")
            self.visited_states.clear()
            self.current_path.clear()
            if self.dls(self.initial_state, depth, []):
                print()  # New line after depth counter
                return self.solution
        
        print()  # New line after depth counter
        return None

def create_random_board(moves=20):
    """Create a random but solvable puzzle state."""
    # Initialize board in goal state
    current_board = []
    num = 1
    for i in range(4):
        row = []
        for j in range(4):
            if i == 3 and j == 3:
                row.append(0)
            else:
                row.append(num)
                num += 1
        current_board.append(row)
    
    blank_pos = [3, 3]  # Initial position of blank tile
    
    # Make random moves
    for _ in range(moves):
        possible_moves = []
        # Check all possible moves
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            new_x, new_y = blank_pos[0] + dx, blank_pos[1] + dy
            if 0 <= new_x < 4 and 0 <= new_y < 4:
                possible_moves.append((dx, dy))
        
        # Make a random move
        if possible_moves:
            dx, dy = random.choice(possible_moves)
            new_x, new_y = blank_pos[0] + dx, blank_pos[1] + dy
            
            # Swap blank tile with chosen adjacent tile
            current_board[blank_pos[0]][blank_pos[1]] = current_board[new_x][new_y]
            current_board[new_x][new_y] = 0
            blank_pos = [new_x, new_y]
    
    return PuzzleState(tuple(tuple(row) for row in current_board))

def print_board(board):
    """Print the puzzle board in a readable format."""
    print("\n+" + "----+" * 4)
    for row in board:
        print("|", end=" ")
        for num in row:
            if num == 0:
                print("  ", end=" |")
            else:
                print(f"{num:2}", end=" |")
        print("\n+" + "----+" * 4)

def main():
    while True:
        print("\n=== 15-Puzzle Solver (IDS) ===")
        print("\n1. Use random puzzle")
        print("2. Enter custom puzzle")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '3':
            print("\nThank you for using the 15-Puzzle Solver!")
            break
            
        if choice == '1':
            initial_state = create_random_board()
        elif choice == '2':
            print("\nEnter the puzzle configuration row by row")
            print("Use 0 for the empty space")
            print("Example: 1 2 3 4")
            
            board = []
            for i in range(4):
                while True:
                    try:
                        row = list(map(int, input(f"Enter row {i+1}: ").split()))
                        if len(row) != 4 or not all(0 <= x <= 15 for x in row):
                            raise ValueError
                        board.append(tuple(row))
                        break
                    except ValueError:
                        print("Invalid input. Please enter 4 numbers between 0 and 15")
            
            initial_state = PuzzleState(tuple(board))
        else:
            print("Invalid choice. Please try again.")
            continue
        
        print("\nInitial state:")
        print_board(initial_state.board)
        
        solver = IDSSolver(initial_state)
        
        if not solver.is_solvable():
            print("\nThis puzzle configuration is not solvable!")
            continue
        
        print("\nSolving...")
        start_time = time.time()
        solution = solver.solve()
        end_time = time.time()
        
        if solution:
            print("\nSolution found!")
            print(f"Number of moves: {len(solution)}")
            print(f"Time taken: {end_time - start_time:.2f} seconds")
            
            print("\nSolution path:")
            current_state = initial_state
            print_board(current_state.board)
            
            for i, move in enumerate(solution, 1):
                input(f"\nPress Enter to see move {i} ({move})")
                
                # Make the move
                blank_row, blank_col = current_state.get_blank_position()
                new_board = [list(row) for row in current_state.board]
                
                if move == "UP":
                    new_row, new_col = blank_row + 1, blank_col
                elif move == "DOWN":
                    new_row, new_col = blank_row - 1, blank_col
                elif move == "LEFT":
                    new_row, new_col = blank_row, blank_col + 1
                else:  # RIGHT
                    new_row, new_col = blank_row, blank_col - 1
                
                new_board[blank_row][blank_col] = new_board[new_row][new_col]
                new_board[new_row][new_col] = 0
                current_state = PuzzleState(tuple(tuple(row) for row in new_board))
                print_board(current_state.board)
        else:
            print("\nNo solution found within the maximum depth!")

if __name__ == "__main__":
    main()