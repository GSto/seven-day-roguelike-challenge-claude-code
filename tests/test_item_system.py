"""
Unit tests for the item system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from items import (
    Item, Consumable, Equipment, 
    HealthPotion,
    Weapon, Armor, Accessory,
    Dagger, Sword, Longsword, WarHammer,
    LeatherArmor, ChainMail, PlateArmor, DragonScale,
    PowerRing, ProtectionRing,
    create_random_item_for_level
)
from player import Player
from level.level import Level


def test_basic_item_creation():
    """Test basic item creation and properties."""
    item = Item(5, 5, "Test Item", '?', (255, 255, 255), "A test item")
    
    assert item.x == 5
    assert item.y == 5
    assert item.name == "Test Item"
    assert item.char == '?'
    assert item.color == (255, 255, 255)
    assert item.description == "A test item"
    
    print("✓ Basic item creation works correctly")


def test_health_potion():
    """Test health potion creation and usage."""
    potion = HealthPotion(10, 10)
    player = Player(5, 5)
    
    # Test potion properties
    assert potion.name == "Health Potion"
    assert potion.char == '!'
    assert potion.effect_value == 1
    
    # Test healing when damaged
    player.hp = 50  # Damage player
    initial_hp = player.hp
    
    result = potion.use(player)
    assert result == True  # Should succeed
    assert player.hp == initial_hp + 30  # Should heal 30 HP
    
    # Test no healing when at full health
    player.hp = player.max_hp
    result = potion.use(player)
    assert result == False  # Should fail (already at full health)
    
    print("✓ Health potion functionality works correctly")

def test_weapon_creation():
    """Test weapon creation and properties."""
    dagger = Dagger(5, 5)
    sword = Sword(6, 6)
    longsword = Longsword(7, 7)
    hammer = WarHammer(8, 8)
    
    # Test dagger
    assert dagger.name == "Dagger"
    assert dagger.char == ')'
    assert dagger.attack_bonus == 3
    assert dagger.equipment_slot == "weapon"
    
    # Test sword
    assert sword.name == "Sword"
    assert sword.attack_bonus == 5
    
    # Test longsword
    assert longsword.name == "Longsword"
    assert longsword.attack_bonus == 8
    
    # Test war hammer
    assert hammer.name == "War Hammer"
    assert hammer.attack_bonus == 12
    
    print("✓ Weapon creation and properties work correctly")


def test_armor_creation():
    """Test armor creation and properties."""
    leather = LeatherArmor(5, 5)
    chain = ChainMail(6, 6)
    plate = PlateArmor(7, 7)
    dragon = DragonScale(8, 8)
    
    # Test leather armor
    assert leather.name == "Leather Armor"
    assert leather.char == '['
    assert leather.defense_bonus == 2
    assert leather.equipment_slot == "armor"
    
    # Test chain mail
    assert chain.name == "Chain Mail"
    assert chain.defense_bonus == 4
    
    # Test plate armor
    assert plate.name == "Plate Armor"
    assert plate.defense_bonus == 6
    
    # Test dragon scale
    assert dragon.name == "Dragon Scale Armor"
    assert dragon.defense_bonus == 10
    
    print("✓ Armor creation and properties work correctly")


def test_accessory_creation():
    """Test accessory creation and properties."""
    power_ring = PowerRing(5, 5)
    protection_ring = ProtectionRing(6, 6)
    
    # Test power ring
    assert power_ring.name == "Ring of Power"
    assert power_ring.char == '='
    assert power_ring.attack_bonus == 3
    assert power_ring.defense_bonus == 1
    assert power_ring.equipment_slot == "accessory"
    
    # Test protection ring
    assert protection_ring.name == "Ring of Protection"
    assert protection_ring.defense_bonus == 3
    assert protection_ring.attack_bonus == 0
    
    print("✓ Accessory creation and properties work correctly")


def test_random_item_generation():
    """Test random item generation for different levels."""
    # Test early level generation
    for _ in range(10):
        item = create_random_item_for_level(1, 5, 5)
        assert item is not None
        assert hasattr(item, 'name')
        assert hasattr(item, 'x')
        assert hasattr(item, 'y')
    
    # Test mid level generation
    for _ in range(10):
        item = create_random_item_for_level(5, 5, 5)
        assert item is not None
    
    # Test late level generation
    for _ in range(10):
        item = create_random_item_for_level(10, 5, 5)
        assert item is not None
    
    print("✓ Random item generation works correctly")


def test_level_item_placement():
    """Test item placement on levels."""
    level = Level(level_number=2)
    
    # Check that items were placed
    assert len(level.items) > 0
    
    # Check that items are in valid positions
    for item in level.items:
        assert 0 <= item.x < 80  # MAP_WIDTH
        assert 0 <= item.y < 43  # MAP_HEIGHT
        assert level.is_walkable(item.x, item.y)
    
    print(f"✓ Level item placement works correctly ({len(level.items)} items placed)")


def test_item_positioning_methods():
    """Test level item positioning and management methods."""
    level = Level(level_number=2)
    
    # Test is_item_at method
    if level.items:
        first_item = level.items[0]
        assert level.is_item_at(first_item.x, first_item.y) == True
        assert level.is_item_at(0, 0) == False  # Likely no item at origin
    
    # Test get_item_at method
    if level.items:
        first_item = level.items[0]
        retrieved_item = level.get_item_at(first_item.x, first_item.y)
        assert retrieved_item == first_item
        assert level.get_item_at(0, 0) is None  # Likely no item at origin
    
    # Test remove_item method
    if level.items:
        item_count = len(level.items)
        item_to_remove = level.items[0]
        level.remove_item(item_to_remove)
        assert len(level.items) == item_count - 1
        assert item_to_remove not in level.items
    
    print("✓ Item positioning and management methods work correctly")


def test_item_drop_mechanics():
    """Test item dropping from monsters."""
    level = Level(level_number=2)
    initial_item_count = len(level.items)
    
    # Test adding item drop
    health_potion = HealthPotion(10, 10)
    level.add_item_drop(15, 15, health_potion)
    
    # Check that item was added
    assert len(level.items) == initial_item_count + 1
    assert health_potion in level.items
    assert health_potion.x == 15
    assert health_potion.y == 15
    
    # Check that item can be retrieved
    retrieved_item = level.get_item_at(15, 15)
    assert retrieved_item == health_potion
    
    print("✓ Item drop mechanics work correctly")


def test_equipment_bonuses():
    """Test that equipment provides correct stat bonuses."""
    # Test weapon bonuses
    dagger = Dagger(5, 5)
    assert dagger.attack_bonus > 0
    assert dagger.defense_bonus == 0
    
    # Test armor bonuses  
    leather = LeatherArmor(5, 5)
    assert leather.defense_bonus > 0
    assert leather.attack_bonus == 0
    
    # Test accessory bonuses
    power_ring = PowerRing(5, 5)
    assert power_ring.attack_bonus > 0
    assert power_ring.defense_bonus > 0
    
    print("✓ Equipment bonuses work correctly")


def test_consumable_inheritance():
    """Test that consumables inherit properly from base classes."""
    health_potion = HealthPotion(5, 5)
    
    # Test inheritance chain
    assert isinstance(health_potion, Consumable)
    assert isinstance(health_potion, Item)
    
    # Test that consumable-specific attributes exist
    assert hasattr(health_potion, 'effect_value')
    assert hasattr(health_potion, 'use')
    
    print("✓ Consumable inheritance works correctly")


def test_equipment_inheritance():
    """Test that equipment inherits properly from base classes."""
    sword = Sword(5, 5)
    
    # Test inheritance chain
    assert isinstance(sword, Weapon)
    assert isinstance(sword, Equipment)
    assert isinstance(sword, Item)
    
    # Test that equipment-specific attributes exist
    assert hasattr(sword, 'attack_bonus')
    assert hasattr(sword, 'defense_bonus')
    assert hasattr(sword, 'equipment_slot')
    
    print("✓ Equipment inheritance works correctly")


def run_all_tests():
    """Run all item system tests."""
    print("Running item system tests...")
    print()
    
    test_basic_item_creation()
    test_health_potion()
    test_mana_potion()
    test_weapon_creation()
    test_armor_creation()
    test_accessory_creation()
    test_random_item_generation()
    test_level_item_placement()
    test_item_positioning_methods()
    test_item_drop_mechanics()
    test_equipment_bonuses()
    test_consumable_inheritance()
    test_equipment_inheritance()
    
    print()
    print("✅ All item system tests passed!")


if __name__ == "__main__":
    run_all_tests()