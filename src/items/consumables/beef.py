"""
Makes you heartier.
"""

from constants import COLOR_RED
from ..consumable import Consumable


class Beef(Consumable):
    """Makes you heartier"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Beef",
            char='b',
            color=COLOR_RED,
            description="Makes you heartier",
            effect_value=20
        )
    
    def use(self, player):
        """Increase the player's max HP and attack."""
        player.max_hp += self.effect_value 
        player.attack += 1
        player.heal(5)
        return (True, "You feel heartier! Max HP +20, Attack +1")