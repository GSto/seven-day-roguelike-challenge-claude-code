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
            description="Restores 30% of max health when consumed",
            effect_value=0.3  # 30% as a decimal
        )
        # For UI display, we'll show percentage instead of fixed amount
        self.heal_percentage = 30  # 30%
    
    def use(self, player):
        """Restore player health by 30% of max HP."""
        if player.hp >= player.max_hp:
            return False  # Already at full health
        
        old_hp = player.hp
        # Calculate 30% of max HP
        heal_amount = int(player.max_hp * self.effect_value)
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