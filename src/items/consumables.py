"""
Consumable items like potions.
"""

from constants import COLOR_RED, COLOR_BLUE, COLOR_ORANGE, COLOR_SALMON
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
            return False  # Already at full health
        
        old_hp = player.hp
        # Calculate healing based on effect_value * player's total health_aspect
        heal_amount = player.max_hp
        player.heal(heal_amount)
        actual_healing = player.hp - old_hp
        return actual_healing > 0

class Beef(Consumable):
    """Makes you heartier"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Beef",
            char='B',
            color=COLOR_RED,
            description="Makes you heartier",
            effect_value=1 
        )
    
    def use(self, player):
        """Increase the player's max HP and attack."""
        player.max_hp += 20 
        player.attack += 1
        return True

class Carrot(Consumable):
    """Improves your eyesight"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Carrot",
            char='!',
            color=COLOR_ORANGE,
            description="Improves your eyesight",
            effect_value=1 
        )
    
    def use(self, player):
        """Increase the player's max HP and attack."""
        player.fov += self.effect_value
        return True

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
        player.gain_xp(self.effect_value)
        return True