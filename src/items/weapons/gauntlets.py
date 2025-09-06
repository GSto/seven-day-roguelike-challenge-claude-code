"""
Gauntlets weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class Gauntlets(Weapon):
    """Gloves that enhance your natural strength."""

    def __init__(self, x, y):
        super().__init__(x, y, "Gauntlets", ')', 0, "Enhances natural strength", attack_multiplier_bonus=1.75, attack_traits=[Trait.THWACK])