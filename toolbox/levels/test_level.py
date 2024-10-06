import os
import pygame
import toolbox.pathfinding
from config import IMAGE_DIR, SCREEN_HEIGHT, SCREEN_WIDTH
from toolbox.level import Level
from toolbox.level_cell import LevelCell
from toolbox.sprites.gameplayer import GamePlayer
from toolbox.sprites.npc import NPC
from toolbox.pathfinding import Pathfinding


class TestLevel(Level):
    def __init__(self):
        super().__init__()
        w, h = 800, 600
        self.level_grid: Pathfinding = Pathfinding([[0] * w for _ in range(h)])
        self.level_grid.create_bounds()

        wall_texture = pygame.image.load(os.path.join(IMAGE_DIR, "test_wall.png"))
        floor_texture = pygame.image.load(os.path.join(IMAGE_DIR, "test_floor.png"))
        ceiling_texture = pygame.image.load(os.path.join(IMAGE_DIR, "test_ceiling.png"))

        self.level_cells = [[None] * w for _ in range(h)]

        for x in range(len(self.level_grid.grid)):
            for y in range(len(self.level_grid.grid[0])):
                wall = None
                ceiling = ceiling_texture
                floor = floor_texture
                grid_spot = self.level_grid.grid[x][y]
                if grid_spot == 1:
                    wall = wall_texture
                self.level_cells[x][y] = LevelCell(wall, ceiling, floor)

    def load_sprites(self):
        GamePlayer((5, 5))
        NPC((3.5, 3.5))
