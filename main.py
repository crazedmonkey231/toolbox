# Imports

# Mandatory imports. The web build will break without preloading these modules.
import numpy
import PIL

# Normal imports.
import pygame
from config import SCREEN_SIZE, FPS, RGB_WHITE
from toolbox.sprites.gameplayer import GamePlayer
from shared import renderer_group
from toolbox.resistry import asset_registry
import shared

# Quick print so imports aren't lost on refactor
print(numpy)
print(PIL)

#
# pygame setup
#
pygame.init()
shared.screen = pygame.display.set_mode(SCREEN_SIZE)
shared.overlay = shared.screen.copy().convert_alpha()
shared.overlay.fill((0, 0, 0, 0))
shared.clock = pygame.time.Clock()


#
# Load Registry
#
images = ['fsh.png']
sounds = ['hello.wav']
gifs = []


# Load assets
asset_registry.load_registry(images, sounds, gifs)

# Starting Sprite
GamePlayer((200, 200))

# Main loop
while shared.running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shared.running = False

    # Draw sprites to canvas
    shared.screen.fill(RGB_WHITE)
    renderer_group.update()
    shared.screen.blit(shared.overlay, (0, 0))
    renderer_group.draw(shared.screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # Delta time
    shared.delta_time = shared.clock.tick(FPS) / 1000

pygame.quit()
