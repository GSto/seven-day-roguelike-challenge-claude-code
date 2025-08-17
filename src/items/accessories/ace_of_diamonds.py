"""
AceOfDiamonds - 2x XP if 20% HP or less.
"""
from .card import Card


class AceOfDiamonds(Card):
    
    def __init__(self, x, y):
        super().__init__(x,y, "Ace of Hearts", description="2x XP if 20% HP or less")

    def get_xp_multiplier_bonus(self, player):
        if(player.hp <= (player.max_hp / 5)):
            return 2
        else:
            return 0