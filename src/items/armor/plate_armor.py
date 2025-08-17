"""
Plate Armor for the roguelike game.
"""

from .base import Armor


class PlateArmor(Armor):
    """Heavy armor for late game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Plate Armor", '[', 3, description="Heavy plate armor")