import pygame
from pygame import Vector2, Mask

from toolbox.components.comp_grow import CompGrow
from toolbox.components.comp_input import CompInput
from toolbox.components.comp_launcher import CompTimedLauncher
from toolbox.components.comp_mouse_follower import CompMouseFollowerDirection
from toolbox.game_objects import Player, Projectile
from toolbox.resistry import asset_registry


class FpsPlayer(Player):
    def __init__(self, pos):
        super().__init__(pos)
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
        self.move_speed = 100
        self.components.append(CompInput(self))
        self.comp_launcher = CompTimedLauncher(self, Projectile)
        self.components.append(self.comp_launcher)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        pygame.draw.rect(args[0], (255, 0, 0), self.rect, 3)
        self.comp_launcher.is_firing = pygame.mouse.get_pressed()[0]

        # pos = renderer_group.mouse_pos_to_global_pos()
        # print(pos)
        # if self.rect.collidepoint(pos) and not self.hovered:
        #     self.hovered = True
        # elif not self.rect.collidepoint(pos) and self.hovered:
        #     self.hovered = False
        # print(self.hovered)

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
