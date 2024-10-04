# Imports

# Mandatory imports. The web build will break without preloading these modules.
import numpy
import PIL

# Normal imports.
import pygame
import shared
from config import SCREEN_SIZE, FPS, DEBUG, RGB_BLACK
from toolbox.levels.test_level import TestLevel
from toolbox.systems.achievement.achievments import Achievements
from toolbox.levels.splash_screen import SplashScreen
from shared import renderer_group
from toolbox.resistry import AssetRegistry
import toolbox.util

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
images = ['fsh.png', 'bullet.png', 'test_wall.png', 'npc.png']
sounds = ['hello.wav']
gifs = ['fire.gif']


# Load assets
shared.asset_registry.load_registry(images, sounds, gifs)

# Load splash screen
# toolbox.util.change_level(SplashScreen)
toolbox.util.change_level(TestLevel)

# shared.mouse_grabbed = True
toolbox.util.mouse_grab(shared.mouse_grabbed)

# Main loop
while shared.running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shared.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                shared.mouse_grabbed = not shared.mouse_grabbed
                toolbox.util.mouse_grab(shared.mouse_grabbed)

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

    # Realtime variables
    shared.time_running_sec += shared.delta_time
    shared.time_running_min = shared.time_running_sec / 60
    shared.time_running_hour = shared.time_running_min / 60

pygame.quit()
