"""
Unified enchantment system for weapons and armor.
"""

from enum import Enum
import random
from traits import Trait

# TODO: should be 25% by default. ramping up for testing
WEAPON_ENCHANT_CHANCE = 0.25
ARMOR_ENCHANT_CHANCE = 0.25

class EnchantmentType(Enum):
    """Unified enchantment types that can be applied to weapons and armor."""
    QUALITY = "Quality"
    SHINY = "Shiny" 
    GLOWING = "Glowing"
    GILDED = "Gilded"
    BLESSED = "Blessed"
    BALANCED = "Balanced"
    RENDING = "Rending"
    SHADOW = "Shadow"
    FIRE = "Fire"
    ICE = "Ice"
    HOLY = "Holy"
    DARK = "Dark"
    
    @property
    def can_enchant_weapon(self):
        """Check if this enchantment can be applied to weapons."""
        return self != EnchantmentType.SHADOW
    
    @property
    def can_enchant_armor(self):
        """Check if this enchantment can be applied to armor."""
        return self != EnchantmentType.RENDING
    
    def get_weapon_label(self):
        """Get the label for this enchantment when applied to weapons."""
        labels = {
            EnchantmentType.QUALITY: "quality",
            EnchantmentType.SHINY: "refined",
            EnchantmentType.GLOWING: "glowing",
            EnchantmentType.GILDED: "gilded",
            EnchantmentType.BLESSED: "blessed",
            EnchantmentType.BALANCED: "bolstered",
            EnchantmentType.RENDING: "rending",
            EnchantmentType.FIRE: "flaming",
            EnchantmentType.ICE: "chilling",
            EnchantmentType.HOLY: "glorious",
            EnchantmentType.DARK: "blasphemous"
        }
        return labels.get(self, self.value.lower())
    
    def get_armor_label(self):
        """Get the label for this enchantment when applied to armor."""
        labels = {
            EnchantmentType.QUALITY: "quality",
            EnchantmentType.SHINY: "refined",
            EnchantmentType.GLOWING: "glowing",
            EnchantmentType.GILDED: "gilded",
            EnchantmentType.BLESSED: "blessed",
            EnchantmentType.BALANCED: "spiked",
            EnchantmentType.SHADOW: "shadow",
            EnchantmentType.FIRE: "fireproof",
            EnchantmentType.ICE: "snuggly",
            EnchantmentType.HOLY: "hexed",
            EnchantmentType.DARK: "haloed"
        }
        return labels.get(self, self.value.lower())


