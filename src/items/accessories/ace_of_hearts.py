"""
AceOfHearts - 2x attack if at full health.
"""
from .card import Card


class AceOfHearts(Card):
        def __init__(self, x, y):
          super().__init__(x, y, "Ace of Hearts", description="2x attack if high health")

        def get_attack_multiplier_bonus(self, player):
            if(player.has_high_hp()): 
                return 2
            else: 
                return 1