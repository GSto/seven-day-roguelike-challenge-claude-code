"""
Coated Plate armor for the roguelike game.
"""

from .base import Armor


class CoatedPlate(Armor):
    """+4 DEF. Immune to poison, burn, stun."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Coated Plate", '[', 4, 
        description="Mid-game+ armor. +4 DEF. Immune to poison, burn, stun")
        self.market_value = 45  # Mid game common armor
    
    def blocks_status_effect(self, effect_name):
        """Check if this armor blocks a specific status effect."""
        return effect_name in ['poison', 'burn', 'stun']