class Enchantment:
    """Represents an enchantment that can be applied to weapons or armor."""
    
    def __init__(self, enchantment_type, target_type="weapon"):
        self.type = enchantment_type
        self.target_type = target_type  # "weapon" or "armor"
        if target_type == "weapon":
            self.name = enchantment_type.get_weapon_label()
        else:
            self.name = enchantment_type.get_armor_label()
        self.attack_traits = self._get_attack_traits()
        self.resistances = self._get_resistances()
    
    def get_weapon_attack_bonus(self):
        """Get the attack bonus when applied to weapons."""
        if self.type == EnchantmentType.QUALITY:
            return 3
        elif self.type == EnchantmentType.BALANCED:
            return 0  # Defense bonus, not attack
        return 0
    
    def get_armor_attack_bonus(self):
        """Get the attack bonus when applied to armor."""
        if self.type == EnchantmentType.BALANCED:
            return 1  # Spiked armor gives attack
        return 0
    
    def get_weapon_defense_bonus(self):
        """Get the defense bonus when applied to weapons."""
        if self.type == EnchantmentType.BALANCED:
            return 1  # Bolstered weapon gives defense
        return 0
    
    def get_armor_defense_bonus(self):
        """Get the defense bonus when applied to armor."""
        if self.type == EnchantmentType.QUALITY:
            return 3
        return 0
    
    def get_weapon_fov_bonus(self):
        """Get the FOV bonus when applied to weapons."""
        if self.type == EnchantmentType.GLOWING:
            return 3
        return 0
    
    def get_armor_fov_bonus(self):
        """Get the FOV bonus when applied to armor."""  
        if self.type == EnchantmentType.GLOWING:
            return 3
        return 0
    
    def get_weapon_attack_multiplier_bonus(self):
        """Get the attack multiplier bonus when applied to weapons."""
        if self.type == EnchantmentType.SHINY:
            return 0.25  # 25% bonus = 1.25x damage
        return 0.0
    
    def get_armor_defense_multiplier_bonus(self):
        """Get the defense multiplier bonus when applied to armor."""
        if self.type == EnchantmentType.SHINY:
            return 0.25  # 25% bonus = 1.25x defense
        return 0.0
    
    def get_xp_multiplier_bonus(self):
        """Get the XP multiplier bonus (same for weapon/armor)."""
        if self.type == EnchantmentType.GILDED:
            return 0.05  # 5% bonus
        return 0.0
    
    def get_health_aspect_bonus(self):
        """Get the health aspect bonus (same for weapon/armor)."""
        if self.type == EnchantmentType.BLESSED:
            return 0.10  # 10% bonus
        return 0.0
    
    def get_weapon_crit_bonus(self):
        """Get the crit chance bonus when applied to weapons."""
        if self.type == EnchantmentType.RENDING:
            return 0.05  # 5% crit chance bonus
        return 0.0
    
    def get_armor_evade_bonus(self):
        """Get the evade chance bonus when applied to armor."""
        if self.type == EnchantmentType.SHADOW:
            return 0.05  # 5% evade chance bonus
        return 0.0
    
    def _get_attack_traits(self):
        """Get the attack traits provided by this enchantment."""
        if self.target_type != "weapon":
            return []
        
        trait_map = {
            EnchantmentType.FIRE: [Trait.FIRE],
            EnchantmentType.ICE: [Trait.ICE],
            EnchantmentType.HOLY: [Trait.HOLY],
            EnchantmentType.DARK: [Trait.DARK]
        }
        return trait_map.get(self.type, [])
    
    def _get_resistances(self):
        """Get the resistances provided by this enchantment."""
        if self.target_type != "armor":
            return []
        
        resistance_map = {
            EnchantmentType.FIRE: [Trait.FIRE],
            EnchantmentType.ICE: [Trait.ICE],
            EnchantmentType.HOLY: [Trait.HOLY],
            EnchantmentType.DARK: [Trait.DARK]
        }
        return resistance_map.get(self.type, [])


def get_random_weapon_enchantment():
    """Get a random enchantment for weapons."""
    weapon_enchantments = [e for e in EnchantmentType if e.can_enchant_weapon]
    enchantment_type = random.choice(weapon_enchantments)
    return Enchantment(enchantment_type, "weapon")


def get_random_armor_enchantment():
    """Get a random enchantment for armor."""
    armor_enchantments = [e for e in EnchantmentType if e.can_enchant_armor]
    enchantment_type = random.choice(armor_enchantments)
    return Enchantment(enchantment_type, "armor")


def get_weapon_enchantment_by_type(enchantment_type):
    """Get a weapon enchantment of a specific type."""
    if not enchantment_type.can_enchant_weapon:
        raise ValueError(f"Enchantment {enchantment_type} cannot be applied to weapons")
    return Enchantment(enchantment_type, "weapon")


def get_armor_enchantment_by_type(enchantment_type):
    """Get an armor enchantment of a specific type."""
    if not enchantment_type.can_enchant_armor:
        raise ValueError(f"Enchantment {enchantment_type} cannot be applied to armor")
    return Enchantment(enchantment_type, "armor")


def get_random_enchantment():
    """Get a random weapon enchantment (deprecated - use get_random_weapon_enchantment)."""
    return get_random_weapon_enchantment()


def get_enchantment_by_type(enchantment_type):
    """Get a weapon enchantment of a specific type (deprecated - use get_weapon_enchantment_by_type)."""
    return get_weapon_enchantment_by_type(enchantment_type)


def should_spawn_with_enchantment():
    """Check if a weapon should spawn with an enchantment."""
    return random.random() < WEAPON_ENCHANT_CHANCE


def should_armor_spawn_with_enchantment():
    """Check if armor should spawn with an enchantment."""
    return random.random() < ARMOR_ENCHANT_CHANCE