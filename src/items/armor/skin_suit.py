"""
Skin Suit armor for the roguelike game.
"""

from .base import Armor


class SkinSuit(Armor):
    """+1 DEF for every 4 enemies slain."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Skin Suit", '[', 0, description="+1 DEF for every 4 enemies slain")

    def get_defense_bonus(self, player):
        return super().get_defense_bonus(player) + int(player.body_count / 4)