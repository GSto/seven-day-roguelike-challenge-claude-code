"""
Chain Mail armor for the roguelike game.
"""

from .base import Armor


class ChainMail(Armor):
    """Medium armor for mid-game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Chain Mail", '[', 2, description="Flexible chain mail armor")