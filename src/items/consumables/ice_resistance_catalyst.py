"""
Permanently adds Ice resistance.
"""

from constants import COLOR_BLUE
from .catalyst import Catalyst
from traits import Trait


class IceResistanceCatalyst(Catalyst):
    """Permanently adds Ice resistance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Yeti Catalyst",
            char='*',
            color=COLOR_BLUE,
            description="Permanently adds Ice resistance",
            effect_value=1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Add Ice resistance to player"""
        if Trait.ICE not in player.resistances:
            player.resistances.append(Trait.ICE)
        return (True, f"You feel protected against ice! (Cost: {hp_cost} HP)")