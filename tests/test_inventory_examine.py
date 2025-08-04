#!/usr/bin/env python3
"""
Test inventory examine functionality.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
from ui import UI
from items.armor import LeatherArmor
from items.consumables import HealthPotion

def test_examine_functionality():
    """Test that examine shows descriptions in correct location."""
    print("Testing inventory examine functionality...")
    
    # Create a mock console for testing
    class MockConsole:
        def __init__(self):
            self.printed_items = []
        
        def clear(self):
            self.printed_items = []
        
        def print(self, x, y, text, fg=None):
            self.printed_items.append((x, y, text, fg))
    
    # Create player with leather armor and health potion
    game = Game()
    leather_armor = LeatherArmor(0, 0)
    health_potion = HealthPotion(0, 0)
    game.player.add_item(leather_armor)
    game.player.add_item(health_potion)
    
    # Create UI and mock console
    ui = UI()
    console = MockConsole()
    
    # Test examining leather armor (index 0)
    ui.render_inventory(console, game.player, 0, True)
    
    # Find equipped items section
    equipped_lines = [item for item in console.printed_items if "Currently Equipped:" in item[2]]
    print(f"Found equipped section: {len(equipped_lines) > 0}")
    
    # Find description section
    description_header = [item for item in console.printed_items if "Item Description:" in item[2]]
    description_content = [item for item in console.printed_items if "Basic leather protection" in item[2]]
    defense_bonus_line = [item for item in console.printed_items if "Defense Bonus: +2" in item[2]]
    
    print(f"Found description header: {len(description_header) > 0}")
    print(f"Found description content: {len(description_content) > 0}")
    print(f"Found defense bonus line: {len(defense_bonus_line) > 0}")
    
    # Check positioning - description should come after equipped items
    if equipped_lines and description_header:
        equipped_y = equipped_lines[0][1]
        description_y = description_header[0][1]
        print(f"Equipped section at Y: {equipped_y}")
        print(f"Description section at Y: {description_y}")
        if description_y > equipped_y:
            print("✓ Description appears after equipped items")
        else:
            print("✗ Description does not appear after equipped items")
    
    # Test examining health potion (index 1)
    console.clear()
    ui.render_inventory(console, game.player, 1, True)
    
    potion_description = [item for item in console.printed_items if "Restores health" in item[2]]
    heal_amount_line = [item for item in console.printed_items if "Heals: 30 HP" in item[2]]
    
    print(f"Found potion description: {len(potion_description) > 0}")
    print(f"Found heal amount line: {len(heal_amount_line) > 0}")
    
    if (len(description_header) > 0 and len(description_content) > 0 and 
        len(defense_bonus_line) > 0 and len(heal_amount_line) > 0):
        print("✓ All examine functionality tests passed!")
        return True
    else:
        print("✗ Some examine functionality tests failed")
        return False

def run_all_tests():
    """Run all examine functionality tests."""
    print("Running inventory examine tests...")
    
    test_examine_functionality()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    run_all_tests()