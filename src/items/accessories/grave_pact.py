"""
GravePact - +6 ATK on Dark and Ice.
"""
from .hat import Hat
from traits import Trait


class GravePact(Hat):
    """+6 ATK on Dark and Ice."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Grave Pact", 
        description="+6 ATK for cold and dark attack")
        self.market_value = 38  # Uncommon accessory
    
    def get_attack_bonus(self, player):
        pt = player.get_total_attack_traits()
        base_bonus = super().get_attack_bonus(player)
        if Trait.DARK in pt or Trait.ICE in pt:
            return base_bonus + 6
        else:
            return base_bonus