"""
Permanently increases crit chance.
"""

from constants import COLOR_RED
from .catalyst import Catalyst


class ReapersCatalyst(Catalyst):
    """Permanently increases crit chance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Reaper's Catalyst",
            char='*',
            color=COLOR_RED,
            description="Permanently increases crit chance by 5%",
            effect_value=0.05
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's crit chance"""
        player.crit += self.effect_value
        return (True, f"You feel deadlier! Crit chance +{int(self.effect_value * 100)}% (Cost: {hp_cost} HP)")