# Classic Puzzle Solvers Collection

This repository contains implementations of various classic puzzle-solving algorithms in Python. Each puzzle solver is implemented with optimizations and includes an interactive command-line interface.

## Table of Contents
- [Puzzles Included](#puzzles-included)
- [Installation](#installation)
- [Usage](#usage)
- [Puzzle Descriptions](#puzzle-descriptions)
- [Implementation Details](#implementation-details)
- [Contributing](#contributing)

## Puzzles Included

1. **8-Puzzle Solver** (8puzzleproblem.py)
   - Implementation of the classic sliding tile puzzle
   - Uses A* search algorithm with Manhattan distance heuristic
   - Includes solvability checker

2. **15-Puzzle Solver** (Fifteen_Puzzle_Solver.py)
   - Extended version of the sliding tile puzzle
   - Uses Iterative Deepening Search (IDS) with optimizations
   - Features random puzzle generation

3. **Missionaries and Cannibals** (Missonariesandcannibals.py)
   - Classic river crossing puzzle
   - Implements Breadth-First Search (BFS)
   - Configurable number of missionaries, cannibals, and boat capacity

4. **Tower of Hanoi** (Towerofhannoi.py)
   - Recursive implementation with visual representation
   - Includes move counter and optimal solution checker
   - Interactive visualization of disk movements

5. **Water Jug Problem** (WaterJugSolver.py)
   - Implements both BFS and DFS solutions
   - Configurable jug capacities and target amounts
   - Complete solution path visualization

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd puzzle-solvers
```

2. Ensure you have Python 3.6 or higher installed.

3. No additional dependencies are required as all puzzles use Python's standard library.

## Usage

Each puzzle solver can be run independently. Here's how to use each one:

### 8-Puzzle Solver
```bash
python 8puzzleproblem.py
```
- Enter the initial state as three rows of numbers (0-8)
- 0 represents the empty tile
- The program will find the shortest solution path using A*

### 15-Puzzle Solver
```bash
python Fifteen_Puzzle_Solver.py
```
- Choose between random puzzle or custom configuration
- For custom configuration, enter four rows of numbers (0-15)
- Watch the solution playback step by step

### Missionaries and Cannibals
```bash
python Missonariesandcannibals.py
```
- Enter the number of missionaries, cannibals, and boat capacity
- The program will find a valid solution that safely crosses everyone
- View step-by-step moves with bank states

### Tower of Hanoi
```bash
python Towerofhannoi.py
```
- Enter the number of disks
- Watch the animated solution with disk movements
- See the comparison between actual and minimum possible moves

### Water Jug Problem
```bash
python WaterJugSolver.py
```
- Enter capacities for both jugs and the target amount
- View solutions using both BFS and DFS approaches
- Compare the different solution paths

## Puzzle Descriptions

### 8-Puzzle
The 8-puzzle consists of a 3×3 grid with 8 numbered tiles and one empty space. The goal is to rearrange the tiles from an initial configuration to a goal state where the numbers are in order.

Key features:
- A* search with Manhattan distance heuristic
- Solvability checking using inversion count
- Complete solution path reconstruction

### 15-Puzzle
An extension of the 8-puzzle to a 4×4 grid with 15 numbered tiles. This implementation uses IDS for memory efficiency.

Key features:
- Iterative Deepening Search with optimizations
- State caching for performance
- Random puzzle generation with guaranteed solvability

### Missionaries and Cannibals
A river crossing puzzle where missionaries and cannibals must cross a river using a boat, ensuring that cannibals never outnumber missionaries on either bank.

Key features:
- Configurable number of missionaries, cannibals, and boat capacity
- BFS implementation for shortest solution
- State validation checking

### Tower of Hanoi
A puzzle consisting of three rods and a number of disks of different sizes. The goal is to move all disks from the first rod to the third rod, following specific rules.

Key features:
- Visual representation of tower states
- Recursive solution implementation
- Move counter and optimal solution verification

### Water Jug Problem
A puzzle involving two jugs of different capacities where the goal is to measure a specific amount of water using only filling, emptying, and pouring operations.

Key features:
- Both BFS and DFS implementations
- Complete state space exploration
- Comparison of different solution paths

## Implementation Details

### Search Algorithms Used
- **A* Search**: Used in 8-puzzle with Manhattan distance heuristic
- **IDS**: Used in 15-puzzle for memory efficiency
- **BFS**: Used in Missionaries and Cannibals, Water Jug Problem
- **DFS**: Alternative solution for Water Jug Problem
- **Recursive Solution**: Used in Tower of Hanoi

### Optimizations
1. **State Representation**
   - Efficient state encoding
   - Hash-based state comparison
   - Memory-efficient data structures

2. **Search Optimizations**
   - Pruning invalid states
   - Cycle detection
   - Heuristic functions for guided search

3. **Performance Improvements**
   - Caching of computed values
   - Early goal detection
   - Efficient state generation

