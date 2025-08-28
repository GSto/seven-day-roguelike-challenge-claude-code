"""
Permanently increases evade chance.
"""

from constants import COLOR_BLUE
from .catalyst import Catalyst


class ShadowsCatalyst(Catalyst):
    """Permanently increases evade chance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Shadow's Catalyst",
            char='*',
            color=COLOR_BLUE,
            description="Permanently increases evade chance by 5%",
            effect_value=0.08
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's evade chance"""
        player.evade += self.effect_value
        return (True, f"You feel more agile! Evade chance +{int(self.effect_value * 100)}% (Cost: {hp_cost} HP)")