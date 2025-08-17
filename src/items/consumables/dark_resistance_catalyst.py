"""
Permanently adds Dark resistance.
"""

from constants import COLOR_SALMON
from .catalyst import Catalyst
from traits import Trait


class DarkResistanceCatalyst(Catalyst):
    """Permanently adds Dark resistance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Demon Catalyst",
            char='*',
            color=COLOR_SALMON,
            description="Permanently adds Dark resistance",
            effect_value=1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Add Dark resistance to player"""
        if Trait.DARK not in player.resistances:
            player.resistances.append(Trait.DARK)
        return (True, f"You feel protected against darkness! (Cost: {hp_cost} HP)")