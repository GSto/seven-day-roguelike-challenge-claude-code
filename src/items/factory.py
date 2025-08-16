"""
Factory functions for creating random items.
"""

import random
# Import from organized consumable subcategories
from .foods import HealthPotion, Beef, Chicken, Elixir, Carrot, SalmonOfKnowledge, Antidote, ShellPotion, MezzoForte, MagicMushroom
from .catalysts import PowerCatalyst, DefenseCatalyst, JewelerCatalyst, BaronCatalyst, WardenCatalyst, ReapersCatalyst, ShadowsCatalyst, FireAttackCatalyst, IceAttackCatalyst, HolyAttackCatalyst, DarkAttackCatalyst, FireResistanceCatalyst, IceResistanceCatalyst, HolyResistanceCatalyst, DarkResistanceCatalyst
from .boons import BaronsBoon, JewelersBoon, MinersBoon, ClericsBoon, JokersBoon, ReapersBoon
from .consumables import D6 
from .weapons import * 
from .armor import * 
from .accessories import  * 
from .enchantments import * 


# ============================================================================
# ITEM POOLS - Edit these to change what items appear at different levels
# ============================================================================

# Taken out of rotation until they can be balanced 
# Accessory: Psychic's Turban: way to much ATK bonus 
# Armor: Skin Suit: still gets way to much DEF

DEFAULT_CONSUMABLES = [Beef, Chicken, SalmonOfKnowledge, D6, MagicMushroom, Carrot]
STATUS_CONSUMABLES = [Antidote, ShellPotion, MezzoForte]
# Boons (can appear from floor 2+)
ENCHANTMENT_BOONS = [BaronsBoon, JewelersBoon, MinersBoon, ClericsBoon, JokersBoon, ReapersBoon]
CATALYSTS = [PowerCatalyst, DefenseCatalyst, JewelerCatalyst, ReapersCatalyst, ShadowsCatalyst, BaronCatalyst, WardenCatalyst, FireAttackCatalyst, IceAttackCatalyst, HolyAttackCatalyst, DarkAttackCatalyst, FireResistanceCatalyst, IceResistanceCatalyst, HolyResistanceCatalyst, DarkResistanceCatalyst]

BASE_CONSUMABLES = DEFAULT_CONSUMABLES + STATUS_CONSUMABLES + ENCHANTMENT_BOONS  + CATALYSTS

# Consumable item pools
EARLY_GAME_CONSUMABLES =  BASE_CONSUMABLES
MID_GAME_CONSUMABLES =   BASE_CONSUMABLES
LATE_GAME_CONSUMABLES =  BASE_CONSUMABLES
END_GAME_CONSUMABLES = [Elixir] + BASE_CONSUMABLES
# Weapon item pools
EARLY_GAME_WEAPONS = [Dagger, Sword, Shield, Katana]
MID_GAME_WEAPONS = [Sword, Shield, Axe, MorningStar, ClericsStaff, Gauntlets, MateriaStaff, Uchigatana, Pickaxe, SnakesFang, Rapier]
LATE_GAME_WEAPONS = [Longsword, MorningStar, WarHammer, WarScythe, TowerShield, Gauntlets, MateriaStaff, Uchigatana, Pickaxe, Rapier]
END_GAME_WEAPONS = [WarHammer, RiversOfBlood, WarScythe]

# Armor item pools
DEFAULT_ARMOR = [SpikedArmor, GamblersVest, MinimalSuit]
EARLY_GAME_ARMOR = [LeatherArmor, SafetyVest, Cloak] + DEFAULT_ARMOR
MID_GAME_ARMOR = [LeatherArmor, ChainMail, SafetyVest, NightCloak] + DEFAULT_ARMOR
LATE_GAME_ARMOR = [ChainMail, PlateArmor, NightCloak, ShadowCloak] + DEFAULT_ARMOR
END_GAME_ARMOR = [PlateArmor, DragonScale, ShadowCloak]

CARDS = [AceOfHearts, AceOfClubs, AceOfDiamonds, AceOfSpades, Joker]
# Actually think I am going to put most accessories here, except for some that are specifcally not for early or late game
DEFAULT_ACCESSORIES = [BaronsCrown, JewelersCap, Rosary, HeadLamp, ShadowRing, RingOfPrecision, BrutalityAmulet, AssassinsMask, GravePact, SturdyRock, PunishTheWeak]
# Accessory item pools
EARLY_GAME_ACCESSORIES = []  # No accessories in early game
MID_GAME_ACCESSORIES = [PowerRing, ProtectionRing] + DEFAULT_ACCESSORIES  # Single item list is fine
LATE_GAME_ACCESSORIES = [GreaterPowerRing, ProtectionRing] + DEFAULT_ACCESSORIES
END_GAME_ACCESSORIES = [GreaterPowerRing, GreaterProtectionRing] + DEFAULT_ACCESSORIES

# Drop chances (adjust these to change item frequency)
# this is the default, cranking it up to test some stuff

CONSUMABLE_CHANCE = 0.6  # 60% chance for consumables
HEALTH_POTION_CHANCE = 0.3  # 50% of consumables are health potions

# Equipment type weights for each tier
EARLY_GAME_EQUIPMENT_TYPES = ['weapon', 'armor', 'accessory']  # No accessories, increased weapons chances early
MID_GAME_EQUIPMENT_TYPES = ['weapon', 'armor', 'accessory', 'accessory', 'accessory']
LATE_GAME_EQUIPMENT_TYPES = ['weapon', 'armor', 'accessory', 'accessory', 'accessory']
END_GAME_EQUIPMENT_TYPES = ['weapon', 'armor', 'accessory']


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_random_item_for_level(level_number, x, y):
    """Create a random item appropriate for the given dungeon level."""
    # Special case: Level 10 always spawns exactly one DemonSlayer weapon
    # This should be handled at the level generation level, but we can help here too
    if level_number == 10 and random.random() < 0.1:  # 10% chance for any item to be DemonSlayer on level 10
        return DemonSlayer(x, y)
    
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
            can_be_enchanted = not getattr(weapon, 'no_initial_enchantments', False)
            #chance to spawn with an enchantment
            if should_spawn_with_enchantment() and can_be_enchanted:
                enchantment = get_random_enchantment()
                weapon.add_enchantment(enchantment)
            return weapon
        elif item_type == 'armor' and armor_pool:
            armor = random.choice(armor_pool)(x, y)
            if should_spawn_with_enchantment():
                enchantment = get_random_armor_enchantment()
                armor.add_enchantment(enchantment)
            return armor
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