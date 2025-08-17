"""
Removes all negative status effects.
"""

from constants import COLOR_GREEN
from ..consumable import Consumable


class Antidote(Consumable):
    """Removes all negative status effects"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Antidote",
            char='!',
            color=COLOR_GREEN,
            description="Removes all negative status effects",
            effect_value=1 
        )
    
    def use(self, player):
        """Remove all negative status effects from player"""
        if player.status_effects.has_negative_effects():
            player.status_effects.clear_negative_effects()
            return (True, "You feel cleansed! All negative status effects removed.")
        else:
            return (False, "You have no negative status effects to cure.")