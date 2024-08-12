import heapq
import random
import pygame
from pygame import Surface
from config import GRID_SIZE, CELL_SIZE, DIRECTIONS, RGB_WHITE, RGB_BLACK, RGB_GREEN
from toolbox.util import log


# Define grid and node properties
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]  # 0 = walkable, 1 = blocked


# Define the Cell class
class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination


def randomize_walls(amount: int):
    for _ in range(amount):
        rx = random.randint(0, GRID_SIZE - 1)
        ry = random.randint(0, GRID_SIZE - 1)
        if not grid[rx][ry]:
            grid[rx][ry] = 1


# Check if a cell is valid (within the grid)
def is_valid(row, col):
    return (row >= 0) and (row < GRID_SIZE) and (col >= 0) and (col < GRID_SIZE)


# Check if a cell is unblocked
def is_unblocked(row, col):
    return grid[row][col] == 0


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


# Implement the A* search algorithm
def a_star(src_pos, dest_pos):
    # Check if the source and destination are valid
    if not is_valid(src_pos[0], src_pos[1]) or not is_valid(dest_pos[0], dest_pos[1]):
        log("Source or destination is invalid")
        return []

    # Check if the source and destination are unblocked
    if not is_unblocked(src_pos[0], src_pos[1]) or not is_unblocked(dest_pos[0], dest_pos[1]):
        log("Source or the destination is blocked")
        return []

    # Check if we are already at the destination
    if is_destination(src_pos[0], src_pos[1], dest_pos):
        log("We are already at the destination")
        return []

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

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
            if is_valid(new_i, new_j) and is_unblocked(new_i, new_j) and not closed_list[new_i][new_j]:
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


def get_grid_pos(pos):
    return pos[0] // CELL_SIZE, pos[1] // CELL_SIZE


def draw_grid(screen: Surface):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = RGB_WHITE
            if not is_unblocked(x, y):
                color = RGB_BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_path(screen: Surface, path):
    for node in path:
        pygame.draw.rect(screen, RGB_GREEN, (node[0] * CELL_SIZE, node[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

#
# Pathfinding draw test
#
# pygame.init()
# fps = 120
# display_screen = pygame.display.set_mode((game_config.SCREEN_WIDTH, game_config.SCREEN_HEIGHT))
# clock = pygame.time.Clock()
# running = True
# dt = 0
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     draw_grid(display_screen)
#     a_path = a_star((2, 2), (10, 15))
#     draw_path(display_screen, a_path)
#     pygame.display.flip()
#     dt = clock.tick(fps) / 1000
# pygame.quit()
