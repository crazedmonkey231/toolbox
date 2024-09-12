import math
from collections import defaultdict
from typing import Sequence

import numpy
from numpy import ndarray
import pygame
from pygame import Surface, Rect, Vector2
from pygame.sprite import Sprite, AbstractGroup
from PIL import Image
from PIL.GifImagePlugin import GifImageFile
from config import DEBUG

# Check mixer
mixer_initialized = pygame.mixer or pygame.mixer.get_init()
if not mixer_initialized:
    print("Warning, sound disabled")
if not pygame.font:
    print("Warning, fonts disabled")


#
# Begin utils
#


# Logger
def log(msg: str):
    if DEBUG:
        print(msg)


# Simple tree maker
def tree():
    return defaultdict(tree)


# Check inside widow bounds
def is_within_screen_bounds(pos, screen_size):
    return 0 <= pos[0] <= screen_size[0] and 0 <= pos[1] <= screen_size[1]


# Map a range to another
def map_range(value, start1, stop1, start2, stop2):
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))


# Clamp value between range
def clamp_value(value, start, stop):
    return min(max(value, start), stop)


# Map range clamped
def map_range_clamped(value, start1, stop1, start2, stop2):
    return clamp_value(map_range(value, start1, stop1, start2, stop2), start2, stop2)


# Get a ndarray matrix of a surface filled with rgba values of pixels
def get_rgba_pixel_array(surface: Surface):
    w, h = surface.get_size()
    s = w * h
    a_matrix: ndarray = numpy.zeros((w, h, 4))
    for i in range(s):
        row = i // h
        col = i % h
        a_matrix[row, col] = tuple(surface.get_at((row, col)))
    return a_matrix


# Get an outline ndarray matrix of a surface filled with rgba values of pixels with a given width
def get_rgba_pixel_array_outline(surface: Surface, outline_color=(0, 255, 255, 255), outline_width: int = 3):
    w, h = surface.get_size()
    s = w * h
    a_matrix: ndarray = numpy.zeros((w, h, 4))

    def set_pixel(x, y):
        if not (0 <= x < w and 0 <= y < h):
            return
        if not a_matrix[x, y][3] and tuple(a_matrix[x, y]) != outline_color:
            a_matrix[x, y] = outline_color

    for i in range(s):
        row = i // h
        col = i % h
        color = tuple(surface.get_at((row, col)))
        if color[3]:
            a_matrix[row, col] = tuple(surface.get_at((row, col)))
            for ow in range(outline_width):
                set_pixel(row, col - ow)
                set_pixel(row, col + ow)
                set_pixel(row - ow, col)
                set_pixel(row + ow, col)
    return a_matrix


# Write a ndarray matrix of colors onto a surface
def write_rgb_pixel_array(surface: Surface, matrix: ndarray):
    w, h = surface.get_size()
    s = w * h
    for i in range(s):
        row = i // h
        col = i % h
        surface.set_at((row, col), matrix[row, col])


# Mask based sprite collisions
def get_sprite_collide_by_mask(source: Sprite, group: AbstractGroup, do_kill: bool = False) -> list[Sprite]:
    return pygame.sprite.spritecollide(source, group, do_kill, pygame.sprite.collide_mask)


# Rotate image
# Example:
# self.current_angle -= self.rotation_speed
# self.image, self.rect = toolbox.util.rotate_image(self.original_image, self.current_angle, self.rect.center)
def rotate_image(original_image: Surface, angle: float, center) -> tuple[Surface, Rect]:
    rotated_image = pygame.transform.rotate(original_image, angle)
    new_rect = rotated_image.get_rect(center=center)
    return rotated_image, new_rect


# Scale image basic.
# Example:
# orig_x, orig_y = self.original_image.get_size()
# size_x = orig_x + round(self.grow)
# size_y = orig_y + round(self.grow)
# self.image, self.rect = toolbox.util.scale_image_basic(self.original_image, (size_x, size_y), self.rect.center)
def scale_image_basic(original_image: Surface, new_size: tuple, center) -> tuple[Surface, Rect]:
    new_image = pygame.transform.scale(original_image, new_size)
    new_rect = new_image.get_rect(center=center)
    return new_image, new_rect


# Scale image smooth.
# Example:
# orig_x, orig_y = self.original_image.get_size()
# size_x = orig_x + round(self.grow)
# size_y = orig_y + round(self.grow)
# self.image, self.rect = toolbox.util.scale_image_smooth(self.original_image, (size_x, size_y), self.rect.center)
def scale_image_smooth(original_image: Surface, new_size: Sequence[float], center) -> tuple[Surface, Rect]:
    new_image = pygame.transform.smoothscale(original_image, new_size)
    new_rect = new_image.get_rect(center=center)
    return new_image, new_rect


