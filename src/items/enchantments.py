"""
Unified enchantment system for weapons and armor.
Backward compatibility module that imports from the new enchantments package.
"""

# Import everything from the new enchantments package for backward compatibility
from enchantments import (
    EnchantmentType,
    Enchantment,
    get_random_weapon_enchantment,
    get_random_armor_enchantment,
    get_weapon_enchantment_by_type,
    get_armor_enchantment_by_type,
    get_random_enchantment,
    get_enchantment_by_type,
    should_spawn_with_enchantment,
    should_armor_spawn_with_enchantment
)

# Also expose the constants for backward compatibility
from enchantments.utils import WEAPON_ENCHANT_CHANCE, ARMOR_ENCHANT_CHANCE

# Export everything for backward compatibility
__all__ = [
    'EnchantmentType',
    'Enchantment',
    'get_random_weapon_enchantment',
    'get_random_armor_enchantment',
    'get_weapon_enchantment_by_type',
    'get_armor_enchantment_by_type',
    'get_random_enchantment',
    'get_enchantment_by_type',
    'should_spawn_with_enchantment',
    'should_armor_spawn_with_enchantment',
    'WEAPON_ENCHANT_CHANCE',
    'ARMOR_ENCHANT_CHANCE'
]