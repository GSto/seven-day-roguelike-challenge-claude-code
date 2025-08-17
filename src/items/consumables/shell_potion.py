"""
Grants 3 shields.
"""

from constants import COLOR_CYAN
from ..consumable import Consumable


class ShellPotion(Consumable):
    """Grants 3 shields"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Shell Potion",
            char='!',
            color=COLOR_CYAN,
            description="Grants 3 protective shields",
            effect_value=3
        )
    
    def use(self, player):
        """Grant shields to player"""
        player.status_effects.apply_status('shields', self.effect_value, player)
        return (True, f"You feel protected! Gained {self.effect_value} shields.")