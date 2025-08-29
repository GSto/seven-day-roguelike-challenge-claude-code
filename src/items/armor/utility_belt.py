"""
Utility Belt armor for the roguelike game.
"""

from .base import Armor


class UtilityBelt(Armor):
    """Mid-game+ armor. +3 DEF, +10% healing, +10% XP, +3 FOV"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Utility Belt", '[', 3, 
        description="Mid-game+ armor. +3 DEF, +10% healing, +10% XP, +3 FOV",
                        fov_bonus=3,
                        health_aspect_bonus=0.1,
                        xp_multiplier_bonus=1.1)
        self.market_value = 90  # Mid game rare armor