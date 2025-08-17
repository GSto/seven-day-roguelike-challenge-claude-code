"""
Enchantments package for the roguelike game.
"""

from .enchantment_type import EnchantmentType
from .enchantment import Enchantment
from .utils import (
    get_random_weapon_enchantment,
    get_random_armor_enchantment,
    get_weapon_enchantment_by_type,
    get_armor_enchantment_by_type,
    get_random_enchantment,
    get_enchantment_by_type,
    should_spawn_with_enchantment,
    should_armor_spawn_with_enchantment,
    WEAPON_ENCHANT_CHANCE,
    ARMOR_ENCHANT_CHANCE
)

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