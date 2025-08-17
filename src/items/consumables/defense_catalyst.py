"""
Permanently increases defense.
"""

from constants import COLOR_BLUE
from .catalyst import Catalyst


class DefenseCatalyst(Catalyst):
    """Permanently increases defense"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Defender's Catalyst",
            char='*',
            color=COLOR_BLUE,
            description="Permanently increases defense by 1",
            effect_value=1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's defense"""
        player.defense += self.effect_value
        return (True, f"You feel more protected! Defense +{self.effect_value} (Cost: {hp_cost} HP)")