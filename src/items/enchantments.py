"""
Enchantment system for weapons.
"""

from enum import Enum
import random


class EnchantmentType(Enum):
    """Types of enchantments available for weapons."""
    QUALITY = "Quality"      # +3 Attack bonus
    SHINY = "Shiny"         # 1.25x damage multiplier 
    GLOWING = "Glowing"     # +2 FOV bonus
    GILDED = "Gilded"       # +5% XP bonus
    BLESSED = "Blessed"     # +5% healing aspect bonus
    BOLSTERED = "Bolstered" # +1 defense bonus
    RENDING = "Rending"     # +10% crit chance


class Enchantment:
    """Represents an enchantment on a weapon."""
    
    def __init__(self, enchantment_type):
        self.type = enchantment_type
        self.name = enchantment_type.value
    
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


def get_random_enchantment():
    """Get a random enchantment."""
    enchantment_type = random.choice(list(EnchantmentType))
    return Enchantment(enchantment_type)


def get_enchantment_by_type(enchantment_type):
    """Get an enchantment of a specific type."""
    return Enchantment(enchantment_type)


def should_spawn_with_enchantment():
    """Check if a weapon should spawn with an enchantment (25% chance)."""
    return random.random() < 0.25