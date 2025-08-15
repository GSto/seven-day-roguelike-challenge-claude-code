"""
Food consumables that provide healing and nutrition.
"""

from constants import COLOR_RED, COLOR_BLUE, COLOR_ORANGE, COLOR_SALMON, COLOR_WHITE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN
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
            return (False, "You are already at full health!")
        
        old_hp = player.hp
        # Calculate healing based on effect_value * player's total health_aspect
        heal_amount = int(player.max_hp * (self.effect_value * player.get_total_health_aspect()))
        player.heal(heal_amount)
        actual_healing = player.hp - old_hp
        if actual_healing > 0:
            return (True, f"You recovered {actual_healing} HP!")
        return (False, "The potion had no effect.")


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


class Beef(Consumable):
    """Makes you heartier"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Beef",
            char='b',
            color=COLOR_RED,
            description="Makes you heartier",
            effect_value=20
        )
    
    def use(self, player):
        """Increase the player's max HP and attack."""
        player.max_hp += self.effect_value 
        player.attack += 1
        player.heal(5)
        return (True, "You feel heartier! Max HP +20, Attack +1")


class Chicken(Consumable):
    """Makes you heartier"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Wall Chicken",
            char='c',
            color=COLOR_RED,
            description="Makes you heartier",
            effect_value=1 
        )
    
    def use(self, player):
        """Increase the player's max HP and attack."""
        player.max_hp += 10 
        player.heal(10)
        return (True, "You feel heartier! Max HP +10")


class Carrot(Consumable):
    """Improves your eyesight"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Carrot",
            char='!',
            color=COLOR_ORANGE,
            description="Improves your eyesight",
            effect_value=3 
        )
    
    def use(self, player):
        """Increase the player's FOV."""
        player.fov += self.effect_value
        player.heal(10) # All food provides a little HP
        return (True, f"Your vision improves! FOV +{self.effect_value}")


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


class Antidote(Consumable):
    """Removes all negative status effects"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Antidote",
            char='!',
            color=COLOR_GREEN,
            description="Removes all negative status effects",
            effect_value=1 
        )
    
    def use(self, player):
        """Remove all negative status effects from player"""
        if player.status_effects.has_negative_effects():
            player.status_effects.clear_negative_effects()
            return (True, "You feel cleansed! All negative status effects removed.")
        else:
            return (False, "You have no negative status effects to cure.")


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
        if player.hp <= 1:
            return (False, "You're too weak to use this!")
        
        player.status_effects.apply_status('shields', self.effect_value, player)
        player.hp = 1
        return (True, f"You feel incredibly protected but fragile! Gained {self.effect_value} shields, HP reduced to 1.")