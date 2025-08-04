"""
Factory functions for creating random items.
"""

import random
from .consumables import HealthPotion, ManaPotion
from .weapons import Dagger, Sword, Longsword, WarHammer
from .armor import LeatherArmor, ChainMail, PlateArmor, DragonScale
from .accessories import PowerRing, ProtectionRing


def create_random_item_for_level(level_number, x, y):
    """Create a random item appropriate for the given dungeon level."""
    # Item rarity based on level
    rand = random.random()
    
    # 40% chance for consumables, 60% for equipment
    if rand < 0.4:
        # Consumables
        if random.random() < 0.8:
            return HealthPotion(x, y)
        else:
            return ManaPotion(x, y)
    
    else:
        # Equipment - scale quality with level
        if level_number <= 2:
            # Early game items
            item_type = random.choice(['weapon', 'armor'])
            if item_type == 'weapon':
                return random.choice([Dagger, Sword])(x, y)
            else:
                return LeatherArmor(x, y)
        
        elif level_number <= 5:
            # Mid game items
            item_type = random.choice(['weapon', 'armor', 'accessory'])
            if item_type == 'weapon':
                return random.choice([Sword, Longsword])(x, y)
            elif item_type == 'armor':
                return random.choice([LeatherArmor, ChainMail])(x, y)
            else:
                return PowerRing(x, y)
        
        elif level_number <= 8:
            # Late game items
            item_type = random.choice(['weapon', 'armor', 'accessory'])
            if item_type == 'weapon':
                return random.choice([Longsword, WarHammer])(x, y)
            elif item_type == 'armor':
                return random.choice([ChainMail, PlateArmor])(x, y)
            else:
                return random.choice([PowerRing, ProtectionRing])(x, y)
        
        else:
            # End game items
            item_type = random.choice(['weapon', 'armor', 'accessory'])
            if item_type == 'weapon':
                return WarHammer(x, y)
            elif item_type == 'armor':
                return random.choice([PlateArmor, DragonScale])(x, y)
            else:
                return random.choice([PowerRing, ProtectionRing])(x, y)