"""
Fully restores health.
"""

from constants import COLOR_RED
from ..consumable import Consumable


class Elixir(Consumable):
    """Fully restores health"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Elixir",
            char='!',
            color=COLOR_RED,
            description="Restores all health",
            effect_value=1  # Multiplier for player's health_aspect
        )
    
    def use(self, player):
        """Restore player health based on player's health_aspect."""
        if player.hp >= player.max_hp:
            return (False, "You are already at full health!")
        
        old_hp = player.hp
        # Calculate healing based on effect_value * player's total health_aspect
        heal_amount = player.max_hp
        player.heal(heal_amount)
        actual_healing = player.hp - old_hp
        if actual_healing > 0:
            return (True, f"You recovered {actual_healing} HP and feel fully restored!")
        return (False, "The elixir had no effect.")