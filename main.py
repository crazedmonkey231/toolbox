# Example file showing a circle moving on screen
import numpy
import pygame
from pygame.sprite import LayeredUpdates, GroupSingle, Group
import toolbox.util
from toolbox.player import Player
from toolbox.thing import Thing
from toolbox.group_config import render_sprites, player_group, enemy_group
from toolbox.resistry import asset_registry

# pygame setup
pygame.init()
fps = 120
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

asset_registry.load_image('fsh.png')

player: Player = Player()
thing: Thing = Thing()

render_sprites.add(player)
render_sprites.add(thing)

player_group.add(player)

enemy_group.add(thing)

thing.rect.center = (1280 // 2, 720 // 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    render_sprites.update(dt)

    render_sprites.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(fps) / 1000

pygame.quit()
