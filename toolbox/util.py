from collections import defaultdict
import numpy
from numpy import ndarray
import pygame
from pygame import Surface, Rect
from pygame.sprite import Sprite, AbstractGroup
from PIL import Image
from PIL.GifImagePlugin import GifImageFile

DEBUG = False

mixer_initialized = pygame.mixer or pygame.mixer.get_init()
if not mixer_initialized:
    print("Warning, sound disabled")
if not pygame.font:
    print("Warning, fonts disabled")


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


# Sound loader
def load_sound(audio_path, play_on_load=False) -> object:
    if not mixer_initialized:
        class NoneSound(object):
            def play(self):
                pass
        sound = NoneSound()
    else:
        sound = pygame.mixer.Sound(audio_path)
    if play_on_load:
        if hasattr(sound, 'play'):
            play = getattr(sound, 'play')
            play()
    return sound


# Image loader
def load_image(image_path, color_key=None, scale=1) -> tuple[Surface, Rect]:
    image = pygame.image.load(image_path).convert_alpha()
    size = image.get_size()
    image = pygame.transform.scale(image, (size[0] * scale, size[1] * scale))
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key, pygame.RLEACCEL)
    return image, image.get_rect()


# Gif loader
def load_gif(gif_path) -> list[Surface]:
    ret = []
    gif: GifImageFile = Image.open(gif_path)
    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_rgba = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
        )
        ret.append(pygame_image)
    return ret


# Rotate image
def rotate_image(original_image: Surface, angle: float, center) -> tuple[Surface, Rect]:
    rotated_image = pygame.transform.rotate(original_image, angle)
    new_rect = rotated_image.get_rect(center=center)
    return rotated_image, new_rect


# Scale image basic
def scale_image(original_image: Surface, new_size: tuple, center) -> tuple[Surface, Rect]:
    new_image = pygame.transform.scale(original_image, new_size)
    new_rect = new_image.get_rect(center=center)
    return new_image, new_rect


# Scale image smooth
def scale_image_smooth(original_image: Surface, new_size: tuple, center) -> tuple[Surface, Rect]:
    new_image = pygame.transform.smoothscale(original_image, new_size)
    new_rect = new_image.get_rect(center=center)
    return new_image, new_rect


# Interpolates between color1 and color2 using a factor.
def interpolate_color_rgba(color1, color2, factor) -> tuple[int, int, int, int]:
    r1, g1, b1, a1 = color1
    r2, g2, b2, a2 = color2
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    a = int(a1 + (a2 - a1) * factor)
    return r, g, b, a


# Simple text maker
def make_simple_text(text: str, size: int = 64, color: tuple[int, int, int] = (255, 255, 255)) -> tuple[Surface, Rect]:
    font = pygame.font.Font(None, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    return text, text_rect


# Particle functions
# Needs trail attribute and draw surface set up, using screen surface will cause unwanted overwriting.

# Create initial rect particle
def create_rect_particle(draw_surface: Surface, particles: list, color, rect: Rect, size: tuple, width: float):
    particles.append(pygame.draw.rect(draw_surface, color, (rect.left, rect.top, size[0], size[1]), width))


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
        pygame.draw.circle(draw_surface, (0, 0, 0, 0), trail.center, trail.width, trail.width)
        r = trail
        if time_alive % decay_factor == 0:
            r = trail.scale_by(.99, .99)
        trail[:] = pygame.draw.circle(draw_surface, color, trail.center, r.width / 2, r.width)
    particles[:] = n_trails
