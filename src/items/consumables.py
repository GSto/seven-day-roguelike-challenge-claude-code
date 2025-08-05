"""
Consumable items like potions.
"""

import random
from constants import COLOR_RED, COLOR_BLUE, COLOR_ORANGE, COLOR_SALMON, COLOR_WHITE, COLOR_YELLOW
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


class PowerCatalyst(Consumable):
    """Permanently increases attack power"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Power Catalyst",
            char='*',
            color=COLOR_RED,
            description="Permanently increases attack by 1",
            effect_value=1
        )
    
    def use(self, player):
        """Permanently increase player's attack"""
        player.attack += self.effect_value
        return True


class DefenseCatalyst(Consumable):
    """Permanently increases defense"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Defense Catalyst",
            char='*',
            color=COLOR_BLUE,
            description="Permanently increases defense by 1",
            effect_value=1
        )
    
    def use(self, player):
        """Permanently increase player's defense"""
        player.defense += self.effect_value
        return True


class D6(Consumable):
    """Random effect dice with 6 possible outcomes"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="D6",
            char='6',
            color=COLOR_WHITE,
            description="Roll for one of 6 random effects: +1 Attack, +1 Defense, +10 max HP, +1 FOV, or -20 max HP",
            effect_value=1
        )
    
    def use(self, player):
        """Apply one of 6 random effects"""
        roll = random.randint(1, 6)
        
        if roll == 1:
            # +1 Attack
            player.attack += 1
            return True
        elif roll == 2:
            # +1 Defense
            player.defense += 1
            return True
        elif roll == 3:
            # +10 max HP
            old_max = player.max_hp
            player.max_hp += 10
            player.hp += (player.max_hp - old_max)  # Heal the difference
            return True
        elif roll == 4:
            # +1 FOV
            player.fov += 1
            return True
        elif roll == 5:
            # -20 max HP (but don't kill the player)
            if player.max_hp > 25:  # Ensure player doesn't die from this
                player.max_hp -= 20
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
            return True
        else:  # roll == 6
            # Duplicate effect - +1 Attack (making it slightly more likely to be positive)
            player.attack += 1
            return True