# Sin curve movement, add this to the default location of the rect for hover movement in the sprite update method.
# Example:
# center = self.rect.center
# rect_y = 250 + self.float_movement_sin()
# self.rect.center = (center[0], rect_y)
def float_movement_sin(amplitude: float = 25, speed: float = 1):
    time = pygame.time.get_ticks() / 1000
    delta = amplitude * math.sin(speed * time)
    return delta


# Cos curve movement, add this to the default location of the rect for hover movement in the sprite update method.
# Example:
# center = self.rect.center
# rect_y = 250 + self.float_movement_cos()
# self.rect.center = (center[0], rect_y)
def float_movement_cos(amplitude: float = 25, speed: float = 1):
    time = pygame.time.get_ticks() / 1000
    delta = amplitude * math.cos(speed * time)
    return delta


def generate_line(start_pos: Vector2, target_pos: Vector2):
    points = []
    dist_target = target_pos - start_pos
    dist_target_len = dist_target.length()
    if dist_target_len > 0:
        dist_target_norm = dist_target.normalize()
        rect_x = start_pos.x
        rect_y = start_pos.y
        for _ in range(int(dist_target_len)):
            rect_x += dist_target_norm.x
            rect_y += dist_target_norm.y
            points.append(Vector2(rect_x, rect_y))
    return points


def generate_arch(start_pos: Vector2, target_pos: Vector2, max_arch_height: float = 100, max_arch_delta: float = 10,
                  inverse: bool = False):
    points = []
    inverse = -1 if inverse else 1
    dist_target = target_pos - start_pos
    dist_target_len = dist_target.length()
    if dist_target_len > 0:
        dist_target_norm = dist_target.normalize()
        dist_target_abs = Vector2(abs(dist_target.x), abs(dist_target.y))
        dist_target_delta = int(dist_target_len)
        rect_x = start_pos.x
        arch_height_max = max_arch_height
        arch_height = clamp_value(dist_target_abs.x, 1, arch_height_max)
        delta_arch = map_range_clamped(dist_target_len, 0, 1000, 1, max_arch_delta)
        epsilon = 1e-6
        for _ in range(dist_target_delta):
            rect_x += dist_target_norm.x
            norm_position = abs((rect_x - start_pos.x) / (dist_target_abs.x + epsilon))
            rect_y = ((1 - norm_position) * start_pos.y + norm_position * target_pos.y -
                      arch_height * inverse * delta_arch * norm_position * (1 - norm_position))
            points.append(Vector2(rect_x, rect_y))
    return points


def generate_circle(center_pos: Vector2, radius: float = 5, start_x_offset: float = 0, start_y_offset: float = 0):
    points = []
    start_x = center_pos.x + radius * start_x_offset
    start_y = center_pos.y + radius * start_y_offset
    for angle in range(360):
        r_angle = math.radians(angle)
        rect_x = start_x + math.cos(r_angle) * radius
        rect_y = start_y + math.sin(r_angle) * radius
        points.append(Vector2(rect_x, rect_y))
    return points


# Interpolates between color1 and color2 using a factor.
def interpolate_color_rgb(color1, color2, factor) -> tuple[int, int, int]:
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = clamp_value(int(r1 + (r2 - r1) * factor), 0, 255)
    g = clamp_value(int(g1 + (g2 - g1) * factor), 0, 255)
    b = clamp_value(int(b1 + (b2 - b1) * factor), 0, 255)
    return r, g, b


# Interpolates between color1 and color2 using a factor.
def interpolate_color_rgba(color1, color2, factor) -> tuple[int, int, int, int]:
    r1, g1, b1, a1 = color1
    r2, g2, b2, a2 = color2
    r = clamp_value(int(r1 + (r2 - r1) * factor), 0, 255)
    g = clamp_value(int(g1 + (g2 - g1) * factor), 0, 255)
    b = clamp_value(int(b1 + (b2 - b1) * factor), 0, 255)
    a = clamp_value(int(a1 + (a2 - a1) * factor), 0, 255)
    return r, g, b, a


