# Imports

# Mandatory imports. The web build will break without preloading these modules.
import numpy
import PIL

# Normal imports.
import pygame

from config import SCREEN_SIZE, FPS, DEBUG, RGB_BLACK
import toolbox
from toolbox.systems.achievement.achievments import Achievements
from toolbox.levels.splash_screen import SplashScreen
import shared
from shared import renderer_group
from toolbox.resistry import AssetRegistry
from toolbox.systems.exchange.exchange import Exchange

# Quick print so imports aren't lost on refactor
if DEBUG:
    print(numpy)
    print(PIL)

# Asset registry
shared.asset_registry = AssetRegistry()

# Achievement system
shared.achievement_system = Achievements()

#
# pygame setup
#
pygame.init()

shared.screen = pygame.display.set_mode(SCREEN_SIZE)

shared.overlay = shared.screen.copy().convert_alpha()
shared.overlay.fill((0, 0, 0, 0))

shared.underlay = shared.screen.copy().convert_alpha()
shared.underlay.fill((0, 0, 0, 0))

shared.clock = pygame.time.Clock()

#
# Load Registry
#
images = ['fsh.png', 'bullet.png']
sounds = ['hello.wav']
gifs = ['fire.gif']


# Load assets
shared.asset_registry.load_registry(images, sounds, gifs)

# Load splash screen
toolbox.util.change_level(SplashScreen)

# Main loop
while shared.running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shared.running = False

    # Draw sprites to canvas
    shared.screen.fill(RGB_BLACK)
    shared.screen.blit(shared.underlay, (0, 0))
    renderer_group.update()
    renderer_group.draw(shared.screen)
    shared.screen.blit(shared.overlay, (0, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # Delta time
    shared.delta_time = shared.clock.tick(FPS) / shared.delta_slowdown

pygame.quit()
