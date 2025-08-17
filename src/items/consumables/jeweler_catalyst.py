"""
Permanently increases XP multiplier by 20%.
"""

from constants import COLOR_WHITE
from .catalyst import Catalyst


class JewelerCatalyst(Catalyst):
    """Permanently increases XP multiplier by 20%"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Jeweler's Catalyst",
            char='!',
            color=COLOR_WHITE,
            description="Permanently increases XP multiplier by 5%",
            effect_value=0.05,
            xp_multiplier_effect=1.05
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's XP multiplier"""
        player.xp_multiplier *= self.xp_multiplier_effect
        return (True, f"You learn more efficiently! XP multiplier increased by {int((self.xp_multiplier_effect-1)*100)}% (Cost: {hp_cost} HP)")