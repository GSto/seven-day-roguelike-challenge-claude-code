"""
Anti-Angel Technology armor for the roguelike game.
"""

from .base import Armor
from traits import Trait


class AntiAngelTechnology(Armor):
    """Mid-game armor. +4 DEF. Holy resistance, immune to blindness."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Anti-Angel Technology", '[', 4, 
                        description="Mid-game armor. +4 DEF. Holy resistance, immune to blindness",
                        resistances=[Trait.HOLY])
    
    def blocks_status_effect(self, effect_name):
        """Check if this armor blocks a specific status effect."""
        return effect_name in ['blindness']