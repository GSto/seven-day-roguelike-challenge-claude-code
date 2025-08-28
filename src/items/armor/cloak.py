"""
Cloak armor for the roguelike game.
"""

from .base import Armor


class Cloak(Armor):
    """Shadow black cloak, hard to see."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Cloak", '[', 1, description="Shadow black, hard to see", evade_bonus=0.10)