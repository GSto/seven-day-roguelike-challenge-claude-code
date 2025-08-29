"""
Demon Slayer weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class DemonSlayer(Weapon):
    """Legendary weapon designed to slay demons."""

    def __init__(self, x, y):
        super().__init__(x, y, "Demon Slayer", ')', 15, "A legendary blade forged to slay demons", 
                         attack_traits=[Trait.DEMONSLAYER, Trait.SLASH])
        self.market_value = 70  # Late game common weapon (boss)