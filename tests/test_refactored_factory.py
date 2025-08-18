#!/usr/bin/env python3
"""
Test the refactored item factory functionality.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from items.factory import create_random_item_for_level
from items.consumables.health_potion import HealthPotion
from items.weapons.dagger import Dagger
from items.weapons.sword import Sword
from items.weapons.longsword import Longsword
from items.weapons.war_hammer import WarHammer
from items.armor.leather_armor import LeatherArmor
from items.armor.chain_mail import ChainMail
from items.armor.plate_armor import PlateArmor
from items.armor.dragon_scale import DragonScale
from items.accessories.power_ring import PowerRing
from items.accessories.protection_ring import ProtectionRing

def test_item_generation_consistency():
    """Test that item generation produces consistent results for each level range."""
    print("Testing item generation consistency...")
    
    # Test early game items (levels 1-2)
    early_items = []
    for _ in range(50):  # Generate many items to test distribution
        item = create_random_item_for_level(1, 0, 0)
        early_items.append(type(item).__name__)
    
    print(f"Early game items generated: {set(early_items)}")
    
    # Should only contain early game items
    valid_early_items = {'HealthPotion', 'Dagger', 'Sword', 'LeatherArmor'}
    actual_early_items = set(early_items)
    
    if actual_early_items.issubset(valid_early_items):
        print("✓ Early game item generation is correct")
    else:
        invalid_items = actual_early_items - valid_early_items
        print(f"✗ Invalid early game items: {invalid_items}")
        return False
    
    # Test end game items (level 10)
    end_items = []
    for _ in range(50):
        item = create_random_item_for_level(10, 0, 0)
        end_items.append(type(item).__name__)
    
    print(f"End game items generated: {set(end_items)}")
    
    # Should only contain end game items
    valid_end_items = {'HealthPotion', 'WarHammer', 'PlateArmor', 'DragonScale', 'PowerRing', 'ProtectionRing'}
    actual_end_items = set(end_items)
    
    if actual_end_items.issubset(valid_end_items):
        print("✓ End game item generation is correct")
    else:
        invalid_items = actual_end_items - valid_end_items
        print(f"✗ Invalid end game items: {invalid_items}")
        return False
    
    return True

def test_single_item_pools():
    """Test that single-item pools work correctly."""
    print("\nTesting single-item pools...")
    
    # Test early game armor (should only be LeatherArmor)
    armor_items = []
    for _ in range(20):
        # Force armor generation by testing multiple times
        item = create_random_item_for_level(1, 0, 0)
        if hasattr(item, 'equipment_slot') and item.equipment_slot == 'armor':
            armor_items.append(type(item).__name__)
    
    if armor_items:
        unique_armor = set(armor_items)
        print(f"Early game armor generated: {unique_armor}")
        
        if unique_armor == {'LeatherArmor'}:
            print("✓ Single-item armor pool works correctly")
        else:
            print(f"✗ Expected only LeatherArmor, got: {unique_armor}")
            return False
    else:
        print("Note: No armor items generated in sample (due to randomness)")
    
    # Test end game weapons (should only be WarHammer)
    weapon_items = []
    for _ in range(20):
        item = create_random_item_for_level(10, 0, 0)
        if hasattr(item, 'equipment_slot') and item.equipment_slot == 'weapon':
            weapon_items.append(type(item).__name__)
    
    if weapon_items:
        unique_weapons = set(weapon_items)
        print(f"End game weapons generated: {unique_weapons}")
        
        if unique_weapons == {'WarHammer'}:
            print("✓ Single-item weapon pool works correctly")
        else:
            print(f"✗ Expected only WarHammer, got: {unique_weapons}")
            return False
    else:
        print("Note: No weapon items generated in sample (due to randomness)")
    
    return True

def test_progression_scaling():
    """Test that item quality scales with level."""
    print("\nTesting item progression scaling...")
    
    # Test that high-level items don't appear early
    for level in [1, 2]:
        items = []
        for _ in range(30):
            item = create_random_item_for_level(level, 0, 0)
            items.append(type(item).__name__)
        
        # DragonScale and WarHammer should never appear at low levels
        forbidden_items = {'DragonScale', 'WarHammer'}
        actual_items = set(items)
        
        if not forbidden_items.intersection(actual_items):
            print(f"✓ Level {level}: No high-tier items generated")
        else:
            found_forbidden = forbidden_items.intersection(actual_items)
            print(f"✗ Level {level}: Found forbidden items: {found_forbidden}")
            return False
    
    # Test that low-level items can still appear at high levels (for some pools)
    high_level_items = []
    for _ in range(30):
        item = create_random_item_for_level(10, 0, 0)
        high_level_items.append(type(item).__name__)
    
    # Health potions should still appear at high levels
    if 'HealthPotion' in high_level_items:
        print("✓ Health potions still appear at high levels")
    else:
        print("✗ Health potions should appear at all levels")
        return False
    
    return True

def test_accessory_progression():
    """Test that accessories appear at appropriate levels."""
    print("\nTesting accessory progression...")
    
    # Early game should have no accessories
    early_accessories = []
    for _ in range(50):
        item = create_random_item_for_level(1, 0, 0)
        if hasattr(item, 'equipment_slot') and item.equipment_slot == 'accessory':
            early_accessories.append(type(item).__name__)
    
    if not early_accessories:
        print("✓ No accessories in early game")
    else:
        print(f"✗ Found accessories in early game: {set(early_accessories)}")
        return False
    
    # Mid game should have accessories
    mid_accessories = []
    for _ in range(50):
        item = create_random_item_for_level(4, 0, 0)
        if hasattr(item, 'equipment_slot') and item.equipment_slot == 'accessory':
            mid_accessories.append(type(item).__name__)
    
    if mid_accessories:
        print(f"✓ Accessories found in mid game: {set(mid_accessories)}")
    else:
        print("Note: No accessories generated in mid game sample (due to randomness)")
    
    return True

def run_all_tests():
    """Run all refactored factory tests."""
    print("Running refactored factory tests...")
    
    test1 = test_item_generation_consistency()
    test2 = test_single_item_pools()
    test3 = test_progression_scaling()
    test4 = test_accessory_progression()
    
    if test1 and test2 and test3 and test4:
        print("\n✓ All refactored factory tests passed!")
    else:
        print("\n✗ Some refactored factory tests failed")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    run_all_tests()