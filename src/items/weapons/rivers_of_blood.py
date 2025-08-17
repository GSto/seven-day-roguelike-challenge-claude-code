"""
Rivers of Blood weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class RiversOfBlood(Weapon):
    """A legendary samurai warrior's blade."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Rivers of Blood", ')', 11, "A samurai warrior's blade", crit_bonus=0.20, crit_multiplier_bonus=0.25, attack_traits=[Trait.SLASH])