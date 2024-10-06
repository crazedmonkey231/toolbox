import heapq
import random
from toolbox.util import log
from config import DIRECTIONS, MAZE_DIRECTIONS


# Check if a cell is the destination
def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]


# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5


# Trace the path from source to destination
def trace_path(cell_details, dest):
    path = []
    row = dest[0]
    col = dest[1]

    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    # Add the source cell to the path
    path.append((row, col))
    # Reverse the path to get the path from source to destination
    path.reverse()

    return path


# Define the Cell class
class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination


class Pathfinding(object):
    def __init__(self, grid):
        self.grid = grid

    def create_bounds(self):
        w, h = len(self.grid[0]), len(self.grid)
        for row in range(h):
            for col in range(w):
                if row == 0 or row == h - 1 or col == 0 or col == w - 1:
                    self.grid[row][col] = 1

    def randomize_walls(self, amount: int):
        w, h = len(self.grid[0]), len(self.grid)
        for _ in range(amount):
            rx = random.randint(0, w - 1)
            ry = random.randint(0, h - 1)
            if not self.grid[ry][rx]:
                self.grid[ry][rx] = 1

    def fill_grid(self):
        w, h = len(self.grid[0]), len(self.grid)
        for row in range(h):
            for col in range(w):
                self.grid[row][col] = 1

    def carve_maze(self, x, y):
        self.grid[y][x] = 0  # Mark the current cell as part of the path
        directions = MAZE_DIRECTIONS
        # Randomize the directions to create more randomness in the maze
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check if the neighboring cell can be carved
            if self.is_valid(nx, ny) and self.grid[ny][nx] == 1:
                # Carve the wall between current cell and the next cell
                self.grid[ny - dy // 2][nx - dx // 2] = 0
                # Recursively carve the next cell
                self.carve_maze(nx, ny)

    def find_maze_dead_ends(self):
        dead_ends = []
        directions = MAZE_DIRECTIONS
        w, h = len(self.grid[0]), len(self.grid)
        for i in range(1, h - 1):
            for j in range(1, w - 1):
                if self.grid[i][j] == 0:
                    wall_count = 0
                    for dx, dy in directions:
                        nx = i + dx
                        ny = j + dy
                        if self.grid[nx][ny] == 1:
                            wall_count += 1
                    if wall_count == 3:
                        dead_ends.append((i, j))
        return dead_ends

    # Check if a cell is valid (within the grid)
    def is_valid(self, row, col):
        w, h = len(self.grid[0]), len(self.grid)
        return (row >= 0) and (row < h) and (col >= 0) and (col < w)

    # Check if a cell is unblocked
    def is_unblocked(self, row, col):
        return self.grid[row][col] == 0

    # Implement the A* search algorithm
    def a_star(self, src_pos, dest_pos):
        # Check if the source and destination are valid
        if not self.is_valid(src_pos[0], src_pos[1]) or not self.is_valid(dest_pos[0], dest_pos[1]):
            log("Source or destination is invalid")
            return []

        # Check if the source and destination are unblocked
        if not self.is_unblocked(src_pos[0], src_pos[1]) or not self.is_unblocked(dest_pos[0], dest_pos[1]):
            log("Source or the destination is blocked")
            return []

        # Check if we are already at the destination
        if is_destination(src_pos[0], src_pos[1], dest_pos):
            log("We are already at the destination")
            return []

        # Initialize the closed list (visited cells)
        closed_list = [[False for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        # Initialize the details of each cell
        cell_details = [[Cell() for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]

        # Initialize the start cell details
        i = src_pos[0]
        j = src_pos[1]
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j

        # Initialize the open list (cells to be visited) with the start cell
        open_list = []
        heapq.heappush(open_list, (0.0, i, j))

        # Initialize the flag for whether destination is found
        found_dest = False

        # Main loop of A* search algorithm
        while len(open_list) > 0:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)

            # Mark the cell as visited
            i = p[1]
            j = p[2]
            closed_list[i][j] = True

            for direction in DIRECTIONS:
                new_i = i + direction[0]
                new_j = j + direction[1]

                # If the successor is valid, unblocked, and not visited
                if self.is_valid(new_i, new_j) and self.is_unblocked(new_i, new_j) and not closed_list[new_i][new_j]:
                    # If the successor is the destination
                    if is_destination(new_i, new_j, dest_pos):
                        # Set the parent of the destination cell
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        # Trace and print the path from source to destination
                        return trace_path(cell_details, dest_pos)
                    else:
                        # Calculate the new f, g, and h values
                        g_new = cell_details[i][j].g + 1.0
                        h_new = calculate_h_value(new_i, new_j, dest_pos)
                        f_new = g_new + h_new

                        # If the cell is not in the open list or the new f value is smaller
                        if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            # Update the cell details
                            cell_details[new_i][new_j].f = f_new
                            cell_details[new_i][new_j].g = g_new
                            cell_details[new_i][new_j].h = h_new
                            cell_details[new_i][new_j].parent_i = i
                            cell_details[new_i][new_j].parent_j = j

        # If the destination is not found after visiting all cells
        if not found_dest:
            log("Failed to find the destination cell")
