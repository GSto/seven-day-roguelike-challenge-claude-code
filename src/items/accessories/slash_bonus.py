"""
SlashBonus - +6 ATK on slash attacks.
"""
from .hat import Hat
from traits import Trait


class SlashBonus(Hat):
    """+6 ATK on slash attacks."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Blade Expertise", 
                        description="+6 ATK on slash attacks")
    
    def get_attack_bonus(self, player):
        pt = player.get_total_attack_traits()
        base_bonus = super().get_attack_bonus(player)
        if Trait.SLASH in pt:
            return base_bonus + 6
        else:
            return base_bonus