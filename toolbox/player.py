import math
import pygame
from pygame import Surface, Vector2, Mask
from pygame.sprite import Sprite
import toolbox.util
from toolbox.group_config import enemy_group, renderer_group
from toolbox.resistry import asset_registry


class Player(Sprite):
    def __init__(self, pos, group):
        Sprite.__init__(self, group)
        self.player_pos = pygame.Vector2(pos)
        self.move_vector = Vector2(200, 200)
        self.image, self.rect = asset_registry.get_image('fsh')
        self.hello_sound = asset_registry.get_sound('hello')
        self.mask: Mask = pygame.mask.from_surface(self.image)
        self.original_image = self.image
        self.image_x_flipped = pygame.transform.flip(self.original_image, True, False)
        self.current_angle = 0
        self.rotation_speed = 3
        self.image_rot_offset = 180
        self.trails = []
        self.rect.center = self.player_pos
        self.mode = 1
        self.grow = 0
        self.hovered = False
        self.collision_rect = self.rect

    def _input(self, delta_time):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_a]:
            dx = -300 * delta_time
        if keys[pygame.K_d]:
            dx = 300 * delta_time
        if keys[pygame.K_w]:
            dy = -300 * delta_time
        if keys[pygame.K_s]:
            dy = 300 * delta_time
        self.rect.center = round(self.rect.center[0] + dx), round(self.rect.center[1] + dy)

    def update(self, *args, **kwargs):
        self._input(args[0])
        renderer_group.camera_lookat_pos = self.rect.center
        pygame.draw.rect(args[1], (255, 0, 0), self.rect, 3)
        # mouse_pos = pygame.mouse.get_pos()
        #
        # if self.rect.collidepoint(mouse_pos) and not self.hovered:
        #     self.hovered = True
        # elif not self.rect.collidepoint(mouse_pos) and self.hovered:
        #     self.hovered = False
        # if keys[pygame.K_a]:
        #     self.hello_sound.play()
        # center = self.rect.center
        # rect_y = 250 + self.float_movement_sin()
        # self.rect.center = (center[0], rect_y)
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_a]:
        #     self.current_angle += self.rotation_speed
        # if keys[pygame.K_d]:
        #     self.current_angle -= self.rotation_speed
        # self.image, self.rect = toolbox.util.rotate_image(self.original_image, self.current_angle, self.rect.center)
        # if keys[pygame.K_w]:
        #     rad_angle = math.radians(self.current_angle + self.image_rot_offset)
        #     dx = math.sin(rad_angle) * self.move_vector[0] * args[0]
        #     dy = math.cos(rad_angle) * self.move_vector[1] * args[0]
        #     self.player_pos.x += dx
        #     self.player_pos.y += dy
        # self.rect.center = self.player_pos

        # if self.grow > 100:
        #     self.mode = -1
        # if self.grow < 1:
        #     self.mode = 1
        # self.grow += 1 * self.mode
        #
        # orig_x, orig_y = self.original_image.get_size()
        # size_x = orig_x + round(self.grow)
        # size_y = orig_y + round(self.grow)
        # self.image, self.rect = toolbox.util.scale_image_smooth(self.original_image, (size_x, size_y), self.rect.center)

        #
        # collision test
        #
        # i = toolbox.util.get_sprite_collide_by_mask(self, enemy_group, True)
        # print(i)
        # if i:
        #     print('enemy collision')
