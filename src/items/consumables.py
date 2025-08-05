"""
Consumable items like potions.
"""

from constants import COLOR_RED, COLOR_BLUE
from .base import Consumable


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
        # For UI display, we'll show percentage based on player's health_aspect
        self.heal_percentage = 30  # Default display value
    
    def use(self, player):
        """Restore player health based on player's health_aspect."""
        if player.hp >= player.max_hp:
            return False  # Already at full health
        
        old_hp = player.hp
        # Calculate healing based on effect_value * player's total health_aspect
        heal_amount = int(player.max_hp * (self.effect_value * player.get_total_health_aspect()))
        player.heal(heal_amount)
        actual_healing = player.hp - old_hp
        return actual_healing > 0


class ManaPotion(Consumable):
    """Mana restoration potion (for future magic system)."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Mana Potion",
            char='!',
            color=COLOR_BLUE,
            description="Restores mana when consumed",
            effect_value=20
        )
        self.heal_amount = self.effect_value  # For UI display consistency
    
    def use(self, player):
        """Restore player mana (placeholder for future magic system)."""
        # For now, just return True to indicate successful use
        return True