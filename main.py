# Imports

# Mandatory imports. The web build will break without preloading these modules.
import numpy
import PIL

# Normal imports.
import pygame
from pygame import Surface

import toolbox.util
from config import SCREEN_SIZE, CANVAS_SIZE, FPS, RGB_WHITE
from toolbox.player import Player
from toolbox.group_config import renderer_group, player_ref_group
from toolbox.resistry import asset_registry
from toolbox.thing import Thing

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
# Load starting sprites
#
def load_starting_sprites():
    player: Player = Player((200, 200), player_ref_group)
    renderer_group.add(player)

    t = Thing()
    t.rect.center = (500, 500)
    renderer_group.add(t)
    pass


load_starting_sprites()


#
# Main loop
#
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            renderer_group.update_zoom_scale(event.y)

    loc = renderer_group.mouse_pos_to_global_pos(pygame.mouse.get_pos())
    print(loc)
    for i in renderer_group.sprites():
        if i.rect.collidepoint(loc):
            print('overlap')

    # Draw sprites to canvas
    canvas.fill(RGB_WHITE)
    renderer_group.update(delta_time, canvas)
    renderer_group.draw(canvas)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # Delta time
    delta_time = clock.tick(FPS) / 1000

pygame.quit()
