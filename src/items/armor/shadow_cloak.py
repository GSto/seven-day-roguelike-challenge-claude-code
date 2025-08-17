"""
Shadow Cloak armor for the roguelike game.
"""

from .base import Armor


class ShadowCloak(Armor):
    """Wearer is translucent, harder to see."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Shadow's Cloak", '[', 1, description="Wearer is transcluent, harder to see", evade_bonus=0.2)