# Simple text maker rgb
def make_simple_text_rgb(text: str, size: int = 64, color: tuple[int, int, int] = (255, 255, 255)) \
        -> tuple[Surface, Rect]:
    font = pygame.font.Font(None, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    return text, text_rect


# Simple text maker rgba
def make_simple_text_rgba(text: str, size: int = 64, color: tuple[int, int, int, int] = (255, 255, 255, 255)) \
        -> tuple[Surface, Rect]:
    font = pygame.font.Font(None, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    return text, text_rect

#
# Begin Sprite callables
#


def call_on_hover_start_method(sprite: Sprite):
    method_name = 'on_hover_start'
    if hasattr(sprite, method_name) and callable(getattr(sprite, method_name)):
        method = getattr(sprite, method_name)
        method()


def call_on_hover_end_method(sprite: Sprite):
    method_name = 'on_hovered_end'
    if hasattr(sprite, method_name) and callable(getattr(sprite, method_name)):
        method = getattr(sprite, method_name)
        method()


def call_on_click_start_method(sprite: Sprite):
    method_name = 'on_click_start'
    if hasattr(sprite, method_name) and callable(getattr(sprite, method_name)):
        method = getattr(sprite, method_name)
        method()


def call_on_click_end_method(sprite: Sprite):
    method_name = 'on_click_end'
    if hasattr(sprite, method_name) and callable(getattr(sprite, method_name)):
        method = getattr(sprite, method_name)
        method()


def call_cutscene_start_method(sprite: Sprite):
    method_name = 'cutscene_start'
    if hasattr(sprite, method_name) and callable(getattr(sprite, method_name)):
        method = getattr(sprite, method_name)
        method()


def call_cutscene_skip_method(sprite: Sprite):
    method_name = 'cutscene_skip'
    if hasattr(sprite, method_name) and callable(getattr(sprite, method_name)):
        method = getattr(sprite, method_name)
        method()


def apply_damage(target_sprite: Sprite, causer_sprite: Sprite, damage_amount: float,
                 affected_stat: str = "health", is_crit: bool = False, crit_multi: float = 1.0,
                 *args, **kwargs) -> float:
    method_name = 'on_damage'
    damage_dealt: float = 0.0
    if hasattr(target_sprite, method_name) and callable(getattr(target_sprite, method_name)):
        method = getattr(target_sprite, method_name)
        calc_kwargs = {"causer": causer_sprite,
                       "is_crit": is_crit,
                       "crit_multi": crit_multi,
                       "affected_stat": affected_stat,
                       "damage_amount": damage_amount * crit_multi if is_crit else damage_amount
                       }
        new_args = {**calc_kwargs, **kwargs}
        damage_dealt = method(*args, **new_args)
    return damage_dealt


#
# Begin Particle functions
# Needs particle list and custom draw surface set up that gets blit onto the screen as either an overlay or underlay.
# Using screen surface for creating or updating will cause unwanted overwriting of sprite images.
# If being used in sprite update method, run update first then create new or the color on creation will be overridden.
#

# Create initial rect particle
def create_rect_particle(draw_surface: Surface, particles: list, color, rect: Rect, size: tuple, width: float):
    s_width, s_height = size
    width_h = s_width // 2
    height_h = s_height // 2
    left = rect.centerx - width_h
    right = rect.centery - height_h
    particles.append(pygame.draw.rect(draw_surface, color, (left, right, s_width, s_height), width))


# Create initial circle particle
def create_circle_particle(draw_surface: Surface, particles: list, color, center: tuple, radius: tuple, width: float):
    particles.append(pygame.draw.circle(draw_surface, color, center, radius, width))


# Update rect particles
def update_rect_particles(draw_surface: Surface, particles: list, time_alive: float, decay_factor: float = 2.0,
                          color=(255, 255, 255, 255)):
    n_trails = [t for t in particles if t.size[0] != 0 and t.size[1] != 0]
    for trail in n_trails:
        pygame.draw.rect(draw_surface, (0, 0, 0, 0), trail, trail.width)
        r = trail
        if time_alive % decay_factor == 0:
            r = trail.scale_by(.99, .99)
        trail[:] = pygame.draw.rect(draw_surface, color, r, r.width)
    particles[:] = n_trails


# Update circle particles
def update_circle_particles(draw_surface: Surface, particles: list, time_alive: float, decay_factor: float = 2.0,
                            color=(255, 255, 255, 255)):
    n_trails = [t for t in particles if t.size[0] != 0 and t.size[1] != 0]
    for trail in n_trails:
        pygame.draw.rect(draw_surface, (0, 0, 0, 0), trail, trail.width)
        r = trail
        if time_alive % decay_factor == 0:
            r = trail.scale_by(.99, .99)
        trail[:] = pygame.draw.circle(draw_surface, color, trail.center, r.width // 2)
    particles[:] = n_trails

#
# End particle utils
#
