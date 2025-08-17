"""
War Hammer weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class WarHammer(Weapon):
    """Heavy weapon for maximum damage."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "War Hammer", ')', 12, "A heavy war hammer", attack_traits=[Trait.STRIKE])