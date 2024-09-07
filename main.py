# Imports

# Mandatory imports. The web build will break without preloading these modules.
import numpy
import PIL

# Normal imports.
import pygame
from config import SCREEN_SIZE, FPS, RGB_WHITE
from toolbox.fpsplayer import FpsPlayer
from toolbox.group_config import renderer_group
from toolbox.resistry import asset_registry

#
# pygame setup
#
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True
delta_time = 0


#
# Load Registry
#
images = ['fsh.png']
sounds = ['hello.wav']
gifs = []


# Load assets
asset_registry.load_registry(images, sounds, gifs)

# Starting Sprite
FpsPlayer((200, 200))

# Main loop
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw sprites to canvas
    screen.fill(RGB_WHITE)
    renderer_group.update(screen, delta_time)
    renderer_group.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # Delta time
    delta_time = clock.tick(FPS) / 1000

pygame.quit()
