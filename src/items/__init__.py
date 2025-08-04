"""
Items package for the roguelike game.
"""

from .base import Item, Consumable, Equipment
from .consumables import HealthPotion, ManaPotion
from .weapons import Weapon, WoodenStick, Dagger, Sword, Longsword, WarHammer
from .armor import Armor, WhiteTShirt, LeatherArmor, ChainMail, PlateArmor, DragonScale
from .accessories import Accessory, Ring, PowerRing, ProtectionRing
from .factory import create_random_item_for_level

# Export all item classes for easy importing
__all__ = [
    # Base classes
    'Item', 'Consumable', 'Equipment',
    
    # Consumables
    'HealthPotion', 'ManaPotion',
    
    # Weapons
    'Weapon', 'WoodenStick', 'Dagger', 'Sword', 'Longsword', 'WarHammer',
    
    # Armor
    'Armor', 'WhiteTShirt', 'LeatherArmor', 'ChainMail', 'PlateArmor', 'DragonScale',
    
    # Accessories
    'Accessory', 'Ring', 'PowerRing', 'ProtectionRing',
    
    # Factory function
    'create_random_item_for_level'
]