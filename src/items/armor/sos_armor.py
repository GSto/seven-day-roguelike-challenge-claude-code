"""
SOS Armor for the roguelike game.
"""

from .base import Armor


class SOSArmor(Armor):
    """+2 DEF. +6 DEF if HP is 20% or less of max HP"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "SOS Armor", '[', 2, 
                        description="+2 DEF. +6 DEF if HP is 20% or less of max HP")
    
    def get_defense_bonus(self, player):
        """Get defense bonus with conditional extra defense at low HP."""
        base_defense = super().get_defense_bonus(player)
        if player.hp <= (player.max_hp * 0.2):  # 20% or less HP
            return base_defense + 6
        return base_defense