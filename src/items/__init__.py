"""
Items package for the roguelike game.
"""

from .item import Item
from .consumable import Consumable
from .equipment import Equipment
# Import from new modular structure
from .weapons.base import Weapon
from .weapons.wooden_stick import WoodenStick
from .weapons.dagger import Dagger
from .weapons.sword import Sword
from .weapons.longsword import Longsword
from .weapons.war_hammer import WarHammer
from .weapons.clerics_staff import ClericsStaff

from .armor.base import Armor
from .armor.white_tshirt import WhiteTShirt
from .armor.leather_armor import LeatherArmor
from .armor.chain_mail import ChainMail
from .armor.plate_armor import PlateArmor
from .armor.dragon_scale import DragonScale
from .armor.spiked_armor import SpikedArmor

from .accessories.accessory import Accessory
from .accessories.ring import Ring
from .accessories.power_ring import PowerRing
from .accessories.protection_ring import ProtectionRing

from .consumables.health_potion import HealthPotion
from .consumables.d6 import D6
from .consumables.power_catalyst import PowerCatalyst
from .consumables.defense_catalyst import DefenseCatalyst
from .consumables.baron_catalyst import BaronCatalyst
from .consumables.warden_catalyst import WardenCatalyst
from .consumables.jeweler_catalyst import JewelerCatalyst
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