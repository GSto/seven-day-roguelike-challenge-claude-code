"""
Makes you heartier.
"""

from constants import COLOR_RED
from ..consumable import Consumable


class Chicken(Consumable):
    """Makes you heartier"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Wall Chicken",
            char='c',
            color=COLOR_RED,
            description="Makes you heartier",
            effect_value=1 
        )
    
    def use(self, player):
        """Increase the player's max HP and attack."""
        player.max_hp += 10 
        player.heal(10)
        return (True, "You feel heartier! Max HP +10")