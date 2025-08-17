"""
Axe weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class Axe(Weapon):
    """Balanced weapon for mid-game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Axe", ')', 6, "An axe", attack_traits=[Trait.STRIKE])