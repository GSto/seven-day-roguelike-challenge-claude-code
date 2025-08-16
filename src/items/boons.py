"""
Boon consumables that apply enchantments to equipped items.
"""

from constants import COLOR_RED, COLOR_BLUE, COLOR_ORANGE, COLOR_SALMON, COLOR_WHITE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN
from .base import Consumable
from .enchantments import EnchantmentType, get_weapon_enchantment_by_type


class Boon(Consumable):
    """Base class for boons that apply enchantments to equipment."""
    
    def __init__(self, x, y, name, char='*', color=COLOR_WHITE, description="", effect_value=1, enchantment_type=None):
        super().__init__(
            x=x, y=y,
            name=name,
            char=char,
            color=color,
            description=description,
            effect_value=effect_value
        )
        self.enchantment_type = enchantment_type
    
    def use(self, player):
        """Default use method that applies enchantment with choice logic."""
        if self.enchantment_type is None:
            return (False, "This boon has no enchantment type specified!")
        return self.apply_enchantment_with_choice(player, self.enchantment_type)
    
    def apply_enchantment_with_choice(self, player, enchantment_type):
        """Apply enchantment with weapon/armor choice logic."""
        # Check eligibility
        weapon_eligible = self.can_enchant_weapon(player, enchantment_type)
        armor_eligible = self.can_enchant_armor(player, enchantment_type)
        
        if not weapon_eligible and not armor_eligible:
            return (False, "You need equipped items that can be further enhanced!")
        
        # If only one option available, use it automatically
        if weapon_eligible and not armor_eligible:
            return self.apply_to_weapon(player, enchantment_type)
        elif armor_eligible and not weapon_eligible:
            return self.apply_to_armor(player, enchantment_type)
        
        # Both are eligible - prompt for choice
        # For now, default to weapon until UI choice is implemented
        return self.apply_to_weapon(player, enchantment_type)
    
    def can_enchant_weapon(self, player, enchantment_type):
        """Check if weapon can be enchanted."""
        return (player.weapon is not None and
                len(player.weapon.enchantments) < 2 and
                enchantment_type.can_enchant_weapon and
                not any(e.type == enchantment_type for e in player.weapon.enchantments))
    
    def can_enchant_armor(self, player, enchantment_type):
        """Check if armor can be enchanted."""
        return (player.armor is not None and
                len(player.armor.enchantments) < 2 and
                enchantment_type.can_enchant_armor and
                not any(e.type == enchantment_type for e in player.armor.enchantments))
    
    def apply_to_weapon(self, player, enchantment_type):
        """Apply enchantment to weapon."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} shines with new power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")
    
    def apply_to_armor(self, player, enchantment_type):
        """Apply enchantment to armor."""
        from .enchantments import get_armor_enchantment_by_type
        enchantment = get_armor_enchantment_by_type(enchantment_type)
        if player.armor.add_enchantment(enchantment):
            return (True, f"Your {player.armor.name} gleams with new protection!")
        else:
            return (False, f"Your {player.armor.name} cannot be further enhanced!")


# ============================================================================
# ENCHANTMENT BOONS - Add enchantments to equipped weapons
# ============================================================================

class BaronsBoon(Boon):
    """Applies Shiny enchantment to equipped weapon or armor"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Baron's Boon",
            char='*',
            color=COLOR_YELLOW,
            description="Applies Shiny enchantment to equipped weapon (+25% damage) or armor (+25% defense)",
            effect_value=1,
            enchantment_type=EnchantmentType.SHINY
        )


class JewelersBoon(Boon):
    """Applies Gilded enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Jeweler's Boon",
            char='*',
            color=COLOR_WHITE,
            description="Applies Gilded enchantment to equipped weapon (+5% XP)",
            effect_value=1,
            enchantment_type=EnchantmentType.GILDED
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Override to provide custom message for Jeweler's Boon."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} gleams with golden light!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")


class MinersBoon(Boon):
    """Applies Glowing enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Miner's Boon",
            char='*',
            color=COLOR_CYAN,
            description="Applies Glowing enchantment to equipped weapon (+2 FOV)",
            effect_value=1,
            enchantment_type=EnchantmentType.GLOWING
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Override to provide custom message for Miner's Boon."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} begins to glow softly!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")


