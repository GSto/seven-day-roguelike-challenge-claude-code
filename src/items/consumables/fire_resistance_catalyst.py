"""
Permanently adds Fire resistance.
"""

from constants import COLOR_ORANGE
from .catalyst import Catalyst
from traits import Trait


class FireResistanceCatalyst(Catalyst):
    """Permanently adds Fire resistance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Salamander Catalyst",
            char='*',
            color=COLOR_ORANGE,
            description="Permanently adds Fire resistance",
            effect_value=1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Add Fire resistance to player"""
        if Trait.FIRE not in player.resistances:
            player.resistances.append(Trait.FIRE)
        return (True, f"You feel protected against fire! (Cost: {hp_cost} HP)")