"""
Wooden Stick weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class WoodenStick(Weapon):
    """Basic starting weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Wooden Stick", ')', 1, "A simple wooden stick", attack_traits=[Trait.STRIKE])