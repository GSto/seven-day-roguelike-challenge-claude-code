"""
Permanently increases attack multiplier by 10%.
"""

from constants import COLOR_YELLOW
from .catalyst import Catalyst


class BaronCatalyst(Catalyst):
    """Permanently increases attack multiplier by 10%"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Baron's Catalyst",
            char='!',
            color=COLOR_YELLOW,
            description="Permanently increases attack multiplier by 10%",
            effect_value=0.1,
            attack_multiplier_effect=1.1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's attack multiplier"""
        player.attack_multiplier *= self.attack_multiplier_effect
        return (True, f"Your attacks become more effective! Attack multiplier increased by {int((self.attack_multiplier_effect-1)*100)}% (Cost: {hp_cost} HP)")