"""
Factory functions for creating random items.
"""

import random
from .consumables import HealthPotion, Beef, Elixir, Carrot, SalmonOfKnowledge, PowerCatalyst, DefenseCatalyst, D6, JewelerCatalyst, BaronCatalyst, WardenCatalyst, BaronsBoon, JewelersBoon, MinersBoon, ClericsBoon, WardensBoon, JokersBoon
from .weapons import Dagger, Sword, Longsword, WarHammer, BrightSword, ClericsStaff, Gauntlets, Weapon
from .armor import LeatherArmor, ChainMail, PlateArmor, DragonScale, SafetyVest, SpikedArmor
from .accessories import PowerRing, ProtectionRing, GreaterPowerRing, GreaterProtectionRing, Rosary, HeadLamp, BaronsCrown, JewelersCap, AceOfSpades
from .enchantments import should_spawn_with_enchantment, get_random_enchantment


# ============================================================================
# ITEM POOLS - Edit these to change what items appear at different levels
# ============================================================================

DEFAULT_CONSUMABLES = [Beef, SalmonOfKnowledge, D6]
# Boons (can appear from floor 2+)
ENCHANTMENT_BOONS = [BaronsBoon, JewelersBoon, MinersBoon, ClericsBoon, WardensBoon, JokersBoon]

# Consumable item pools
# Power and Defense Catalysts found in all levels, D6 found in all levels
EARLY_GAME_CONSUMABLES = [Carrot, PowerCatalyst, DefenseCatalyst, JewelerCatalyst] + DEFAULT_CONSUMABLES
MID_GAME_CONSUMABLES = [Carrot, PowerCatalyst, DefenseCatalyst] + DEFAULT_CONSUMABLES + ENCHANTMENT_BOONS
LATE_GAME_CONSUMABLES = [BaronCatalyst, WardenCatalyst] + DEFAULT_CONSUMABLES + ENCHANTMENT_BOONS
END_GAME_CONSUMABLES = [BaronCatalyst, WardenCatalyst, Elixir] + DEFAULT_CONSUMABLES + ENCHANTMENT_BOONS

# Weapon item pools
# Cleric's Staff: early-late game, Bright Sword: mid & late game
EARLY_GAME_WEAPONS = [Dagger, Sword, ClericsStaff]
MID_GAME_WEAPONS = [Sword, Longsword, BrightSword, ClericsStaff, Gauntlets]
LATE_GAME_WEAPONS = [Longsword, WarHammer, BrightSword, ClericsStaff, Gauntlets]
END_GAME_WEAPONS = [WarHammer, BrightSword, Gauntlets]

# Armor item pools
# Added SpikedArmor in mid-late game range
EARLY_GAME_ARMOR = [LeatherArmor, SafetyVest]
MID_GAME_ARMOR = [LeatherArmor, ChainMail, SafetyVest, SpikedArmor]
LATE_GAME_ARMOR = [ChainMail, PlateArmor, SpikedArmor]
END_GAME_ARMOR = [PlateArmor, DragonScale]

# Mostly for testing new things, may need to rebalance
DEFAULT_ACCESSORIES = [BaronsCrown, JewelersCap, AceOfSpades]
# Accessory item pools
EARLY_GAME_ACCESSORIES = []  # No accessories in early game
MID_GAME_ACCESSORIES = [PowerRing, Rosary, HeadLamp] + DEFAULT_ACCESSORIES  # Single item list is fine
LATE_GAME_ACCESSORIES = [GreaterPowerRing, ProtectionRing, Rosary, HeadLamp] + DEFAULT_ACCESSORIES
END_GAME_ACCESSORIES = [GreaterPowerRing, GreaterProtectionRing, Rosary, HeadLamp] + DEFAULT_ACCESSORIES

# Drop chances (adjust these to change item frequency)
# this is the default, cranking it up to test some stuff

CONSUMABLE_CHANCE = 0.4  # 40% chance for consumables
HEALTH_POTION_CHANCE = 0.5  # 50% of consumables are health potions

# Equipment type weights for each tier
EARLY_GAME_EQUIPMENT_TYPES = ['weapon', 'weapon', 'armor']  # No accessories, increased weapons chances early
MID_GAME_EQUIPMENT_TYPES = ['weapon', 'weapon', 'armor', 'accessory']
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
        
        # 67% health potions, 33% other consumables
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
            weapon = random.choice(weapon_pool)(x, y)
            # 25% chance to spawn with an enchantment
            if should_spawn_with_enchantment():
                enchantment = get_random_enchantment()
                weapon.add_enchantment(enchantment)
            return weapon
        elif item_type == 'armor' and armor_pool:
            return random.choice(armor_pool)(x, y)
        elif item_type == 'accessory' and accessory_pool:
            return random.choice(accessory_pool)(x, y)
        else:
            # Fallback to weapon if requested type is empty
            if weapon_pool:
                weapon = random.choice(weapon_pool)(x, y)
                # 25% chance to spawn with an enchantment
                if should_spawn_with_enchantment():
                    enchantment = get_random_enchantment()
                    weapon.add_enchantment(enchantment)
                return weapon
            elif armor_pool:
                return random.choice(armor_pool)(x, y)
            else:
                return HealthPotion(x, y)  # Ultimate fallback