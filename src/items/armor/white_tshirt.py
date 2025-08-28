"""
White T-Shirt armor for the roguelike game.
"""

from .base import Armor


class WhiteTShirt(Armor):
    """Basic starting armor."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "White T-Shirt", '[', 0, "A plain white T-shirt")