"""
Enchantment utility functions for the roguelike game.
"""

import random
from .enchantment_type import EnchantmentType
from .enchantment import Enchantment

# TODO: should be 25% by default. ramping up for testing
WEAPON_ENCHANT_CHANCE = 0.25
ARMOR_ENCHANT_CHANCE = 0.25


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