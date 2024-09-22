import os
from typing import AnyStr, LiteralString

from pygame import Vector2

#
# Game Config
#
DEBUG: bool = False

# Asset directories
MAIN_DIR: AnyStr = os.path.split(os.path.abspath(__file__))[0]
IMAGE_DIR: LiteralString = os.path.join(MAIN_DIR, 'images')
AUDIO_DIR: LiteralString = os.path.join(MAIN_DIR, 'audio')
GIF_DIR: LiteralString = os.path.join(MAIN_DIR, 'gif')

# fps
FPS: int = 120

# Screen
SCREEN_SIZE: tuple[int, int] = (800, 600)
SCREEN_WIDTH: int = SCREEN_SIZE[0]
SCREEN_WIDTH_HALF: int = SCREEN_SIZE[0] // 2
SCREEN_HEIGHT: int = SCREEN_SIZE[1]
SCREEN_HEIGHT_HALF: int = SCREEN_SIZE[1] // 2
SCREEN_SIZE_V2: Vector2 = Vector2(SCREEN_SIZE)
SCREEN_SIZE_HALF_V2: Vector2 = Vector2(SCREEN_WIDTH_HALF, SCREEN_HEIGHT_HALF)

# Canvas
CANVAS_SIZE: tuple[int, int] = (10000, 10000)
CANVAS_WIDTH: int = CANVAS_SIZE[0]
CANVAS_WIDTH_HALF: int = CANVAS_SIZE[0] // 2
CANVAS_HEIGHT: int = CANVAS_SIZE[1]
CANVAS_HEIGHT_HALF: int = CANVAS_SIZE[1] // 2

# Camera
MIN_ZOOM: float = 0.1
MAX_ZOOM: float = 5
ZOOM_STEP: float = 0.1

# Pathfinding
GRID_WIDTH: int = 32
GRID_SIZE: int = CANVAS_WIDTH // GRID_WIDTH
CELL_SIZE: int = CANVAS_WIDTH // GRID_SIZE
DIRECTIONS: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Stock market
HIGH: str = "High"
LOW: str = "Low"
NEUTRAL: str = "Neutral"
DECREASING: str = "Decreasing"
INCREASING: str = "Increasing"

# Colors RGB
RGB_WHITE: tuple[int, int, int] = (255, 255, 255)
RGB_BLACK: tuple[int, int, int] = (0, 0, 0)
RGB_RED: tuple[int, int, int] = (255, 0, 0)
RGB_GREEN: tuple[int, int, int] = (0, 255, 0)
RGB_BLUE: tuple[int, int, int] = (0, 0, 255)
RGB_YELLOW: tuple[int, int, int] = (255, 255, 0)
RGB_CYAN: tuple[int, int, int] = (0, 255, 255)
RGB_PURPLE: tuple[int, int, int] = (255, 0, 255)

# Colors RGBA
RGBA_WHITE: tuple[int, int, int, int] = (255, 255, 255, 255)
RGBA_BLACK: tuple[int, int, int, int] = (0, 0, 0, 255)
RGBA_RED: tuple[int, int, int, int] = (255, 0, 0, 255)
RGBA_GREEN: tuple[int, int, int, int] = (0, 255, 0, 255)
RGBA_BLUE: tuple[int, int, int, int] = (0, 0, 255, 255)
RGBA_YELLOW: tuple[int, int, int] = (255, 255, 0, 255)
RGBA_CYAN: tuple[int, int, int] = (0, 255, 255, 255)
RGBA_PURPLE: tuple[int, int, int] = (255, 0, 255, 255)
