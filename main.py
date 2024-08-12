# Imports

# Mandatory imports. The web build will break without preloading these modules.
import numpy
import PIL

# Normal imports.
import pygame
from pygame import Surface
from config import SCREEN_SIZE, CANVAS_SIZE, FPS
from toolbox.player import Player
from toolbox.group_config import render_sprites, player_group
from toolbox.resistry import asset_registry

# pygame setup

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
canvas = Surface(CANVAS_SIZE).convert_alpha()
clock = pygame.time.Clock()
running = True
delta_time = 0

asset_registry.load_image('fsh.png')
asset_registry.load_sound('hello.wav')

player: Player = Player((200, 200), player_group)
render_sprites.add(player)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw sprites to canvas
    canvas.fill("purple")
    render_sprites.update(delta_time, canvas)
    render_sprites.draw(canvas)

    # Draw subsection of canvas to screen
    screen.fill('white')
    screen.blit(canvas, (0, 0), (player.rect.centerx - 640, player.rect.centery - 360, 1280, 720))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # Delta time
    delta_time = clock.tick(FPS) / 1000

pygame.quit()
