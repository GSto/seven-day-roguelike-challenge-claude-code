"""
Katana weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class Katana(Weapon):
    """Critical chance based weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Katana", ')', 4, "A light, fast blade", crit_bonus=0.15, attack_traits=[Trait.SLASH])
        self.market_value = 38  # Early game uncommon weapon (25 * 1.5)