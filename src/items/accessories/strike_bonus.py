"""
StrikeBonus - +6 ATK on strike attacks.
"""
from .hat import Hat
from traits import Trait


class StrikeBonus(Hat):
    """+6 ATK on strike attacks."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Strike Expertise", 
                        description="+6 ATK on strike attacks")
    
    def get_attack_bonus(self, player):
        pt = player.get_total_attack_traits()
        base_bonus = super().get_attack_bonus(player)
        if Trait.STRIKE in pt:
            return base_bonus + 6
        else:
            return base_bonus