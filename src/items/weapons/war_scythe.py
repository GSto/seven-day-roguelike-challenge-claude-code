"""
War Scythe weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class WarScythe(Weapon):
    """Heavy weapon for maximum damage."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "War Scythe", ')', 12, "A long, brutal weapon", attack_traits=[Trait.SLASH])