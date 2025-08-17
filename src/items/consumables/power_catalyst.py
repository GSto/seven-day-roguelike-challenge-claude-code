"""
Permanently increases attack power.
"""

from constants import COLOR_RED
from .catalyst import Catalyst


class PowerCatalyst(Catalyst):
    """Permanently increases attack power"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Warrior's Catalyst",
            char='*',
            color=COLOR_RED,
            description="Permanently increases attack by 1",
            effect_value=1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's attack"""
        player.attack += self.effect_value
        return (True, f"You feel more powerful! Attack +{self.effect_value} (Cost: {hp_cost} HP)")