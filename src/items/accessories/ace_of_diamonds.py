"""
AceOfDiamonds - 2x XP if 20% HP or less.
"""
from .card import Card


class AceOfDiamonds(Card):
    
    def __init__(self, x, y):
        super().__init__(x,y, "Ace of Diamonds", description="2x XP if low health")
        self.market_value = 38  # Uncommon accessory (card)

    def get_xp_multiplier_bonus(self, player):
        if(player.has_low_hp()):
            return 2
        else:
            return 1