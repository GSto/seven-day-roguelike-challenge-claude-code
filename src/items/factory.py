"""
Factory functions for creating random items.
"""

import random
from .consumables import HealthPotion, Beef, Chicken, Elixir, Carrot, SalmonOfKnowledge, PowerCatalyst, DefenseCatalyst, D6, JewelerCatalyst, BaronCatalyst, WardenCatalyst, BaronsBoon, JewelersBoon, MinersBoon, ClericsBoon, WardensBoon, JokersBoon, ReapersCatalyst, ShadowsCatalyst, ReapersBoon
from .weapons import Dagger, Sword, Axe, Longsword, MorningStar, WarHammer, ClericsStaff, Gauntlets, Shield, TowerShield, MateriaStaff, Katana, Uchigatana, RiversOfBlood, WarScythe
from .armor import LeatherArmor, ChainMail, PlateArmor, DragonScale, SafetyVest, SpikedArmor, GamblersVest, Cloak, NightCloak, ShadowCloak, SkinSuit
from .accessories import PowerRing, ProtectionRing, GreaterPowerRing, GreaterProtectionRing, Rosary, HeadLamp, BaronsCrown, JewelersCap, AceOfSpades, AceOfClubs, AceOfDiamonds, AceOfHearts, Joker, ShadowRing, RingOfPrecision, BrutalityAmulet, AssassinsMask, PsychicsTurban
from .enchantments import should_spawn_with_enchantment, get_random_enchantment


# ============================================================================
# ITEM POOLS - Edit these to change what items appear at different levels
# ============================================================================

DEFAULT_CONSUMABLES = [Beef, Chicken, SalmonOfKnowledge, D6]
# Boons (can appear from floor 2+)
ENCHANTMENT_BOONS = [BaronsBoon, JewelersBoon, MinersBoon, ClericsBoon, WardensBoon, JokersBoon, ReapersBoon]

BASE_CONSUMABLES = DEFAULT_CONSUMABLES + ENCHANTMENT_BOONS 

# Consumable item pools
EARLY_GAME_CONSUMABLES = [Carrot, PowerCatalyst, DefenseCatalyst, JewelerCatalyst] + BASE_CONSUMABLES
MID_GAME_CONSUMABLES = [Carrot, PowerCatalyst, DefenseCatalyst, ReapersCatalyst, ShadowsCatalyst] + BASE_CONSUMABLES
LATE_GAME_CONSUMABLES = [BaronCatalyst, WardenCatalyst, ReapersCatalyst, ShadowsCatalyst] + BASE_CONSUMABLES
END_GAME_CONSUMABLES = [BaronCatalyst, WardenCatalyst, ReapersCatalyst, ShadowsCatalyst, Elixir] + BASE_CONSUMABLES
# Weapon item pools
EARLY_GAME_WEAPONS = [Dagger, Sword, Shield, MateriaStaff, Katana]
MID_GAME_WEAPONS = [Sword, Shield, Axe, Longsword, MorningStar, ClericsStaff, Gauntlets, MateriaStaff, Uchigatana]
LATE_GAME_WEAPONS = [Longsword, MorningStar, WarHammer, WarScythe, TowerShield, Gauntlets, MateriaStaff, Uchigatana]
END_GAME_WEAPONS = [WarHammer, RiversOfBlood, WarScythe]

# Armor item pools
DEFAULT_ARMOR = [SpikedArmor, GamblersVest, SkinSuit]
EARLY_GAME_ARMOR = [LeatherArmor, SafetyVest, Cloak] + DEFAULT_ARMOR
MID_GAME_ARMOR = [LeatherArmor, ChainMail, SafetyVest, NightCloak] + DEFAULT_ARMOR
LATE_GAME_ARMOR = [ChainMail, PlateArmor, NightCloak, ShadowCloak] + DEFAULT_ARMOR
END_GAME_ARMOR = [PlateArmor, DragonScale, ShadowCloak]

CARDS = [AceOfHearts, AceOfClubs, AceOfDiamonds, AceOfSpades, Joker]
# Actually think I am going to put most accessories here, except for some that are specifcally not for early or late game
DEFAULT_ACCESSORIES = [BaronsCrown, JewelersCap, Rosary, HeadLamp, ShadowRing, RingOfPrecision, BrutalityAmulet, AssassinsMask, PsychicsTurban]
# Accessory item pools
EARLY_GAME_ACCESSORIES = []  # No accessories in early game
MID_GAME_ACCESSORIES = [PowerRing, ProtectionRing] + DEFAULT_ACCESSORIES  # Single item list is fine
LATE_GAME_ACCESSORIES = [GreaterPowerRing, ProtectionRing] + DEFAULT_ACCESSORIES
END_GAME_ACCESSORIES = [GreaterPowerRing, GreaterProtectionRing] + DEFAULT_ACCESSORIES

# Drop chances (adjust these to change item frequency)
# this is the default, cranking it up to test some stuff

CONSUMABLE_CHANCE = 0.4  # 40% chance for consumables
HEALTH_POTION_CHANCE = 0.5  # 50% of consumables are health potions

# Equipment type weights for each tier
EARLY_GAME_EQUIPMENT_TYPES = ['weapon', 'weapon', 'armor']  # No accessories, increased weapons chances early
MID_GAME_EQUIPMENT_TYPES = ['weapon', 'armor', 'accessory', 'accessory', 'accessory']
LATE_GAME_EQUIPMENT_TYPES = ['weapon', 'armor', 'accessory', 'accessory', 'accessory']
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