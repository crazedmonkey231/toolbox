import os
import pygame
from pygame.sprite import Group, Sprite
from config import IMAGE_DIR, SCREEN_HEIGHT, SCREEN_WIDTH, TEXTURE_SIZE, COS, SIN, SCREEN_WIDTH_HALF, SCREEN_HEIGHT_HALF
from math import cos, sin
from toolbox.util import get_sprite_distance

# A map over the world
worldMap = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1]]


# Creates window

wall_texture = pygame.image.load(os.path.join(IMAGE_DIR, "test_wall.png"))
floor_texture = pygame.image.load(os.path.join(IMAGE_DIR, "test_floor.png"))
ceiling_texture = pygame.image.load(os.path.join(IMAGE_DIR, "test_ceiling.png"))


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
        self.bounds = .05

        self.z_buffer: list[float] = [0] * SCREEN_WIDTH

    # moves camera returns transform
    def move(self, move_speed, rotation_speed, forward=False, backward=False, left=False, right=False,
             strafe_left=False, strafe_right=False):

        tgm = (cos(rotation_speed), sin(rotation_speed))
        itgm = (cos(-rotation_speed), sin(-rotation_speed))

        if forward:
            if not worldMap[int(self.position_x + self.direction_x * move_speed)][int(self.position_y)]:
                self.position_x += self.direction_x * move_speed
            if not worldMap[int(self.position_x)][int(self.position_y + self.direction_y * move_speed)]:
                self.position_y += self.direction_y * move_speed
        if backward:
            if not worldMap[int(self.position_x - self.direction_x * move_speed)][int(self.position_y)]:
                self.position_x -= self.direction_x * move_speed
            if not worldMap[int(self.position_x)][int(self.position_y - self.direction_y * move_speed)]:
                self.position_y -= self.direction_y * move_speed
        if strafe_right:
            x_pos = int(self.position_x)
            y_pos = int(self.position_y)
            new_x_pos = int(self.position_x - self.direction_y * move_speed)
            new_y_pos = int(self.position_y + self.direction_x * move_speed)
            if not worldMap[new_x_pos][y_pos]:
                self.position_x -= self.direction_y * move_speed
            if not worldMap[x_pos][new_y_pos]:
                self.position_y += self.direction_x * move_speed
        if strafe_left:
            x_pos = int(self.position_x)
            y_pos = int(self.position_y)
            new_x_pos = int(self.position_x + self.direction_y * move_speed)
            new_y_pos = int(self.position_y - self.direction_x * move_speed)
            if not worldMap[new_x_pos][y_pos]:
                self.position_x += self.direction_y * move_speed
            if not worldMap[x_pos][new_y_pos]:
                self.position_y -= self.direction_x * move_speed
        if left:
            old_direction_x = self.direction_x
            self.direction_x = self.direction_x * itgm[COS] - self.direction_y * itgm[SIN]
            self.direction_y = old_direction_x * itgm[SIN] + self.direction_y * itgm[COS]
            old_plane_x = self.plane_x
            self.plane_x = self.plane_x * itgm[COS] - self.plane_y * itgm[SIN]
            self.plane_y = old_plane_x * itgm[SIN] + self.plane_y * itgm[COS]
        if right:
            old_direction_x = self.direction_x
            self.direction_x = self.direction_x * tgm[COS] - self.direction_y * tgm[SIN]
            self.direction_y = old_direction_x * tgm[SIN] + self.direction_y * tgm[COS]
            old_plane_x = self.plane_x
            self.plane_x = self.plane_x * tgm[COS] - self.plane_y * tgm[SIN]
            self.plane_y = old_plane_x * tgm[SIN] + self.plane_y * tgm[COS]
        return self.position_x, self.position_y, self.direction_x, self.direction_y

    def draw(self, screen):
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
            while hit == 0:
                if side_distance_x < side_distance_y:
                    side_distance_x += delta_distance_x
                    map_x += step_x
                    side = 0
                else:
                    side_distance_y += delta_distance_y
                    map_y += step_y
                    side = 1

                if worldMap[map_x][map_y] > 0:
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

            wall_texture_slice = wall_texture.subsurface((tex_x, 0, 1, TEXTURE_SIZE))
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

                tx = (TEXTURE_SIZE * (floor_x - cell_x)) % TEXTURE_SIZE
                ty = (TEXTURE_SIZE * (floor_y - cell_y)) % TEXTURE_SIZE

                # pygame.draw.rect(screen, "gray", (column, draw_start, self.resolution, self.resolution))
                screen.blit(ceiling_texture, (column, draw_start), (tx, ty, self.resolution, self.resolution))

                # pygame.draw.rect(screen, "purple", (column, draw_end, self.resolution, self.resolution))
                screen.blit(floor_texture, (column, draw_end), (tx, ty, self.resolution, self.resolution))

                draw_start -= self.resolution
                draw_end += self.resolution

        camera_pos = (self.position_x, self.position_y)
        filtered_sorted_sprites = sorted(
            [sprite for sprite in self.sprites() if sprite != self.owner and get_sprite_distance(camera_pos, sprite) > 0.2],
            key=lambda x: get_sprite_distance(camera_pos, x)
        )

        for sprite in filtered_sorted_sprites:
            sprite: Sprite = sprite
            center = sprite.rect.center
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
                        # for y in range(draw_start_y, draw_end_y, self.resolution):
                        #     d = (y - v_move_screen) * 256 - SCREEN_HEIGHT * 128 + sprite_height * 128
                        #     sprite_tex_y = ((d * TEXTURE_SIZE) / sprite_height) / 256
                        #     screen.blit(sprite.image, (stripe, y), (sprite_tex_x, sprite_tex_y, self.resolution, self.resolution))
                        sprite_texture_slice = sprite.image.subsurface((sprite_tex_x, 0, 1, TEXTURE_SIZE))
                        sprite_scaled_slice = pygame.transform.scale(sprite_texture_slice, (self.resolution, min(draw_end_y - draw_start_y, 15000)))
                        screen.blit(sprite_scaled_slice, (stripe, draw_start_y))
