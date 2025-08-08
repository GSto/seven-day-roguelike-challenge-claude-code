"""
Consumable items like potions.
"""

import random
from constants import COLOR_RED, COLOR_BLUE, COLOR_ORANGE, COLOR_SALMON, COLOR_WHITE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN
from .base import Consumable
from .enchantments import EnchantmentType, get_enchantment_by_type, get_random_enchantment


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
            char='B',
            color=COLOR_RED,
            description="Makes you heartier",
            effect_value=1 
        )
    
    def use(self, player):
        """Increase the player's max HP and attack."""
        player.max_hp += 20 
        player.attack += 1
        return (True, "You feel heartier! Max HP +20, Attack +1")

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
        """Increase the player's FOV."""
        player.fov += self.effect_value
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
        player.gain_xp(self.effect_value)
        return (True, f"You gain {self.effect_value} XP from ancient wisdom!")


class PowerCatalyst(Consumable):
    """Permanently increases attack power"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Warrior's Catalyst",
            char='*',
            color=COLOR_RED,
            description="Permanently increases attack by 1",
            effect_value=1
        )
    
    def use(self, player):
        """Permanently increase player's attack"""
        player.attack += self.effect_value
        return (True, f"You feel more powerful! Attack +{self.effect_value}")


class DefenseCatalyst(Consumable):
    """Permanently increases defense"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Defender's Catalyst",
            char='*',
            color=COLOR_BLUE,
            description="Permanently increases defense by 1",
            effect_value=1
        )
    
    def use(self, player):
        """Permanently increase player's defense"""
        player.defense += self.effect_value
        return (True, f"You feel more protected! Defense +{self.effect_value}")

class D6(Consumable):
    """Random effect dice with 6 possible outcomes"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="D6",
            char='6',
            color=COLOR_WHITE,
            description="Roll for one of 6 random effects:\n +1 Attack, +1 Defense, +10 max HP, +1 FOV, or -20 max HP",
            effect_value=1
        )
    
    def use(self, player):
        """Apply one of 6 random effects"""
        roll = random.randint(1, 6)
        
        if roll == 1:
            # +1 Attack
            player.attack += 1
            return (True, f"Rolled {roll}! Attack +1")
        elif roll == 2:
            # +1 Defense
            player.defense += 1
            return (True, f"Rolled {roll}! Defense +1")
        elif roll == 3:
            # +10 max HP
            old_max = player.max_hp
            player.max_hp += 10
            player.hp += (player.max_hp - old_max)  # Heal the difference
            return (True, f"Rolled {roll}! Max HP +10")
        elif roll == 4:
            # +1 FOV
            player.fov += 1
            return (True, f"Rolled {roll}! FOV +1")
        elif roll == 5:
            # -20 max HP (but don't kill the player)
            if player.max_hp > 25:  # Ensure player doesn't die from this
                player.max_hp -= 20
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
                return (True, f"Rolled {roll}! Max HP -20 (ouch!)")
            else:
                return (True, f"Rolled {roll}! But you're too weak for the penalty to apply.")
        else:  # roll == 6
            # Duplicate effect - +1 Attack (making it slightly more likely to be positive)
            player.attack += 1
            return (True, f"Rolled {roll}! Attack +1")


class BaronCatalyst(Consumable):
    """Permanently increases attack multiplier by 10%"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Baron's Catalyst",
            char='!',
            color=COLOR_YELLOW,
            description="Permanently increases attack multiplier by 10%",
            effect_value=0.1,
            attack_multiplier_effect=1.1
        )
    
    def use(self, player):
        """Permanently increase player's attack multiplier"""
        player.attack_multiplier *= self.attack_multiplier_effect
        return (True, f"Your attacks become more effective! Attack multiplier increased by {int((self.attack_multiplier_effect-1)*100)}%")


