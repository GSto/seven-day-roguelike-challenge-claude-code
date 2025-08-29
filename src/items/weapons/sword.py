"""
Sword weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class Sword(Weapon):
    """Balanced weapon for mid-game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Sword", ')', 5, "A well-balanced sword", attack_traits=[Trait.SLASH])
        self.market_value = 25  # Early game common weapon