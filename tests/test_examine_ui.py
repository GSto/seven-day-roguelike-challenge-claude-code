#!/usr/bin/env python3
"""
Test examine UI functionality.
"""
import sys
sys.path.append('src')

from game import Game
from ui import UI
from items.armor import LeatherArmor

def test_examine_ui():
    """Test that examine shows descriptions in UI."""
    
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
    
    # Test without showing description
    ui.render_inventory(console, game.player, 0, False)
    
    description_lines_without = [item for item in console.printed_items if "Basic leather protection" in item[2]]
    print(f"Description lines without examine: {len(description_lines_without)}")
    
    # Test with showing description
    console.clear()
    ui.render_inventory(console, game.player, 0, True)
    
    description_lines_with = [item for item in console.printed_items if "Basic leather protection" in item[2]]
    print(f"Description lines with examine: {len(description_lines_with)}")
    
    # Find all lines with description content
    all_description_content = [item for item in console.printed_items if any(word in item[2] for word in ["Basic", "leather", "protection", "Defense Bonus"])]
    print("Description content found:")
    for item in all_description_content:
        print(f"  {item[2]}")
    
    if len(description_lines_with) > 0:
        print("✓ Description is shown when examine is active!")
    else:
        print("✗ Description is not being shown properly")
    
    return True

if __name__ == "__main__":
    test_examine_ui()