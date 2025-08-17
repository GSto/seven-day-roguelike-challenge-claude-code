"""
Pickaxe weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class Pickaxe(Weapon):
    """Favorite of Miners, scales with light."""

    def __init__(self, x, y):
        super().__init__(x, y, "Pickaxe", ')', 6, "Favorite of Miners, scales with light", attack_traits=[Trait.STRIKE])

    def get_attack_multiplier_bonus(self, player):
        return min(1, 1 + (player.get_total_fov() / 100))  # return 1 so we don't accidentally scale down