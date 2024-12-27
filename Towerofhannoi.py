import time
import os
import platform

class Disk:
    def __init__(self, size):
        self.size = size
    
    def __str__(self):
        return str(self.size)
    
    def __repr__(self):
        return f"Disk({self.size})"
    
    def __lt__(self, other):
        if other is None:
            return False
        return self.size < other.size

class Tower:
    def __init__(self, name, capacity):
        self.name = name
        self.disks = []
        self.capacity = capacity
    
    def add_disk(self, disk):
        if not self.disks or disk < self.disks[-1]:
            self.disks.append(disk)
            return True
        return False
    
    def remove_disk(self):
        if not self.disks:
            return None
        return self.disks.pop()
    
    def peek(self):
        if not self.disks:
            return None
        return self.disks[-1]
    
    def __str__(self):
        return f"Tower {self.name}: {[str(disk) for disk in self.disks]}"
    
    def __repr__(self):
        return f"Tower({self.name}, {self.disks})"

class HanoiState:
    def __init__(self, num_disks):
        self.num_disks = num_disks
        self.towers = [
            Tower('A', num_disks),
            Tower('B', num_disks),
            Tower('C', num_disks)
        ]
        self.moves = []
        self.current_move = -1
        
        # Initialize the first tower with all disks
        for size in range(num_disks, 0, -1):
            self.towers[0].add_disk(Disk(size))
    
    def is_valid_move(self, from_tower, to_tower):
        if not (0 <= from_tower < 3 and 0 <= to_tower < 3):
            return False
        
        source = self.towers[from_tower]
        target = self.towers[to_tower]
        
        if not source.disks:
            return False
        
        return target.peek() is None or source.peek() < target.peek()
    
    def make_move(self, from_tower, to_tower):
        if self.is_valid_move(from_tower, to_tower):
            disk = self.towers[from_tower].remove_disk()
            self.towers[to_tower].add_disk(disk)
            self.moves.append((from_tower, to_tower, disk.size))
            self.current_move += 1
            return True
        return False
    
    def undo_move(self):
        if self.current_move >= 0:
            from_tower, to_tower, disk_size = self.moves[self.current_move]
            disk = self.towers[to_tower].remove_disk()
            self.towers[from_tower].add_disk(disk)
            self.current_move -= 1
            return True
        return False
    
    def is_solved(self):
        return len(self.towers[2].disks) == self.num_disks

class HanoiVisualizer:
    def __init__(self, max_disk_width=20):
        self.max_disk_width = max_disk_width
        self.clear_command = 'cls' if platform.system() == 'Windows' else 'clear'
    
    def clear_screen(self):
        os.system(self.clear_command)
    
    def display_state(self, state, move_count=None, delay=0):
        self.clear_screen()
        print("\n=== Towers of Hanoi ===")
        if move_count is not None:
            print(f"Move: {move_count}")
        
        # Get maximum tower height
        max_height = state.num_disks
        
        # Display towers
        for level in range(max_height - 1, -1, -1):
            row = ""
            for tower in state.towers:
                if level < len(tower.disks):
                    disk = tower.disks[level]
                    disk_width = disk.size * 2 - 1
                    disk_str = f"{'#' * disk_width:^{self.max_disk_width}}"
                else:
                    disk_str = f"|".center(self.max_disk_width)
                row += disk_str + " "
            print(row)
        
        # Display tower bases
        base_line = "=" * self.max_disk_width
        print(f"{base_line} {base_line} {base_line}")
        
        # Display tower labels
        labels = "A".center(self.max_disk_width) + " " + \
                "B".center(self.max_disk_width) + " " + \
                "C".center(self.max_disk_width)
        print(labels)
        
        if delay > 0:
            time.sleep(delay)

class HanoiSolver:
    def __init__(self, num_disks, visualizer=None, delay=0.5):
        self.state = HanoiState(num_disks)
        self.visualizer = visualizer
        self.delay = delay
    
    def solve(self):
        """Solve the puzzle using recursion."""
        self._move_tower(self.state.num_disks, 0, 2, 1)
        return self.state.moves
    
    def _move_tower(self, height, source, target, auxiliary):
        if height >= 1:
            # Move n-1 disks from source to auxiliary
            self._move_tower(height - 1, source, auxiliary, target)
            
            # Move the largest disk from source to target
            self.state.make_move(source, target)
            if self.visualizer:
                self.visualizer.display_state(self.state, len(self.state.moves), self.delay)
            
            # Move n-1 disks from auxiliary to target
            self._move_tower(height - 1, auxiliary, target, source)

def main():
    while True:
        try:
            print("\n=== Towers of Hanoi Solver ===")
            num_disks = int(input("\nEnter the number of disks (1-8): "))
            
            if num_disks < 1:
                print("Please enter a positive number")
                continue
            
            if num_disks > 8:
                print("Warning: Using more than 8 disks might be hard to visualize")
                confirm = input("Continue anyway? (y/n): ")
                if confirm.lower() != 'y':
                    continue
            
            # Initialize visualizer and solver
            visualizer = HanoiVisualizer(max_disk_width=20)
            solver = HanoiSolver(num_disks, visualizer, delay=0.5)
            
            # Display initial state
            visualizer.display_state(solver.state, move_count=0)
            input("\nPress Enter to start solving...")
            
            # Solve the puzzle
            start_time = time.time()
            moves = solver.solve()
            end_time = time.time()
            
            # Display results
            total_moves = len(moves)
            time_taken = end_time - start_time
            
            print(f"\nPuzzle solved!")
            print(f"Total moves: {total_moves}")
            print(f"Time taken: {time_taken:.2f} seconds")
            print(f"Minimum possible moves: {2**num_disks - 1}")
            
            # Ask to try again
            again = input("\nWould you like to solve another puzzle? (y/n): ")
            if again.lower() != 'y':
                print("\nThank you for using the Towers of Hanoi Solver!")
                break
        
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nProgram terminated by user")
            break

if __name__ == "__main__":
    main()