"""
Uchigatana weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class Uchigatana(Weapon):
    """A samurai warrior's blade."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Uchigatana", ')', 7, "A samurai warrior's blade", crit_bonus=0.15, attack_traits=[Trait.SLASH])