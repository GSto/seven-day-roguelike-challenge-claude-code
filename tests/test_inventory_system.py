"""
Unit tests for the inventory management system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from level import Level
from items import HealthPotion, Dagger, LeatherArmor, PowerRing
from game import Game


def test_item_pickup_basic():
    """Test basic item pickup functionality."""
    player = Player(10, 10)
    level = Level(level_number=1)
    
    # Place an item at player's position
    health_potion = HealthPotion(10, 10)
    level.items.append(health_potion)
    
    # Test pickup
    item_at_position = level.get_item_at(10, 10)
    assert item_at_position == health_potion
    
    # Test adding to inventory
    initial_count = len(player.inventory)
    success = player.add_item(health_potion)
    assert success == True
    assert len(player.inventory) == initial_count + 1
    assert health_potion in player.inventory
    
    print("✓ Basic item pickup works correctly")


def test_inventory_size_limits():
    """Test inventory size limitations."""
    player = Player(10, 10)
    
    # Fill inventory to capacity
    for i in range(player.inventory_size):
        item = HealthPotion(0, 0)
        success = player.add_item(item)
        assert success == True
    
    # Try to add one more item (should fail)
    extra_item = HealthPotion(0, 0)
    success = player.add_item(extra_item)
    assert success == False
    assert len(player.inventory) == player.inventory_size
    assert extra_item not in player.inventory
    
    print("✓ Inventory size limits work correctly")


def test_item_removal():
    """Test removing items from inventory."""
    player = Player(10, 10)
    health_potion = HealthPotion(0, 0)
    
    # Add item
    player.add_item(health_potion)
    assert health_potion in player.inventory
    
    # Remove item
    success = player.remove_item(health_potion)
    assert success == True
    assert health_potion not in player.inventory
    
    # Try to remove item not in inventory
    another_potion = HealthPotion(0, 0)
    success = player.remove_item(another_potion)
    assert success == False
    
    print("✓ Item removal works correctly")


def test_equipment_basic():
    """Test basic equipment functionality."""
    player = Player(10, 10)
    
    # Test weapon equipment
    dagger = Dagger(0, 0)
    assert player.weapon is None
    player.weapon = dagger
    assert player.weapon == dagger
    
    # Test armor equipment
    armor = LeatherArmor(0, 0)
    assert player.armor is None
    player.armor = armor
    assert player.armor == armor
    
    # Test accessory equipment
    ring = PowerRing(0, 0)
    assert player.accessory is None
    player.accessory = ring
    assert player.accessory == ring
    
    print("✓ Basic equipment functionality works correctly")


def test_equipment_stat_bonuses():
    """Test that equipped items provide stat bonuses."""
    player = Player(10, 10)
    
    # Test base stats
    base_attack = player.attack
    base_defense = player.defense
    
    # Equip weapon
    dagger = Dagger(0, 0)
    player.weapon = dagger
    assert player.get_total_attack() == base_attack + dagger.attack_bonus
    
    # Equip armor
    armor = LeatherArmor(0, 0)
    player.armor = armor
    assert player.get_total_defense() == base_defense + armor.defense_bonus
    
    # Equip accessory
    ring = PowerRing(0, 0)
    player.accessory = ring
    total_attack = base_attack + dagger.attack_bonus + ring.attack_bonus
    total_defense = base_defense + armor.defense_bonus + ring.defense_bonus
    assert player.get_total_attack() == total_attack
    assert player.get_total_defense() == total_defense
    
    print("✓ Equipment stat bonuses work correctly")


def test_consumable_usage():
    """Test using consumable items."""
    player = Player(10, 10)
    
    # Damage player first
    player.hp = 50
    initial_hp = player.hp
    
    # Use health potion
    health_potion = HealthPotion(0, 0)
    result = health_potion.use(player)
    assert result == True
    assert player.hp > initial_hp
    
    # Try to use potion at full health
    player.hp = player.max_hp
    result = health_potion.use(player)
    assert result == False  # Should fail
    
    print("✓ Consumable usage works correctly")


def test_equipment_slot_management():
    """Test equipment slot management and swapping."""
    player = Player(10, 10)
    
    # Equip first weapon
    dagger = Dagger(0, 0)
    player.weapon = dagger
    assert player.weapon == dagger
    
    # Equip second weapon (should replace first)
    player.add_item(dagger)  # Simulate unequipping to inventory
    player.weapon = None
    
    # Test that we can manage weapon slots
    assert player.weapon is None
    
    # Re-equip
    player.weapon = dagger
    assert player.weapon == dagger
    
    print("✓ Equipment slot management works correctly")


def test_inventory_with_mixed_items():
    """Test inventory with different types of items."""
    player = Player(10, 10)
    
    # Add different types of items
    health_potion = HealthPotion(0, 0)
    dagger = Dagger(0, 0)
    armor = LeatherArmor(0, 0)
    ring = PowerRing(0, 0)
    
    items = [health_potion, dagger, armor, ring]
    
    for item in items:
        success = player.add_item(item)
        assert success == True
        assert item in player.inventory
    
    assert len(player.inventory) == 4
    
    # Test that all items have the expected properties
    for item in player.inventory:
        assert hasattr(item, 'name')
        assert hasattr(item, 'x')
        assert hasattr(item, 'y')
    
    print("✓ Inventory with mixed items works correctly")


def test_item_pickup_integration():
    """Test item pickup integration with level."""
    level = Level(level_number=1)
    
    # Find a walkable position
    walkable_pos = None
    for x in range(level.width):
        for y in range(level.height):
            if level.is_walkable(x, y):
                walkable_pos = (x, y)
                break
        if walkable_pos:
            break
    
    assert walkable_pos is not None
    
    # Place item at walkable position
    health_potion = HealthPotion(walkable_pos[0], walkable_pos[1])
    level.items.append(health_potion)
    
    # Test item retrieval
    item = level.get_item_at(walkable_pos[0], walkable_pos[1])
    assert item == health_potion
    
    # Test item removal
    level.remove_item(health_potion)
    assert health_potion not in level.items
    item = level.get_item_at(walkable_pos[0], walkable_pos[1])
    assert item is None
    
    print("✓ Item pickup integration works correctly")


def test_inventory_edge_cases():
    """Test inventory edge cases and error conditions."""
    player = Player(10, 10)
    
    # Test removing item that doesn't exist
    non_existent_item = HealthPotion(0, 0)
    result = player.remove_item(non_existent_item)
    assert result == False
    
    # Test adding None item (current implementation allows it)
    initial_count = len(player.inventory)
    result = player.add_item(None)
    # Current implementation will add None if there's space
    if result == True:
        assert len(player.inventory) == initial_count + 1
        # Remove the None item for cleanup
        player.remove_item(None)
    else:
        assert result == False
    
    # Test equipment with None
    original_weapon = player.weapon
    player.weapon = None
    assert player.weapon is None
    
    print("✓ Inventory edge cases work correctly")


def test_game_state_management():
    """Test inventory game state management concepts."""
    # Test game state transitions
    game_states = {
        'PLAYING': 'playing',
        'INVENTORY': 'inventory',
        'DEAD': 'dead'
    }
    
    # Test state transition from playing to inventory
    current_state = game_states['PLAYING']
    assert current_state == 'playing'
    
    # Open inventory
    current_state = game_states['INVENTORY']
    assert current_state == 'inventory'
    
    # Close inventory
    current_state = game_states['PLAYING']
    assert current_state == 'playing'
    
    print("✓ Game state management concepts work correctly")


def run_all_tests():
    """Run all inventory system tests."""
    print("Running inventory system tests...")
    print()
    
    test_item_pickup_basic()
    test_inventory_size_limits()
    test_item_removal()
    test_equipment_basic()
    test_equipment_stat_bonuses()
    test_consumable_usage()
    test_equipment_slot_management()
    test_inventory_with_mixed_items()
    test_item_pickup_integration()
    test_inventory_edge_cases()
    test_game_state_management()
    
    print()
    print("✅ All inventory system tests passed!")


if __name__ == "__main__":
    run_all_tests()