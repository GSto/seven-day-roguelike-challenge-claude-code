#!/usr/bin/env python3
"""
Quick test to verify inventory highlighting works.
"""
import sys
sys.path.append('src')

from game import Game
from ui import UI
from player import Player
from items import HealthPotion

def test_inventory_highlight():
    """Test that inventory highlighting works correctly."""
    # Create a mock console for testing
    class MockConsole:
        def __init__(self):
            self.printed_items = []
        
        def clear(self):
            self.printed_items = []
        
        def print(self, x, y, text, fg=None):
            self.printed_items.append((x, y, text, fg))
    
    # Create player with some items
    player = Player(10, 10)
    potion = HealthPotion(0, 0)
    player.add_item(potion)
    
    # Create UI and mock console
    ui = UI()
    console = MockConsole()
    
    # Test without selection
    ui.render_inventory(console, player, None, False)
    
    # Find the item line
    item_line = None
    for item in console.printed_items:
        if "Health Potion" in item[2]:
            item_line = item
            break
    
    print(f"Without selection: {item_line}")
    
    # Test with selection
    console.clear()
    ui.render_inventory(console, player, 0, False)
    
    # Find the item line again
    item_line_selected = None
    for item in console.printed_items:
        if "Health Potion" in item[2]:
            item_line_selected = item
            break
    
    print(f"With selection: {item_line_selected}")
    
    # Check if colors are different
    if item_line and item_line_selected:
        if item_line[3] != item_line_selected[3]:
            print("✓ Item highlighting works - colors are different!")
            return True
        else:
            print("✗ Item highlighting not working - colors are the same")
            return False
    else:
        print("✗ Could not find item lines in output")
        return False

if __name__ == "__main__":
    test_inventory_highlight()