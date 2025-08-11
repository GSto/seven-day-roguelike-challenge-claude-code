"""
Items package for the roguelike game.
"""

from .base import Item, Consumable, Equipment
from .consumables import (HealthPotion, PowerCatalyst, DefenseCatalyst, D6, 
                           BaronCatalyst, WardenCatalyst, JewelerCatalyst)
from .weapons import Weapon, WoodenStick, Dagger, Sword, Longsword, WarHammer, ClericsStaff
from .armor import Armor, WhiteTShirt, LeatherArmor, ChainMail, PlateArmor, DragonScale, SpikedArmor
from .accessories import Accessory, Ring, PowerRing, ProtectionRing
from .factory import create_random_item_for_level

# Export all item classes for easy importing
__all__ = [
    # Base classes
    'Item', 'Consumable', 'Equipment',
    
    # Consumables
    'HealthPotion', 'PowerCatalyst', 'DefenseCatalyst', 'D6',
    'BaronCatalyst', 'WardenCatalyst', 'JewelerCatalyst',
    
    # Weapons
    'Weapon', 'WoodenStick', 'Dagger', 'Sword', 'Longsword', 'WarHammer', 'ClericsStaff',
    
    # Armor
    'Armor', 'WhiteTShirt', 'LeatherArmor', 'ChainMail', 'PlateArmor', 'DragonScale', 'SpikedArmor',
    
    # Accessories
    'Accessory', 'Ring', 'PowerRing', 'ProtectionRing',
    
    # Factory function
    'create_random_item_for_level'
]