from pygame.sprite import Group, GroupSingle
from toolbox.camera import CameraRenderer

#
# Main renderer
#
renderer_group: CameraRenderer = CameraRenderer()

#
# Player ref group
#
player_ref_group: GroupSingle = GroupSingle()

#
# Organizational Groups
#
enemy_group: Group = Group()
pickup_group: Group = Group()
effect_group: Group = Group()
projectile_group: Group = Group()
widget_group: Group = Group()
button_group: Group = Group()
