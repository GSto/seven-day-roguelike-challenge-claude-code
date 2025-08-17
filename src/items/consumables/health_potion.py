"""
Health restoration potion.
"""

from constants import COLOR_RED
from ..consumable import Consumable


class HealthPotion(Consumable):
    """Health restoration potion."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Health Potion",
            char='!',
            color=COLOR_RED,
            description="Restores health when consumed",
            effect_value=1  # Multiplier for player's health_aspect
        )
    
    def use(self, player):
        """Restore player health based on player's health_aspect."""
        if player.hp >= player.max_hp:
            return (False, "You are already at full health!")
        
        old_hp = player.hp
        # Calculate healing based on effect_value * player's total health_aspect
        heal_amount = int(player.max_hp * (self.effect_value * player.get_total_health_aspect()))
        player.heal(heal_amount)
        actual_healing = player.hp - old_hp
        if actual_healing > 0:
            return (True, f"You recovered {actual_healing} HP!")
        return (False, "The potion had no effect.")