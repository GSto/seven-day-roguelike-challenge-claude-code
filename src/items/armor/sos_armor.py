"""
SOS Armor for the roguelike game.
"""

from .base import Armor


class SOSArmor(Armor):
    """+2 DEF. +6 DEF if HP is 20% or less of max HP"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "SOS Armor", '[', 2, 
        description="+2 DEF. +6 DEF if HP is 20% or less of max HP")
        self.market_value = 68  # Mid game uncommon armor
    
    def get_defense_bonus(self, player):
        """Get defense bonus with conditional extra defense at low HP."""
        base_defense = super().get_defense_bonus(player)
        if player.has_low_hp():
            return base_defense + 6
        return base_defense