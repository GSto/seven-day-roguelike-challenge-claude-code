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
            effect_value=30
        )
        self.heal_amount = self.effect_value  # For UI display
    
    def use(self, player):
        """Restore player health."""
        if player.hp >= player.max_hp:
            return False  # Already at full health
        
        old_hp = player.hp
        player.heal(self.effect_value)
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