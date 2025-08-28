"""
Minimal Suit armor for the roguelike game.
"""

from .base import Armor


class MinimalSuit(Armor):
    """More evade the lighter you are."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Traveler's Garb", '[', 0, description="More evade the lighter you are")

    def get_evade_bonus(self, player):
        inventory_space = player.inventory_size - len(player.inventory)
        return super().get_evade_bonus(player) + (inventory_space / 50)