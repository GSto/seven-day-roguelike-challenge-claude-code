"""
Permanently adds Holy resistance.
"""

from constants import COLOR_WHITE
from .catalyst import Catalyst
from traits import Trait


class HolyResistanceCatalyst(Catalyst):
    """Permanently adds Holy resistance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Angel Catalyst",
            char='*',
            color=COLOR_WHITE,
            description="Permanently adds Holy resistance",
            effect_value=1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Add Holy resistance to player"""
        if Trait.HOLY not in player.resistances:
            player.resistances.append(Trait.HOLY)
        return (True, f"You feel protected against holy light! (Cost: {hp_cost} HP)")