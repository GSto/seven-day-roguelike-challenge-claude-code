"""
Gambler's Vest armor for the roguelike game.
"""

import random
from .base import Armor


class GamblersVest(Armor):
    """Double or 0.5x on defense."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Gambler's Vest", '[', 0, description="Double or 0.5x on defense")
        self.market_value = 68  # All-level uncommon armor

    def get_defense_multiplier_bonus(self, player):
        base = super().get_defense_multiplier_bonus(player)
        rand = random.random()
        if rand <= 0.5:
            return base + 1.0  # 2x total (base 1.0 + 1.0 bonus)
        else:
            return base - 0.5  # 0.5x total (base 1.0 - 0.5 penalty)