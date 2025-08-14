"""
Enchantment system for weapons.
"""

from enum import Enum
import random
from traits import Trait

# TODO: should be 25% by default. ramping up for testing
WEAPON_ENCHANT_CHANCE = 0.25
ARMOR_ENCHANT_CHANCE = 0.25

class EnchantmentType(Enum):
    """Types of enchantments available for weapons."""
    QUALITY = "Quality"      # +3 Attack bonus
    SHINY = "Shiny"         # 1.25x damage multiplier 
    GLOWING = "Glowing"     # +2 FOV bonus
    GILDED = "Gilded"       # +5% XP bonus
    BLESSED = "Blessed"     # +5% healing aspect bonus
    BOLSTERED = "Bolstered" # +1 defense bonus
    RENDING = "Rending"     # +10% crit chance
    # New trait enchantments
    FLAMING = "Flaming"     # Fire attack trait
    CHILLING = "Chilling"   # Ice attack trait
    GLORIOUS = "Glorious"   # Holy attack trait
    BLASPHEMOUS = "Blasphemous" # Dark attack trait


class ArmorEnchantmentType(Enum):
    """Types of enchantments available for armor."""
    FIREPROOF = "Fireproof"   # Fire resistance
    SNUGGLY = "Snuggly"       # Ice resistance  
    BLASPHEMOUS_ARMOR = "Blasphemous"  # Dark resistance
    GLORIOUS_ARMOR = "Glorious"        # Holy resistance
    STURDY = "Sturdy"         # Strike resistance
    PLATED = "Plated"         # Slash resistance


class Enchantment:
    """Represents an enchantment on a weapon."""
    
    def __init__(self, enchantment_type):
        self.type = enchantment_type
        self.name = enchantment_type.value
        self.attack_traits = self._get_attack_traits()
    
    def get_attack_bonus(self):
        """Get the attack bonus provided by this enchantment."""
        if self.type == EnchantmentType.QUALITY:
            return 3
        elif self.type == EnchantmentType.BOLSTERED:
            return 0  # Defense bonus, not attack
        return 0
    
    def get_defense_bonus(self):
        """Get the defense bonus provided by this enchantment."""
        if self.type == EnchantmentType.BOLSTERED:
            return 1
        return 0
    
    def get_fov_bonus(self):
        """Get the FOV bonus provided by this enchantment."""
        if self.type == EnchantmentType.GLOWING:
            return 2
        return 0
    
    def get_attack_multiplier_bonus(self):
        """Get the attack multiplier bonus provided by this enchantment."""
        if self.type == EnchantmentType.SHINY:
            return 0.25  # 25% bonus = 1.25x damage
        return 0.0
    
    def get_xp_multiplier_bonus(self):
        """Get the XP multiplier bonus provided by this enchantment."""
        if self.type == EnchantmentType.GILDED:
            return 0.05  # 5% bonus
        return 0.0
    
    def get_health_aspect_bonus(self):
        """Get the health aspect bonus provided by this enchantment."""
        if self.type == EnchantmentType.BLESSED:
            return 0.05  # 5% bonus
        return 0.0
    
    def get_crit_bonus(self):
        """Get the crit chance bonus provided by this enchantment."""
        if self.type == EnchantmentType.RENDING:
            return 0.10  # 10% crit chance bonus
        return 0.0
    
    def _get_attack_traits(self):
        """Get the attack traits provided by this enchantment."""
        trait_map = {
            EnchantmentType.FLAMING: [Trait.FIRE],
            EnchantmentType.CHILLING: [Trait.ICE],
            EnchantmentType.GLORIOUS: [Trait.HOLY],
            EnchantmentType.BLASPHEMOUS: [Trait.DARK]
        }
        return trait_map.get(self.type, [])


class ArmorEnchantment:
    """Represents an enchantment on armor."""
    
    def __init__(self, enchantment_type):
        self.type = enchantment_type
        self.name = enchantment_type.value
        self.resistances = self._get_resistances()
    
    def _get_resistances(self):
        """Get the resistances provided by this enchantment."""
        resistance_map = {
            ArmorEnchantmentType.FIREPROOF: [Trait.FIRE],
            ArmorEnchantmentType.SNUGGLY: [Trait.ICE],
            ArmorEnchantmentType.BLASPHEMOUS_ARMOR: [Trait.DARK],
            ArmorEnchantmentType.GLORIOUS_ARMOR: [Trait.HOLY],
            ArmorEnchantmentType.STURDY: [Trait.STRIKE],
            ArmorEnchantmentType.PLATED: [Trait.SLASH]
        }
        return resistance_map.get(self.type, [])


def get_random_enchantment():
    """Get a random enchantment."""
    enchantment_type = random.choice(list(EnchantmentType))
    return Enchantment(enchantment_type)


def get_enchantment_by_type(enchantment_type):
    """Get an enchantment of a specific type."""
    return Enchantment(enchantment_type)


def get_random_armor_enchantment():
    """Get a random armor enchantment."""
    enchantment_type = random.choice(list(ArmorEnchantmentType))
    return ArmorEnchantment(enchantment_type)


def get_armor_enchantment_by_type(enchantment_type):
    """Get an armor enchantment of a specific type."""
    return ArmorEnchantment(enchantment_type)


def should_spawn_with_enchantment():
    """Check if a weapon should spawn with an enchantment."""
    return random.random() < WEAPON_ENCHANT_CHANCE


def should_armor_spawn_with_enchantment():
    """Check if armor should spawn with an enchantment."""
    return random.random() < ARMOR_ENCHANT_CHANCE