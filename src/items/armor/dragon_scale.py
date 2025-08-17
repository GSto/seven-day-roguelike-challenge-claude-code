"""
Dragon Scale armor for the roguelike game.
"""

from .base import Armor


class DragonScale(Armor):
    """Legendary armor from dragon materials."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Dragon Scale Armor", '[', 5, description="Legendary dragon scale armor")