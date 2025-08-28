"""
Stone Armor
"""

from .base import Armor
from traits import Trait


class StoneArmor(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Stone Armor", '[', 3, 
                        description="Mid-game armor. +3 DEF. Immunity to stun, immobilized, and off-guard")
    
    def blocks_status_effect(self, effect_name):
        """Check if this armor blocks a specific status effect."""
        return effect_name in ['stun', 'immobilized', 'off-guard']