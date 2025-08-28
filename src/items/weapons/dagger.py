"""
Dagger weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class Dagger(Weapon):
    """Light, fast weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Dagger", ')', 3, "A sharp dagger. free to equip", crit_multiplier_bonus=0.5, attack_traits=[Trait.SLASH])