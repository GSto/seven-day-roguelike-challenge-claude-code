"""
Improves your eyesight.
"""

from constants import COLOR_ORANGE
from ..consumable import Consumable


class Carrot(Consumable):
    """Improves your eyesight"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Carrot",
            char='!',
            color=COLOR_ORANGE,
            description="Improves your eyesight",
            effect_value=3 
        )
    
    def use(self, player):
        """Increase the player's FOV."""
        player.fov += self.effect_value
        player.heal(10) # All food provides a little HP
        return (True, f"Your vision improves! FOV +{self.effect_value}")