class WardenCatalyst(Consumable):
    """Permanently increases defense multiplier by 10%"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Warden's Catalyst",
            char='!',
            color=COLOR_BLUE,
            description="Permanently increases defense multiplier by 10%",
            effect_value=0.1,
            defense_multiplier_effect=1.1
        )
    
    def use(self, player):
        """Permanently increase player's defense multiplier"""
        player.defense_multiplier *= self.defense_multiplier_effect
        return (True, f"Your defenses become more effective! Defense multiplier increased by {int((self.defense_multiplier_effect-1)*100)}%")


class JewelerCatalyst(Consumable):
    """Permanently increases XP multiplier by 20%"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Jeweler's Catalyst",
            char='!',
            color=COLOR_WHITE,
            description="Permanently increases XP multiplier by 5%",
            effect_value=0.05,
            xp_multiplier_effect=1.05
        )
    
    def use(self, player):
        """Permanently increase player's XP multiplier"""
        player.xp_multiplier *= self.xp_multiplier_effect
        return (True, f"You learn more efficiently! XP multiplier increased by {int((self.xp_multiplier_effect-1)*100)}%")


# ============================================================================
# ENCHANTMENT BOONS - Add enchantments to equipped weapons
# ============================================================================

class BaronsBoon(Consumable):
    """Applies Shiny enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Baron's Boon",
            char='*',
            color=COLOR_YELLOW,
            description="Applies Shiny enchantment to equipped weapon (+25% damage)",
            effect_value=1
        )
    
    def use(self, player):
        """Apply Shiny enchantment to equipped weapon"""
        if not player.weapon:
            return (False, "You need to have a weapon equipped to use this!")
        
        enchantment = get_enchantment_by_type(EnchantmentType.SHINY)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} shines with new power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")


class JewelersBoon(Consumable):
    """Applies Gilded enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Jeweler's Boon",
            char='*',
            color=COLOR_WHITE,
            description="Applies Gilded enchantment to equipped weapon (+5% XP)",
            effect_value=1
        )
    
    def use(self, player):
        """Apply Gilded enchantment to equipped weapon"""
        if not player.weapon:
            return (False, "You need to have a weapon equipped to use this!")
        
        enchantment = get_enchantment_by_type(EnchantmentType.GILDED)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} gleams with golden light!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")


class MinersBoon(Consumable):
    """Applies Glowing enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Miner's Boon",
            char='*',
            color=COLOR_CYAN,
            description="Applies Glowing enchantment to equipped weapon (+2 FOV)",
            effect_value=1
        )
    
    def use(self, player):
        """Apply Glowing enchantment to equipped weapon"""
        if not player.weapon:
            return (False, "You need to have a weapon equipped to use this!")
        
        enchantment = get_enchantment_by_type(EnchantmentType.GLOWING)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} begins to glow softly!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")


class ClericsBoon(Consumable):
    """Applies Blessed enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Cleric's Boon",
            char='*',
            color=COLOR_WHITE,
            description="Applies Blessed enchantment to equipped weapon (+5% healing)",
            effect_value=1
        )
    
    def use(self, player):
        """Apply Blessed enchantment to equipped weapon"""
        if not player.weapon:
            return (False, "You need to have a weapon equipped to use this!")
        
        enchantment = get_enchantment_by_type(EnchantmentType.BLESSED)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} is blessed with divine power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")


class WardensBoon(Consumable):
    """Applies Bolstered enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Warden's Boon",
            char='*',
            color=COLOR_BLUE,
            description="Applies Bolstered enchantment to equipped weapon (+1 defense)",
            effect_value=1
        )
    
    def use(self, player):
        """Apply Bolstered enchantment to equipped weapon"""
        if not player.weapon:
            return (False, "You need to have a weapon equipped to use this!")
        
        enchantment = get_enchantment_by_type(EnchantmentType.BOLSTERED)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} feels more solid and protective!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")


class JokersBoon(Consumable):
    """Applies a random enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Joker's Boon",
            char='*',
            color=COLOR_GREEN,
            description="Applies a random enchantment to equipped weapon",
            effect_value=1
        )
    
    def use(self, player):
        """Apply a random enchantment to equipped weapon"""
        if not player.weapon:
            return (False, "You need to have a weapon equipped to use this!")
        
        enchantment = get_random_enchantment()
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} is enchanted with {enchantment.name} power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")