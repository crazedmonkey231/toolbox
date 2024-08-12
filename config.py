import os

#
# Game Config
#

# Asset directories
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
IMAGE_DIR = os.path.join(MAIN_DIR, 'images')
AUDIO_DIR = os.path.join(MAIN_DIR, 'audio')
GIF_DIR = os.path.join(MAIN_DIR, 'gif')

# fps
FPS: int = 120

# Screen
SCREEN_SIZE: tuple[int, int] = (1280, 720)
SCREEN_WIDTH: int = SCREEN_SIZE[0]
SCREEN_WIDTH_HALF: int = SCREEN_SIZE[0] // 2
SCREEN_HEIGHT = SCREEN_SIZE[1]
SCREEN_HEIGHT_HALF = SCREEN_SIZE[1] // 2

# Canvas
CANVAS_SIZE: tuple[int, int] = (10000, 10000)
CANVAS_WIDTH: int = CANVAS_SIZE[0]
CANVAS_WIDTH_HALF: int = CANVAS_SIZE[0] // 2
CANVAS_HEIGHT: int = CANVAS_SIZE[1]
CANVAS_HEIGHT_HALF: int = CANVAS_SIZE[1] // 2

# Pathfinding
GRID_WIDTH: int = 32
GRID_SIZE: int = CANVAS_WIDTH // GRID_WIDTH
CELL_SIZE: int = CANVAS_WIDTH // GRID_SIZE
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Colors RGB
RGB_WHITE = (255, 255, 255)
RGB_BLACK = (0, 0, 0)
RGB_RED = (255, 0, 0)
RGB_GREEN = (0, 255, 0)
RGB_BLUE = (0, 0, 255)

# Colors RGBA
RGBA_WHITE = (255, 255, 255, 255)
RGBA_BLACK = (0, 0, 0, 255)
RGBA_RED = (255, 0, 0, 255)
RGBA_GREEN = (0, 255, 0, 255)
RGBA_BLUE = (0, 0, 255, 255)
