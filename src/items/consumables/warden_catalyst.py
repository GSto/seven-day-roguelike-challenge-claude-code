"""
Permanently increases defense multiplier by 10%.
"""

from constants import COLOR_BLUE
from .catalyst import Catalyst


class WardenCatalyst(Catalyst):
    """Permanently increases defense multiplier by 10%"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Warden's Catalyst",
            char='!',
            color=COLOR_BLUE,
            description="Permanently increases defense multiplier by 10%",
            effect_value=0.1,
            defense_multiplier_effect=1.1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's defense multiplier"""
        player.defense_multiplier *= self.defense_multiplier_effect
        return (True, f"Your defenses become more effective! Defense multiplier increased by {int((self.defense_multiplier_effect-1)*100)}% (Cost: {hp_cost} HP)")