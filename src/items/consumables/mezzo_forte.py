"""
Grants 10 shields but reduces HP to 1.
"""

from constants import COLOR_YELLOW
from ..consumable import Consumable


class MezzoForte(Consumable):
    """Grants 10 shields but reduces HP to 1"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Mezzo Forte",
            char='!',
            color=COLOR_YELLOW,
            description="Grants 10 shields but reduces your HP to 1",
            effect_value=10
        )
    
    def use(self, player):
        """Grant many shields but reduce HP to 1"""
        
        player.status_effects.apply_status('shields', self.effect_value, player)
        player.hp = 1
        return (True, f"You feel incredibly protected but fragile! Gained {self.effect_value} shields, HP reduced to 1.")