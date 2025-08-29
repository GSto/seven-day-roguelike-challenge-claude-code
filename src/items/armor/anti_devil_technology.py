"""
Anti-Devil Technology armor for the roguelike game.
"""

from .base import Armor
from traits import Trait


class AntiDevilTechnology(Armor):
    """Mid-game armor. +4 DEF. Holy resistance, immune to blindness."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Anti-Devil Armor", '[', 4, 
        description="+4 DEF. Dark resistance, cannot be frightened",
                        resistances=[Trait.DARK])
        self.market_value = 68  # Mid game uncommon armor
    
    def blocks_status_effect(self, effect_name):
        """Check if this armor blocks a specific status effect."""
        return effect_name in ['frightened']