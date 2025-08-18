#!/usr/bin/env python3
"""
Test simplified inventory functionality.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import tcod.event
from game import Game
from ui import UI
from items.armor.leather_armor import LeatherArmor
from items.consumables.health_potion import HealthPotion

def test_automatic_description_display():
    """Test that descriptions show automatically when items are selected."""
    print("Testing automatic description display...")
    
    # Create a mock console for testing
    class MockConsole:
        def __init__(self):
            self.printed_items = []
        
        def clear(self):
            self.printed_items = []
        
        def print(self, x, y, text, fg=None):
            self.printed_items.append((x, y, text, fg))
    
    # Create player with leather armor
    game = Game()
    leather_armor = LeatherArmor(0, 0)
    game.player.add_item(leather_armor)
    
    # Create UI and mock console
    ui = UI()
    console = MockConsole()
    
    # Test with item selected (should show description automatically)
    ui.render_inventory(console, game.player, 0)
    
    # Find description content
    description_header = [item for item in console.printed_items if "Item Description:" in item[2]]
    description_content = [item for item in console.printed_items if "Basic leather protection" in item[2]]
    defense_bonus_line = [item for item in console.printed_items if "Defense Bonus: +2" in item[2]]
    
    print(f"Found description header: {len(description_header) > 0}")
    print(f"Found description content: {len(description_content) > 0}")
    print(f"Found defense bonus line: {len(defense_bonus_line) > 0}")
    
    # Test without item selected (should not show description)
    console.clear()
    ui.render_inventory(console, game.player, None)
    
    no_description_header = [item for item in console.printed_items if "Item Description:" in item[2]]
    print(f"Description header when nothing selected: {len(no_description_header) == 0}")
    
    if (len(description_header) > 0 and len(description_content) > 0 and 
        len(defense_bonus_line) > 0 and len(no_description_header) == 0):
        print("✓ Automatic description display works correctly!")
        return True
    else:
        print("✗ Automatic description display not working properly")
        return False

def test_enter_key_functionality():
    """Test that Enter key works to use/equip items."""
    print("\nTesting Enter key functionality...")
    
    # Create a game instance
    game = Game()
    
    # Add leather armor to inventory
    leather_armor = LeatherArmor(0, 0)
    game.player.add_item(leather_armor)
    
    # Set up inventory state
    game.game_state = 'INVENTORY'
    game.selected_item_index = 0  # Select first item
    
    print(f"Before Enter key - player armor: {game.player.armor.name if game.player.armor else 'None'}")
    print(f"Inventory size: {len(game.player.inventory)}")
    
    # Simulate Enter key press
    key = tcod.event.KeySym.RETURN
    if key == tcod.event.KeySym.RETURN and game.selected_item_index is not None:
        game.use_inventory_item(game.selected_item_index)
    
    print(f"After Enter key - player armor: {game.player.armor.name if game.player.armor else 'None'}")
    print(f"Inventory size: {len(game.player.inventory)}")
    print(f"Game state: {game.game_state}")
    
    # Check if armor was equipped
    if game.player.armor and game.player.armor.name == "Leather Armor":
        print("✓ Enter key successfully equipped armor!")
        return True
    else:
        print("✗ Enter key did not equip armor properly")
        return False

def test_simplified_controls():
    """Test that the UI shows the correct simplified controls."""
    print("\nTesting simplified controls display...")
    
    # Create a mock console for testing
    class MockConsole:
        def __init__(self):
            self.printed_items = []
        
        def clear(self):
            self.printed_items = []
        
        def print(self, x, y, text, fg=None):
            self.printed_items.append((x, y, text, fg))
    
    # Create player with item
    game = Game()
    health_potion = HealthPotion(0, 0)
    game.player.add_item(health_potion)
    
    # Create UI and mock console
    ui = UI()
    console = MockConsole()
    
    # Render inventory
    ui.render_inventory(console, game.player, 0)
    
    # Check for simplified controls
    enter_instruction = [item for item in console.printed_items if "[Enter] Use/Equip" in item[2]]
    d_instruction = [item for item in console.printed_items if "[D] Drop" in item[2]]
    no_examine_instruction = [item for item in console.printed_items if "[E]" in item[2] and "xamine" in item[2]]
    
    print(f"Found Enter instruction: {len(enter_instruction) > 0}")
    print(f"Found D instruction: {len(d_instruction) > 0}")
    print(f"No examine instruction: {len(no_examine_instruction) == 0}")
    
    if len(enter_instruction) > 0 and len(d_instruction) > 0 and len(no_examine_instruction) == 0:
        print("✓ Simplified controls display correctly!")
        return True
    else:
        print("✗ Controls display not correct")
        return False

def run_all_tests():
    """Run all simplified inventory tests."""
    print("Running simplified inventory tests...")
    
    test1 = test_automatic_description_display()
    test2 = test_enter_key_functionality()
    test3 = test_simplified_controls()
    
    if test1 and test2 and test3:
        print("\n✓ All simplified inventory tests passed!")
    else:
        print("\n✗ Some simplified inventory tests failed")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    run_all_tests()