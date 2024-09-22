from pygame import Surface, Clock
from pygame.sprite import Group, GroupSingle, LayeredUpdates

from toolbox.achievment_system import Achievements
from toolbox.level import Level
from toolbox.resistry import AssetRegistry
from toolbox.shop import Shop
from toolbox.stock_market import StockMarket

# Shared systems
asset_registry: AssetRegistry = None
achievement_system: Achievements = None
shop: Shop = None
stock_market: StockMarket = None
current_level: Level = None

# Pygame stuff
screen: Surface = None
underlay: Surface = None
overlay: Surface = None
clock: Clock = None
running: bool = True
delta_time: float = 0
delta_slowdown: float = 1000

# Main renderer
renderer_group: LayeredUpdates = LayeredUpdates()

# Player ref group
player_ref_group: GroupSingle = GroupSingle()

# Organizational Groups
enemy_group: Group = Group()
pickup_group: Group = Group()
effect_group: Group = Group()
projectile_group: Group = Group()
widget_group: Group = Group()
