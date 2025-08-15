"""
Boon consumables that apply enchantments to equipped items.
"""

from constants import COLOR_RED, COLOR_BLUE, COLOR_ORANGE, COLOR_SALMON, COLOR_WHITE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN
from .base import Consumable
from .enchantments import EnchantmentType, get_enchantment_by_type, get_random_enchantment


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