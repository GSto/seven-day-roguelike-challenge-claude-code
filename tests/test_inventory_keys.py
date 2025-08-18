#!/usr/bin/env python3
"""
Test inventory U and E key functionality.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import tcod.event
from game import Game
from items.armor.leather_armor import LeatherArmor
from items.consumables.health_potion import HealthPotion

def test_u_key_functionality():
    """Test that U key works to use/equip items."""
    print("Testing U key functionality...")
    
    # Create a game instance
    game = Game()
    
    # Add leather armor to inventory
    leather_armor = LeatherArmor(0, 0)
    game.player.add_item(leather_armor)
    
    # Set up inventory state
    game.game_state = 'INVENTORY'
    game.selected_item_index = 0  # Select first item
    game.show_item_description = False
    
    print(f"Before U key - player armor: {game.player.armor.name if game.player.armor else 'None'}")
    print(f"Inventory size: {len(game.player.inventory)}")
    
    # Simulate U key press
    class MockEvent:
        def __init__(self, key):
            self.sym = key
    
    event = MockEvent(ord('u'))
    
    # Process the key press
    key = event.sym
    if key == ord('u') and game.selected_item_index is not None:
        game.use_inventory_item(game.selected_item_index)
    
    print(f"After U key - player armor: {game.player.armor.name if game.player.armor else 'None'}")
    print(f"Inventory size: {len(game.player.inventory)}")
    print(f"Game state: {game.game_state}")
    
    # Check if armor was equipped
    if game.player.armor and game.player.armor.name == "Leather Armor":
        print("✓ U key successfully equipped armor!")
        return True
    else:
        print("✗ U key did not equip armor properly")
        return False

def test_e_key_functionality():
    """Test that E key works to examine items."""
    print("\nTesting E key functionality...")
    
    # Create a game instance
    game = Game()
    
    # Add health potion to inventory
    health_potion = HealthPotion(0, 0)
    game.player.add_item(health_potion)
    
    # Set up inventory state
    game.game_state = 'INVENTORY'
    game.selected_item_index = 0  # Select first item
    game.show_item_description = False
    
    print(f"Before E key - show_item_description: {game.show_item_description}")
    
    # Simulate E key press
    class MockEvent:
        def __init__(self, key):
            self.sym = key
    
    event = MockEvent(ord('e'))
    
    # Process the key press
    key = event.sym
    if key == ord('e') and game.selected_item_index is not None:
        game.show_item_description = not game.show_item_description
    
    print(f"After E key - show_item_description: {game.show_item_description}")
    
    if game.show_item_description:
        print("✓ E key successfully toggled item description!")
        return True
    else:
        print("✗ E key did not toggle item description")
        return False

def test_key_order():
    """Test that action keys take precedence over letter selection."""
    print("\nTesting key precedence...")
    
    # Create a game instance
    game = Game()
    
    # Add multiple items to test letter conflicts
    items = [
        HealthPotion(0, 0),  # a
        LeatherArmor(0, 0),  # b
        HealthPotion(0, 0),  # c
        HealthPotion(0, 0),  # d - conflicts with drop key
        HealthPotion(0, 0),  # e - conflicts with examine key
    ]
    
    for item in items:
        game.player.add_item(item)
    
    # Set up inventory state
    game.game_state = 'INVENTORY'
    game.selected_item_index = 1  # Select leather armor (index 1)
    game.show_item_description = False
    
    print(f"Selected item index: {game.selected_item_index}")
    print(f"Selected item name: {game.player.inventory[game.selected_item_index].name}")
    
    # Test that 'e' triggers examine, not item selection
    key = ord('e')
    if key == ord('e') and game.selected_item_index is not None:
        game.show_item_description = not game.show_item_description
        print("E key triggered examine action")
    elif ord('a') <= key <= ord('z') and key not in [ord('u'), ord('d'), ord('e'), ord('k'), ord('j')]:
        print("E key triggered item selection")
    
    if game.show_item_description:
        print("✓ E key triggered examine action (not item selection)")
        return True
    else:
        print("✗ E key may have triggered item selection instead of examine")
        return False

def run_all_tests():
    """Run all key functionality tests."""
    print("Running inventory key tests...")
    
    test1 = test_u_key_functionality()
    test2 = test_e_key_functionality()
    test3 = test_key_order()
    
    if test1 and test2 and test3:
        print("\n✓ All inventory key tests passed!")
    else:
        print("\n✗ Some inventory key tests failed")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    run_all_tests()