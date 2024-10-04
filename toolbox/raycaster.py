import os
import pygame
from pygame import Surface, Vector2
from pygame.sprite import Group, Sprite
import shared
from config import SCREEN_HEIGHT, SCREEN_WIDTH, TEXTURE_SIZE, COS, SIN, SCREEN_WIDTH_HALF, SCREEN_HEIGHT_HALF
from math import cos, sin
from toolbox.util import log


class Raycaster(Group):
    def __init__(self):
        super().__init__()

        self.owner: Sprite = None

        self.position_x = 0
        self.position_y = 0

        self.direction_x = 1.0
        self.direction_y = 0.0

        self.plane_x = 0.0
        self.plane_y = 0.66

        self.resolution = 4
        self.bounds = .1
        self.render_distance = 500

        self.z_buffer: list[float] = [0] * SCREEN_WIDTH

    def _modify_transform(self, x, y):
        old_direction_x = self.direction_x
        self.direction_x = self.direction_x * x - self.direction_y * y
        self.direction_y = old_direction_x * y + self.direction_y * x
        old_plane_x = self.plane_x
        self.plane_x = self.plane_x * x - self.plane_y * y
        self.plane_y = old_plane_x * y + self.plane_y * x

    # moves camera returns transform
    def move(self, move_speed, rotation_speed, forward=False, backward=False, left=False, right=False,
             strafe_left=False, strafe_right=False):

        tgm = (cos(rotation_speed), sin(rotation_speed))
        itgm = (cos(-rotation_speed), sin(-rotation_speed))

        dx = self.direction_x * move_speed
        dy = self.direction_y * move_speed

        x_pos = int(self.position_x)
        y_pos = int(self.position_y)

        l_grid = shared.current_level.level_grid

        if forward:
            if not l_grid[int(self.position_x + dx)][y_pos]:
                self.position_x += dx
            if not l_grid[x_pos][int(self.position_y + dy)]:
                self.position_y += dy
        if backward:
            if not l_grid[int(self.position_x - dx)][y_pos]:
                self.position_x -= dx
            if not l_grid[x_pos][int(self.position_y - dy)]:
                self.position_y -= dy
        if strafe_right:
            new_x_pos = int(self.position_x - dy)
            new_y_pos = int(self.position_y + dx)
            if not shared.current_level.level_grid[new_x_pos][y_pos]:
                self.position_x -= dy
            if not shared.current_level.level_grid[x_pos][new_y_pos]:
                self.position_y += dx
        if strafe_left:
            new_x_pos = int(self.position_x + dy)
            new_y_pos = int(self.position_y - dx)
            if not l_grid[new_x_pos][y_pos]:
                self.position_x += dy
            if not l_grid[x_pos][new_y_pos]:
                self.position_y -= dx
        if left:
            self._modify_transform(itgm[COS], itgm[SIN])
        if right:
            self._modify_transform(tgm[COS], tgm[SIN])
        return self.position_x, self.position_y, self.direction_x, self.direction_y

    def _get_sprite_distance(self, sprite):
        center: Vector2 = sprite.raycaster_draw_position
        pos: Vector2 = Vector2(self.position_x, self.position_y)
        return (center - pos).length()

    def _get_valid_sprites(self, sprite):
        return sprite != self.owner and self.bounds < self._get_sprite_distance(sprite) < self.render_distance

    def draw(self, screen: Surface):
        if not shared.current_level.level_cells:
            return
        for column in range(0, SCREEN_WIDTH, self.resolution):
            camera_x = 2.0 * column / SCREEN_WIDTH - 1.0

            ray_dir_x = self.direction_x + self.plane_x * camera_x
            ray_dir_y = self.direction_y + self.plane_y * camera_x + 1e-30

            # In what square is the ray?
            map_x = int(self.position_x)
            map_y = int(self.position_y)

            # Delta distance calculation
            delta_distance_x = 1e-30 if ray_dir_x == 0 else abs(1 / ray_dir_x)
            delta_distance_y = 1e-30 if ray_dir_y == 0 else abs(1 / ray_dir_y)

            # We need sideDistanceX and Y for distance calculation. Checks quadrant
            if ray_dir_x < 0:
                step_x = -1
                side_distance_x = (self.position_x - map_x) * delta_distance_x
            else:
                step_x = 1
                side_distance_x = (map_x + 1.0 - self.position_x) * delta_distance_x

            if ray_dir_y < 0:
                step_y = -1
                side_distance_y = (self.position_y - map_y) * delta_distance_y
            else:
                step_y = 1
                side_distance_y = (map_y + 1.0 - self.position_y) * delta_distance_y

            # Finding distance to a wall
            hit = 0
            side = 0
            wall_tex = None
            while hit == 0:
                if side_distance_x < side_distance_y:
                    side_distance_x += delta_distance_x
                    map_x += step_x
                    side = 0
                else:
                    side_distance_y += delta_distance_y
                    map_y += step_y
                    side = 1
                try:
                    if shared.current_level.level_grid[map_x][map_y] > 0:
                        hit = 1
                        wall_tex = (shared.current_level.level_cells[map_x][map_y]).wall
                except (IndexError, TypeError) as error:
                    log(f"Error drawing floor and ceilings.\n{error}")
                    hit = 1

            # Correction against fish eye effect
            if side == 0:
                perp_wall_dist = side_distance_x - delta_distance_x
            else:
                perp_wall_dist = side_distance_y - delta_distance_y
            perp_wall_dist = max(perp_wall_dist, self.bounds)

            self.z_buffer[column] = perp_wall_dist

            line_height = int(SCREEN_HEIGHT / perp_wall_dist)
            draw_start = int((-line_height + SCREEN_HEIGHT) / 2)
            draw_end = int((line_height + SCREEN_HEIGHT) / 2)

            if not side:
                wall_x = self.position_y + perp_wall_dist * ray_dir_y
            else:
                wall_x = self.position_x + perp_wall_dist * ray_dir_x

            tex_x = int(TEXTURE_SIZE * wall_x) % TEXTURE_SIZE

            if wall_tex:
                wall_texture_slice = wall_tex.subsurface((tex_x, 0, 1, TEXTURE_SIZE))
                wall_scaled_slice = pygame.transform.scale(wall_texture_slice, (self.resolution, draw_end - draw_start))
                screen.blit(wall_scaled_slice, (column, draw_start))

            while draw_end < SCREEN_HEIGHT:
                p = draw_end - SCREEN_HEIGHT_HALF
                pos_z = 0.5 * SCREEN_HEIGHT
                row_distance = pos_z / p

                floor_x = self.position_x + row_distance * ray_dir_x
                floor_y = self.position_y + row_distance * ray_dir_y

                cell_x = int(floor_x)
                cell_y = int(floor_y)

                try:
                    cell_data = shared.current_level.level_cells[cell_x][cell_y]
                    ceiling_tex = cell_data.ceiling
                    floor_tex = cell_data.floor

                    tx = (TEXTURE_SIZE * (floor_x - cell_x)) % TEXTURE_SIZE
                    ty = (TEXTURE_SIZE * (floor_y - cell_y)) % TEXTURE_SIZE

                    # pygame.draw.rect(screen, "gray", (column, draw_start, self.resolution, self.resolution))
                    screen.blit(ceiling_tex, (column, draw_start), (tx, ty, self.resolution, self.resolution))

                    # pygame.draw.rect(screen, "purple", (column, draw_end, self.resolution, self.resolution))
                    screen.blit(floor_tex, (column, draw_end), (tx, ty, self.resolution, self.resolution))
                except (IndexError, TypeError) as error:
                    log(f"Error drawing floor and ceilings.\n{error}")

                draw_start -= self.resolution
                draw_end += self.resolution

        f_sprites = filter(lambda x: self._get_valid_sprites(x), self.sprites())
        fs_sprites = sorted(f_sprites, key=lambda x: self._get_sprite_distance(x), reverse=True)
        for sprite in fs_sprites:
            center = sprite.raycaster_draw_position
            sprite_x = center[0] - self.position_x
            sprite_y = center[1] - self.position_y

            inv_det = 1.0 / (self.plane_x * self.direction_y - self.direction_x * self.plane_y)

            transform_x = inv_det * (self.direction_y * sprite_x - self.direction_x * sprite_y)
            transform_y = inv_det * (-self.plane_y * sprite_x + self.plane_x * sprite_y)

            if transform_y > 0:
                sprite_screen_x = int(SCREEN_WIDTH_HALF * (1 + transform_x / transform_y))

                u_div = 1
                v_div = 1
                v_move = 0.0
                v_move_screen = int(v_move / transform_y)

                sprite_width = abs(int(SCREEN_HEIGHT / transform_y)) / u_div
                sprite_height = abs(int(SCREEN_HEIGHT / transform_y)) / v_div

                draw_start_x = -sprite_width / 2 + sprite_screen_x
                if draw_start_x < 0:
                    draw_start_x = 0

                draw_end_x = sprite_width / 2 + sprite_screen_x
                if draw_end_x >= SCREEN_WIDTH:
                    draw_end_x = SCREEN_WIDTH - 1

                draw_start_y = int(-sprite_height / 2 + SCREEN_HEIGHT_HALF + v_move_screen)
                # if draw_start_y < 0:
                #     draw_start_y = 0

                draw_end_y = int(sprite_height / 2 + SCREEN_HEIGHT_HALF + v_move_screen)
                # if draw_end_y > SCREEN_HEIGHT:
                #     draw_end_y = SCREEN_HEIGHT + 1

                if 0 < draw_start_x < SCREEN_WIDTH:
                    draw_start_x = max(0, draw_start_x)
                    draw_end_x = min(SCREEN_WIDTH, draw_end_x)

                for stripe in range(int(draw_start_x), int(draw_end_x)):
                    sprite_tex_x = int(256 * (stripe - (sprite_screen_x - sprite_width / 2)) * sprite.image.get_width() / sprite_width) / 256
                    if transform_y < self.z_buffer[stripe]:
                        # Scaling based blit
                        if sprite_tex_x >= 1:
                            sprite_texture_slice = sprite.image.subsurface((sprite_tex_x, 0, 1, TEXTURE_SIZE))
                            size = (self.resolution, min(draw_end_y - draw_start_y, 15000))
                            sprite_scaled_slice = pygame.transform.scale(sprite_texture_slice, size)
                            screen.blit(sprite_scaled_slice, (stripe, draw_start_y))
                        # Resolution based blit
                        # for y in range(draw_start_y, draw_end_y, self.resolution):
                        #     d = ((y - v_move_screen) * 256) - ((SCREEN_HEIGHT + sprite_height) * 128)
                        #     sprite_tex_y = ((d * TEXTURE_SIZE) / sprite_height) / 256
                        #     area = (sprite_tex_x, sprite_tex_y, self.resolution, self.resolution)
                        #     screen.blit(sprite.image, (stripe, y), area)
