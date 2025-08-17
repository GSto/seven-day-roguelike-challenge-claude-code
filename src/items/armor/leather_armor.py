"""
Leather Armor for the roguelike game.
"""

from .base import Armor


class LeatherArmor(Armor):
    """Light armor for early game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Leather Armor", '[', 1, description="Basic leather protection. Free to equip", xp_cost=0)