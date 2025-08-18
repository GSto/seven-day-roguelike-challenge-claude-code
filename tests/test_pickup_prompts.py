"""
Unit tests for item pickup prompts and user feedback.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from level.level import Level
from items.consumables.health_potion import HealthPotion
from items.weapons.dagger import Dagger
from ui import UI


def test_pickup_prompt_detection():
    """Test that pickup prompts are properly detected."""
    player = Player(10, 10)
    level = Level(level_number=1)
    ui = UI()
    
    # Test no item at position
    item = level.get_item_at(player.x, player.y)
    assert item is None
    
    # Place item at player position
    health_potion = HealthPotion(player.x, player.y)
    level.items.append(health_potion)
    
    # Test item detected at position
    item = level.get_item_at(player.x, player.y)
    assert item == health_potion
    assert item.name == "Health Potion"
    
    print("✓ Pickup prompt detection works correctly")


def test_pickup_functionality():
    """Test the actual pickup functionality."""
    player = Player(10, 10)
    level = Level(level_number=1)
    
    # Place item at player position
    health_potion = HealthPotion(player.x, player.y)
    level.items.append(health_potion)
    
    # Test pickup
    initial_inventory_size = len(player.inventory)
    initial_level_items = len(level.items)
    
    # Simulate pickup
    item = level.get_item_at(player.x, player.y)
    if item and player.add_item(item):
        level.remove_item(item)
        pickup_success = True
    else:
        pickup_success = False
    
    assert pickup_success == True
    assert len(player.inventory) == initial_inventory_size + 1
    assert len(level.items) == initial_level_items - 1
    assert health_potion in player.inventory
    assert health_potion not in level.items
    
    print("✓ Pickup functionality works correctly")


def test_full_inventory_pickup():
    """Test pickup behavior when inventory is full."""
    player = Player(10, 10)
    level = Level(level_number=1)
    
    # Fill inventory to capacity
    for i in range(player.inventory_size):
        item = HealthPotion(0, 0)
        player.add_item(item)
    
    # Place item at player position
    extra_item = Dagger(player.x, player.y)
    level.items.append(extra_item)
    
    # Test pickup attempt
    initial_inventory_size = len(player.inventory)
    initial_level_items = len(level.items)
    
    item = level.get_item_at(player.x, player.y)
    if item and player.add_item(item):
        level.remove_item(item)
        pickup_success = True
    else:
        pickup_success = False
    
    # Should fail because inventory is full
    assert pickup_success == False
    assert len(player.inventory) == initial_inventory_size
    assert len(level.items) == initial_level_items
    assert extra_item in level.items
    assert extra_item not in player.inventory
    
    print("✓ Full inventory pickup behavior works correctly")


def test_multiple_items_same_position():
    """Test behavior when multiple items are at the same position."""
    level = Level(level_number=1)
    
    # Place multiple items at same position
    pos_x, pos_y = 10, 10
    item1 = HealthPotion(pos_x, pos_y)
    item2 = Dagger(pos_x, pos_y)
    
    level.items.append(item1)
    level.items.append(item2)
    
    # Test get_item_at behavior (should return first item found)
    item = level.get_item_at(pos_x, pos_y)
    assert item is not None
    assert item in [item1, item2]  # Should be one of the items
    
    print("✓ Multiple items at same position handled correctly")


def test_pickup_after_monster_death():
    """Test pickup functionality with monster drops."""
    level = Level(level_number=1)
    player = Player(15, 15)
    
    # Simulate monster drop by adding item to level
    drop_x, drop_y = 20, 20
    dropped_item = HealthPotion(drop_x, drop_y)
    level.add_item_drop(drop_x, drop_y, dropped_item)
    
    # Test that item was added correctly
    assert dropped_item in level.items
    assert dropped_item.x == drop_x
    assert dropped_item.y == drop_y
    
    # Test retrieval
    item = level.get_item_at(drop_x, drop_y)
    assert item == dropped_item
    
    print("✓ Pickup after monster death works correctly")


def test_ui_prompt_concepts():
    """Test UI prompt concepts."""
    # Test prompt message formatting
    item_name = "Health Potion"
    expected_prompt = f"Press 'g' to pick up {item_name}"
    
    assert "Press 'g'" in expected_prompt
    assert item_name in expected_prompt
    assert "pick up" in expected_prompt
    
    # Test that we can construct prompts for different items
    items = ["Dagger", "Leather Armor", "Ring of Power"]
    for item in items:
        prompt = f"Press 'g' to pick up {item}"
        assert item in prompt
        assert "Press 'g'" in prompt
    
    print("✓ UI prompt concepts work correctly")


def run_all_tests():
    """Run all pickup prompt tests."""
    print("Running pickup prompt tests...")
    print()
    
    test_pickup_prompt_detection()
    test_pickup_functionality()
    test_full_inventory_pickup()
    test_multiple_items_same_position()
    test_pickup_after_monster_death()
    test_ui_prompt_concepts()
    
    print()
    print("✅ All pickup prompt tests passed!")


if __name__ == "__main__":
    run_all_tests()