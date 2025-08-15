"""
Consumable items like potions.
"""

import random
from constants import COLOR_RED, COLOR_BLUE, COLOR_ORANGE, COLOR_SALMON, COLOR_WHITE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN
from .base import Consumable
from .enchantments import EnchantmentType, get_enchantment_by_type, get_random_enchantment
from traits import Trait


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
        
        if roll == 5:
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
            # +3 FOV
            player.fov += 1
            return (True, f"Rolled {roll}! FOV +3")
        elif roll == 1:
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

class MagicMushroom(Consumable): 
    """All stats up +1"""

    def __init__(self, x, y):
          super().__init__(
              x=x, y=y,
              name="Magic Mushroom",
              char='m',
              color=COLOR_RED,
              description="Permanently increases XP multiplier by 5%",
              effect_value=1,
              xp_multiplier_effect=1.05
          )
    
    def use(self, player): 
        player.max_hp += 1
        player.attack += 1
        player.defense += 1 
        player.xp += 1
        player.fov += 1
        player.evade += 0.01
        player.crit += 0.01
        player.crit_multiplier += 0.01
        player.health_aspect += 0.01
        player.attack_multiplier += 0.01
        player.defense_multiplier += 0.01
        player.xp_multiplier += 0.01 
        return (True, f"all up by 1")
        


# ============================================================================
# ENCHANTMENT BOONS - Add enchantments to equipped weapons
# ============================================================================

class BaronsBoon(Consumable):
    """Applies Shiny enchantment to equipped weapon or armor"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Baron's Boon",
            char='*',
            color=COLOR_YELLOW,
            description="Applies Shiny enchantment to equipped weapon (+25% damage) or armor (+25% defense)",
            effect_value=1
        )
    
    def use(self, player):
        """Apply Shiny enchantment with equipment choice"""
        from .enchantments import EnchantmentType, get_weapon_enchantment_by_type, get_armor_enchantment_by_type
        
        return self._apply_enchantment_with_choice(player, EnchantmentType.SHINY)
    
    def _apply_enchantment_with_choice(self, player, enchantment_type):
        """Apply enchantment with weapon/armor choice logic."""
        # Check eligibility
        weapon_eligible = self._can_enchant_weapon(player, enchantment_type)
        armor_eligible = self._can_enchant_armor(player, enchantment_type)
        
        if not weapon_eligible and not armor_eligible:
            return (False, "You need equipped items that can be further enhanced!")
        
        # If only one option available, use it automatically
        if weapon_eligible and not armor_eligible:
            return self._apply_to_weapon(player, enchantment_type)
        elif armor_eligible and not weapon_eligible:
            return self._apply_to_armor(player, enchantment_type)
        
        # Both are eligible - prompt for choice
        # For now, default to weapon until UI choice is implemented
        return self._apply_to_weapon(player, enchantment_type)
    
    def _can_enchant_weapon(self, player, enchantment_type):
        """Check if weapon can be enchanted."""
        return (player.weapon is not None and
                len(player.weapon.enchantments) < 2 and
                enchantment_type.can_enchant_weapon and
                not any(e.type == enchantment_type for e in player.weapon.enchantments))
    
    def _can_enchant_armor(self, player, enchantment_type):
        """Check if armor can be enchanted."""
        return (player.armor is not None and
                len(player.armor.enchantments) < 2 and
                enchantment_type.can_enchant_armor and
                not any(e.type == enchantment_type for e in player.armor.enchantments))
    
    def _apply_to_weapon(self, player, enchantment_type):
        """Apply enchantment to weapon."""
        from .enchantments import get_weapon_enchantment_by_type
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} shines with new power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")
    
    def _apply_to_armor(self, player, enchantment_type):
        """Apply enchantment to armor."""
        from .enchantments import get_armor_enchantment_by_type
        enchantment = get_armor_enchantment_by_type(enchantment_type)
        if player.armor.add_enchantment(enchantment):
            return (True, f"Your {player.armor.name} gleams with new protection!")
        else:
            return (False, f"Your {player.armor.name} cannot be further enhanced!")


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


class ReapersCatalyst(Consumable):
    """Permanently increases crit chance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Reaper's Catalyst",
            char='*',
            color=COLOR_RED,
            description="Permanently increases crit chance by 5%",
            effect_value=0.05
        )
    
    def use(self, player):
        """Permanently increase player's crit chance"""
        player.crit += self.effect_value
        return (True, f"You feel deadlier! Crit chance +{int(self.effect_value * 100)}%")


class ShadowsCatalyst(Consumable):
    """Permanently increases evade chance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Shadow's Catalyst",
            char='*',
            color=COLOR_BLUE,
            description="Permanently increases evade chance by 5%",
            effect_value=0.05
        )
    
    def use(self, player):
        """Permanently increase player's evade chance"""
        player.evade += self.effect_value
        return (True, f"You feel more agile! Evade chance +{int(self.effect_value * 100)}%")


