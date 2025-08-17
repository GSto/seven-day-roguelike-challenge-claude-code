"""
Gain insight.
"""

from constants import COLOR_SALMON
from ..consumable import Consumable


class SalmonOfKnowledge(Consumable):
    """Gain insight"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Salmon of Knowledge",
            char='!',
            color=COLOR_SALMON,
            description="Gain insight",
            effect_value=50 
        )
    
    def use(self, player):
        """Player gains XP"""
        player.heal(5)
        player.gain_xp(self.effect_value)
        return (True, f"You gain {self.effect_value} XP from ancient wisdom!")