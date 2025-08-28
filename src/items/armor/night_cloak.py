"""
Night Cloak armor for the roguelike game.
"""

from .base import Armor


class NightCloak(Armor):
    """Vanta black cloak, harder to see."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Night Cloak", '[', 1, description="Vanta black, harder to see", evade_bonus=0.2)