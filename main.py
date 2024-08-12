# Imports

# Mandatory imports. The web build will break without preloading these modules.
import numpy
import PIL

# Normal imports.
import pygame
from pygame import Surface
from config import SCREEN_SIZE, CANVAS_SIZE, FPS, RGB_WHITE
from toolbox.player import Player
from toolbox.group_config import render_sprites, player_group
from toolbox.resistry import asset_registry

#
# pygame setup
#
pygame.init()
pygame.display.set_mode(SCREEN_SIZE)
canvas = Surface(CANVAS_SIZE).convert_alpha()
clock = pygame.time.Clock()
running = True
delta_time = 0


#
# Load Registry
#
def load_registry():
    images: list[str] = ['fsh.png']
    for image in images:
        asset_registry.load_image(image)

    sounds: list[str] = ['hello.wav']
    for sound in sounds:
        asset_registry.load_sound(sound)

    gifs: list[str] = []
    for gif in gifs:
        asset_registry.load_gif(gif)


load_registry()

#
# Test Sprites area
#
player: Player = Player((200, 200), player_group)
render_sprites.add(player)

#
# Main loop
#
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw sprites to canvas
    canvas.fill(RGB_WHITE)
    render_sprites.update(delta_time, canvas)
    render_sprites.draw(canvas)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # Delta time
    delta_time = clock.tick(FPS) / 1000

pygame.quit()