class ClericsBoon(Boon):
    """Applies Blessed enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Cleric's Boon",
            char='*',
            color=COLOR_WHITE,
            description="Applies Blessed enchantment to equipped weapon (+5% healing)",
            effect_value=1,
            enchantment_type=EnchantmentType.BLESSED
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Override to provide custom message for Cleric's Boon."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} is blessed with divine power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")


class JokersBoon(Boon):
    """Applies a random enchantment to equipped weapon or armor"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Joker's Boon",
            char='*',
            color=COLOR_GREEN,
            description="Applies a random enchantment to equipped weapon or armor",
            effect_value=1
        )
    
    def use(self, player):
        """Apply a random enchantment with equipment choice"""
        import random
        
        # Get all possible enchantment types
        all_enchantments = [e for e in EnchantmentType]
        random_enchantment_type = random.choice(all_enchantments)
        
        # Use the choice logic with the random enchantment type
        return self.apply_enchantment_with_choice(player, random_enchantment_type)
    
    def apply_to_weapon(self, player, enchantment_type):
        """Override to provide custom message for Joker's Boon."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} is enchanted with {enchantment.name} power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")
    
    def apply_to_armor(self, player, enchantment_type):
        """Override to provide custom message for Joker's Boon."""
        from .enchantments import get_armor_enchantment_by_type
        enchantment = get_armor_enchantment_by_type(enchantment_type)
        if player.armor.add_enchantment(enchantment):
            return (True, f"Your {player.armor.name} is enchanted with {enchantment.name} power!")
        else:
            return (False, f"Your {player.armor.name} cannot be further enhanced!")


class ReapersBoon(Boon):
    """Applies Rending enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Reaper's Boon",
            char='*',
            color=COLOR_RED,
            description="Applies Rending enchantment to equipped weapon (+10% crit)",
            effect_value=1,
            enchantment_type=EnchantmentType.RENDING
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Override to provide custom message for Reaper's Boon."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} is enchanted with Rending power (+10% crit chance)!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")


# ============================================================================
# ELEMENTAL BOONS - Apply attack traits to weapons, resistance to armor
# ============================================================================

class FireBoon(Boon):
    """Applies Fire enchantment to equipped weapon (attack trait) or armor (resistance)"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Fire Boon",
            char='*',
            color=COLOR_RED,
            description="Applies Fire enchantment to equipped weapon (Fire attacks) or armor (Fire resistance)",
            effect_value=1,
            enchantment_type=EnchantmentType.FIRE
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Apply Fire enchantment to weapon for attack trait."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} ignites with flaming power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")
    
    def apply_to_armor(self, player, enchantment_type):
        """Apply Fire enchantment to armor for resistance."""
        from .enchantments import get_armor_enchantment_by_type
        enchantment = get_armor_enchantment_by_type(enchantment_type)
        if player.armor.add_enchantment(enchantment):
            return (True, f"Your {player.armor.name} becomes fireproof!")
        else:
            return (False, f"Your {player.armor.name} cannot be further enhanced!")


class IceBoon(Boon):
    """Applies Ice enchantment to equipped weapon (attack trait) or armor (resistance)"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Ice Boon",
            char='*',
            color=COLOR_CYAN,
            description="Applies Ice enchantment to equipped weapon (Ice attacks) or armor (Ice resistance)",
            effect_value=1,
            enchantment_type=EnchantmentType.ICE
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Apply Ice enchantment to weapon for attack trait."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} becomes cold as winter!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")
    
    def apply_to_armor(self, player, enchantment_type):
        """Apply Ice enchantment to armor for resistance."""
        from .enchantments import get_armor_enchantment_by_type
        enchantment = get_armor_enchantment_by_type(enchantment_type)
        if player.armor.add_enchantment(enchantment):
            return (True, f"Your {player.armor.name} becomes snuggly warm!")
        else:
            return (False, f"Your {player.armor.name} cannot be further enhanced!")


class HolyBoon(Boon):
    """Applies Holy enchantment to equipped weapon (attack trait) or armor (resistance)"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Holy Boon",
            char='*',
            color=COLOR_YELLOW,
            description="Applies Holy enchantment to equipped weapon (Holy attacks) or armor (Holy resistance)",
            effect_value=1,
            enchantment_type=EnchantmentType.HOLY
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Apply Holy enchantment to weapon for attack trait."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} shines with divine light!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")
    
    def apply_to_armor(self, player, enchantment_type):
        """Apply Holy enchantment to armor for resistance."""
        from .enchantments import get_armor_enchantment_by_type
        enchantment = get_armor_enchantment_by_type(enchantment_type)
        if player.armor.add_enchantment(enchantment):
            return (True, f"Your {player.armor.name} glows with blessed protection!")
        else:
            return (False, f"Your {player.armor.name} cannot be further enhanced!")


class DarkBoon(Boon):
    """Applies Dark enchantment to equipped weapon (attack trait) or armor (resistance)"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Dark Boon",
            char='*',
            color=COLOR_SALMON,
            description="Applies Dark enchantment to equipped weapon (Dark attacks) or armor (Dark resistance)",
            effect_value=1,
            enchantment_type=EnchantmentType.DARK
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Apply Dark enchantment to weapon for attack trait."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} is shrouded in dark power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")
    
    def apply_to_armor(self, player, enchantment_type):
        """Apply Dark enchantment to armor for resistance."""
        from .enchantments import get_armor_enchantment_by_type
        enchantment = get_armor_enchantment_by_type(enchantment_type)
        if player.armor.add_enchantment(enchantment):
            return (True, f"Your {player.armor.name} radiates an ominous aura!")
        else:
            return (False, f"Your {player.armor.name} cannot be further enhanced!")