class ReapersBoon(Consumable):
    """Applies Rending enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Reaper's Boon",
            char='*',
            color=COLOR_RED,
            description="Applies Rending enchantment to equipped weapon (+10% crit)",
            effect_value=1
        )
    
    def use(self, player):
        """Apply Rending enchantment to player's weapon"""
        if not player.weapon:
            return (False, "You need to have a weapon equipped to use this!")
        
        enchantment = get_enchantment_by_type(EnchantmentType.RENDING)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} is enchanted with Rending power (+10% crit chance)!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")


# ============================================================================
# ELEMENTAL ATTACK CATALYSTS - Permanently add attack traits and weaknesses
# ============================================================================

class FireAttackCatalyst(Consumable):
    """Permanently adds Fire attack trait and Ice weakness"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Ember Catalyst",
            char='*',
            color=COLOR_RED,
            description="Permanently adds Fire attack trait but makes you weak to Ice",
            effect_value=1
        )
    
    def use(self, player):
        """Add Fire attack trait and Ice weakness to player"""
        if Trait.FIRE not in player.attack_traits:
            player.attack_traits.append(Trait.FIRE)
        if Trait.ICE not in player.weaknesses:
            player.weaknesses.append(Trait.ICE)
        return (True, "Your attacks burn with fire, but you feel vulnerable to ice!")


class IceAttackCatalyst(Consumable):
    """Permanently adds Ice attack trait and Fire weakness"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Frost Catalyst",
            char='*',
            color=COLOR_CYAN,
            description="Permanently adds Ice attack trait but makes you weak to Fire",
            effect_value=1
        )
    
    def use(self, player):
        """Add Ice attack trait and Fire weakness to player"""
        if Trait.ICE not in player.attack_traits:
            player.attack_traits.append(Trait.ICE)
        if Trait.FIRE not in player.weaknesses:
            player.weaknesses.append(Trait.FIRE)
        return (True, "Your attacks freeze with ice, but you feel vulnerable to fire!")


class HolyAttackCatalyst(Consumable):
    """Permanently adds Holy attack trait and Dark weakness"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Divine Catalyst",
            char='*',
            color=COLOR_YELLOW,
            description="Permanently adds Holy attack trait but makes you weak to Dark",
            effect_value=1
        )
    
    def use(self, player):
        """Add Holy attack trait and Dark weakness to player"""
        if Trait.HOLY not in player.attack_traits:
            player.attack_traits.append(Trait.HOLY)
        if Trait.DARK not in player.weaknesses:
            player.weaknesses.append(Trait.DARK)
        return (True, "Your attacks shine with holy light, but you feel vulnerable to darkness!")


class DarkAttackCatalyst(Consumable):
    """Permanently adds Dark attack trait and Holy weakness"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Shadow Catalyst",
            char='*',
            color=COLOR_SALMON,
            description="Permanently adds Dark attack trait but makes you weak to Holy",
            effect_value=1
        )
    
    def use(self, player):
        """Add Dark attack trait and Holy weakness to player"""
        if Trait.DARK not in player.attack_traits:
            player.attack_traits.append(Trait.DARK)
        if Trait.HOLY not in player.weaknesses:
            player.weaknesses.append(Trait.HOLY)
        return (True, "Your attacks darken with shadow, but you feel vulnerable to holy light!")


# ============================================================================
# ELEMENTAL RESISTANCE CATALYSTS - Permanently add resistance traits
# ============================================================================

class FireResistanceCatalyst(Consumable):
    """Permanently adds Fire resistance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Salamander Catalyst",
            char='*',
            color=COLOR_ORANGE,
            description="Permanently adds Fire resistance",
            effect_value=1
        )
    
    def use(self, player):
        """Add Fire resistance to player"""
        if Trait.FIRE not in player.resistances:
            player.resistances.append(Trait.FIRE)
        return (True, "You feel protected against fire!")


class IceResistanceCatalyst(Consumable):
    """Permanently adds Ice resistance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Yeti Catalyst",
            char='*',
            color=COLOR_BLUE,
            description="Permanently adds Ice resistance",
            effect_value=1
        )
    
    def use(self, player):
        """Add Ice resistance to player"""
        if Trait.ICE not in player.resistances:
            player.resistances.append(Trait.ICE)
        return (True, "You feel protected against ice!")


class HolyResistanceCatalyst(Consumable):
    """Permanently adds Holy resistance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Angel Catalyst",
            char='*',
            color=COLOR_WHITE,
            description="Permanently adds Holy resistance",
            effect_value=1
        )
    
    def use(self, player):
        """Add Holy resistance to player"""
        if Trait.HOLY not in player.resistances:
            player.resistances.append(Trait.HOLY)
        return (True, "You feel protected against holy light!")


class DarkResistanceCatalyst(Consumable):
    """Permanently adds Dark resistance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Demon Catalyst",
            char='*',
            color=COLOR_SALMON,
            description="Permanently adds Dark resistance",
            effect_value=1
        )
    
    def use(self, player):
        """Add Dark resistance to player"""
        if Trait.DARK not in player.resistances:
            player.resistances.append(Trait.DARK)
        return (True, "You feel protected against darkness!")