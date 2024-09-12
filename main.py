# Imports

# Mandatory imports. The web build will break without preloading these modules.
import numpy
import PIL

# Normal imports.
import pygame

from config import SCREEN_SIZE, FPS, RGB_WHITE, DEBUG
from toolbox import game_objects
from toolbox.achievment_system import Achievements
from toolbox.experiences.splash_screen import SplashScreen
import shared
from shared import renderer_group
from toolbox.resistry import AssetRegistry

# Quick print so imports aren't lost on refactor
if DEBUG:
    print(numpy)
    print(PIL)

# Systems setup
shared.asset_registry = AssetRegistry()
shared.achievement_system = Achievements()

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
images = ['fsh.png', 'bullet.png']
sounds = ['hello.wav']
gifs = ['fire.gif']


# Load assets
shared.asset_registry.load_registry(images, sounds, gifs)

# Starting Sprite
game_objects.change_experience(SplashScreen)

# Main loop
while shared.running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shared.running = False

    # Draw sprites to canvas
    shared.screen.fill(RGB_WHITE)
    renderer_group.update()
    renderer_group.draw(shared.screen)
    shared.screen.blit(shared.overlay, (0, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # Delta time
    shared.delta_time = shared.clock.tick(FPS) / shared.delta_slowdown

pygame.quit()
