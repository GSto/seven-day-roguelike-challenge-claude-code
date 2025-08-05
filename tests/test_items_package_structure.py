"""
Test the new items package structure to ensure all imports work correctly.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_base_imports():
    """Test importing base classes from items package."""
    from items import Item, Consumable, Equipment
    
    # Test that classes are properly imported
    assert Item is not None
    assert Consumable is not None
    assert Equipment is not None
    
    print("✓ Base classes import correctly")


def test_consumable_imports():
    """Test importing consumable classes."""
    from items import HealthPotion
    
    # Create instances to ensure they work
    health_potion = HealthPotion(5, 5)
    
    assert health_potion.name == "Health Potion"
    assert hasattr(health_potion, 'heal_amount')
    
    print("✓ Consumable classes import and work correctly")


def test_weapon_imports():
    """Test importing weapon classes."""
    from items import Weapon, WoodenStick, Dagger, Sword, Longsword, WarHammer
    
    # Create instances to ensure they work
    wooden_stick = WoodenStick(5, 5)
    dagger = Dagger(5, 5)
    sword = Sword(5, 5)
    longsword = Longsword(5, 5)
    war_hammer = WarHammer(5, 5)
    
    # Test properties
    assert wooden_stick.equipment_slot == "weapon"
    assert dagger.attack_bonus == 3
    assert sword.attack_bonus == 5
    assert longsword.attack_bonus == 8
    assert war_hammer.attack_bonus == 12
    
    print("✓ Weapon classes import and work correctly")


def test_armor_imports():
    """Test importing armor classes."""
    from items import Armor, WhiteTShirt, LeatherArmor, ChainMail, PlateArmor, DragonScale
    
    # Create instances to ensure they work
    white_tshirt = WhiteTShirt(5, 5)
    leather_armor = LeatherArmor(5, 5)
    chain_mail = ChainMail(5, 5)
    plate_armor = PlateArmor(5, 5)
    dragon_scale = DragonScale(5, 5)
    
    # Test properties
    assert white_tshirt.equipment_slot == "armor"
    assert white_tshirt.defense_bonus == 0
    assert leather_armor.defense_bonus == 2
    assert chain_mail.defense_bonus == 4
    assert plate_armor.defense_bonus == 6
    assert dragon_scale.defense_bonus == 10
    
    print("✓ Armor classes import and work correctly")


def test_accessory_imports():
    """Test importing accessory classes."""
    from items import Accessory, Ring, PowerRing, ProtectionRing
    
    # Create instances to ensure they work
    power_ring = PowerRing(5, 5)
    protection_ring = ProtectionRing(5, 5)
    
    # Test properties
    assert power_ring.equipment_slot == "accessory"
    assert power_ring.attack_bonus == 3
    assert power_ring.defense_bonus == 1
    assert protection_ring.defense_bonus == 3
    
    print("✓ Accessory classes import and work correctly")


def test_factory_import():
    """Test importing factory function."""
    from items import create_random_item_for_level
    
    # Test creating items for different levels
    item_level_1 = create_random_item_for_level(1, 10, 10)
    item_level_5 = create_random_item_for_level(5, 10, 10)
    item_level_10 = create_random_item_for_level(10, 10, 10)
    
    # Verify items are created successfully
    assert item_level_1 is not None
    assert item_level_5 is not None
    assert item_level_10 is not None
    
    # Verify they have basic item properties
    assert hasattr(item_level_1, 'name')
    assert hasattr(item_level_5, 'name')
    assert hasattr(item_level_10, 'name')
    
    print("✓ Factory function imports and works correctly")


def test_all_exports():
    """Test that all expected items are exported from __init__.py."""
    import items
    
    # Test that all expected classes are available
    expected_classes = [
        'Item', 'Consumable', 'Equipment',
        'HealthPotion',
        'Weapon', 'WoodenStick', 'Dagger', 'Sword', 'Longsword', 'WarHammer',
        'Armor', 'WhiteTShirt', 'LeatherArmor', 'ChainMail', 'PlateArmor', 'DragonScale',
        'Accessory', 'Ring', 'PowerRing', 'ProtectionRing',
        'create_random_item_for_level'
    ]
    
    for class_name in expected_classes:
        assert hasattr(items, class_name), f"Missing export: {class_name}"
    
    print("✓ All expected classes are properly exported")


def test_package_structure():
    """Test that the package structure is correct."""
    import items.base
    import items.consumables
    import items.weapons
    import items.armor
    import items.accessories
    import items.factory
    
    # Test that each module has expected classes
    assert hasattr(items.base, 'Item')
    assert hasattr(items.consumables, 'HealthPotion')
    assert hasattr(items.weapons, 'Weapon')
    assert hasattr(items.armor, 'Armor')
    assert hasattr(items.accessories, 'Accessory')
    assert hasattr(items.factory, 'create_random_item_for_level')
    
    print("✓ Package structure is correct")


def test_backwards_compatibility():
    """Test that existing import patterns still work."""
    # These should work exactly as they did before
    from items import HealthPotion, create_random_item_for_level
    from items import WoodenStick, WhiteTShirt
    
    # Test creating items as before
    health_potion = HealthPotion(5, 5)
    wooden_stick = WoodenStick(5, 5)
    white_tshirt = WhiteTShirt(5, 5)
    random_item = create_random_item_for_level(3, 10, 10)
    
    # Verify they work as expected
    assert health_potion.name == "Health Potion"
    assert wooden_stick.name == "Wooden Stick"
    assert white_tshirt.name == "White T-Shirt"
    assert random_item is not None
    
    print("✓ Backwards compatibility maintained")


def run_all_tests():
    """Run all package structure tests."""
    print("Running items package structure tests...")
    print()
    
    test_base_imports()
    test_consumable_imports()  
    test_weapon_imports()
    test_armor_imports()
    test_accessory_imports()
    test_factory_import()
    test_all_exports()
    test_package_structure()
    test_backwards_compatibility()
    
    print()
    print("✅ All items package structure tests passed!")


if __name__ == "__main__":
    run_all_tests()