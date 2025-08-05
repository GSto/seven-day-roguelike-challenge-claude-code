"""
Factory functions for creating random items.
"""

import random
from .consumables import HealthPotion, Beef, Elixir, Carrot, SalmonOfKnowledge
from .weapons import Dagger, Sword, Longsword, WarHammer
from .armor import LeatherArmor, ChainMail, PlateArmor, DragonScale, SafetyVest
from .accessories import PowerRing, ProtectionRing, GreaterPowerRing, GreaterProtectionRing, Rosary, HeadLamp


# ============================================================================
# ITEM POOLS - Edit these to change what items appear at different levels
# ============================================================================

# Consumable item pools
EARLY_GAME_CONSUMABLES = [Carrot, SalmonOfKnowledge]
MID_GAME_CONSUMABLES = [Beef, Carrot, SalmonOfKnowledge]
LATE_GAME_CONSUMABLES = [Beef, SalmonOfKnowledge]
END_GAME_CONSUMABLES = [Elixir]

# Weapon item pools
EARLY_GAME_WEAPONS = [Dagger, Sword]
MID_GAME_WEAPONS = [Sword, Longsword]
LATE_GAME_WEAPONS = [Longsword, WarHammer]
END_GAME_WEAPONS = [WarHammer]  # Single item list is fine

# Armor item pools
EARLY_GAME_ARMOR = [LeatherArmor, SafetyVest]  # Single item list is fine
MID_GAME_ARMOR = [LeatherArmor, ChainMail, SafetyVest]
LATE_GAME_ARMOR = [ChainMail, PlateArmor]
END_GAME_ARMOR = [PlateArmor, DragonScale]

# Accessory item pools
EARLY_GAME_ACCESSORIES = []  # No accessories in early game
MID_GAME_ACCESSORIES = [PowerRing, Rosary, HeadLamp]  # Single item list is fine
LATE_GAME_ACCESSORIES = [GreaterPowerRing, ProtectionRing, Rosary, HeadLamp]
END_GAME_ACCESSORIES = [GreaterPowerRing, GreaterProtectionRing, Rosary, HeadLamp]

# Drop chances (adjust these to change item frequency)
# this is the default, cranking it up to test some stuff

CONSUMABLE_CHANCE = 0.4  # 40% chance for consumables
HEALTH_POTION_CHANCE = 0.67  # 80% of consumables are health potions

# Equipment type weights for each tier
EARLY_GAME_EQUIPMENT_TYPES = ['weapon', 'armor']  # No accessories
MID_GAME_EQUIPMENT_TYPES = ['weapon', 'armor', 'accessory']
LATE_GAME_EQUIPMENT_TYPES = ['weapon', 'armor', 'accessory']
END_GAME_EQUIPMENT_TYPES = ['weapon', 'armor', 'accessory']


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_random_item_for_level(level_number, x, y):
    """Create a random item appropriate for the given dungeon level."""
    # Item rarity based on level
    rand = random.random()
    
    # Check for consumable drop
    if rand < CONSUMABLE_CHANCE:
        # Choose consumable pool based on level
        if level_number <= 2:
            consumable_pool = EARLY_GAME_CONSUMABLES
        elif level_number <= 5:
            consumable_pool = MID_GAME_CONSUMABLES
        elif level_number <= 8:
            consumable_pool = LATE_GAME_CONSUMABLES
        else:
            consumable_pool = END_GAME_CONSUMABLES
        
        # 80% health potions, 20% other consumables
        if random.random() < HEALTH_POTION_CHANCE:
            return HealthPotion(x, y)
        else:
            # Choose from other consumables (excluding health potions)
            other_consumables = [item for item in consumable_pool if item != HealthPotion]
            if other_consumables:
                return random.choice(other_consumables)(x, y)
            else:
                return HealthPotion(x, y)  # Fallback to health potion
    
    else:
        # Equipment drop - choose pools based on level
        if level_number <= 2:
            # Early game items
            weapon_pool = EARLY_GAME_WEAPONS
            armor_pool = EARLY_GAME_ARMOR
            accessory_pool = EARLY_GAME_ACCESSORIES
            equipment_types = EARLY_GAME_EQUIPMENT_TYPES
        elif level_number <= 5:
            # Mid game items
            weapon_pool = MID_GAME_WEAPONS
            armor_pool = MID_GAME_ARMOR
            accessory_pool = MID_GAME_ACCESSORIES
            equipment_types = MID_GAME_EQUIPMENT_TYPES
        elif level_number <= 8:
            # Late game items
            weapon_pool = LATE_GAME_WEAPONS
            armor_pool = LATE_GAME_ARMOR
            accessory_pool = LATE_GAME_ACCESSORIES
            equipment_types = LATE_GAME_EQUIPMENT_TYPES
        else:
            # End game items
            weapon_pool = END_GAME_WEAPONS
            armor_pool = END_GAME_ARMOR
            accessory_pool = END_GAME_ACCESSORIES
            equipment_types = END_GAME_EQUIPMENT_TYPES
        
        # Choose equipment type
        item_type = random.choice(equipment_types)
        
        if item_type == 'weapon' and weapon_pool:
            return random.choice(weapon_pool)(x, y)
        elif item_type == 'armor' and armor_pool:
            return random.choice(armor_pool)(x, y)
        elif item_type == 'accessory' and accessory_pool:
            return random.choice(accessory_pool)(x, y)
        else:
            # Fallback to weapon if requested type is empty
            if weapon_pool:
                return random.choice(weapon_pool)(x, y)
            elif armor_pool:
                return random.choice(armor_pool)(x, y)
            else:
                return HealthPotion(x, y)  # Ultimate fallback