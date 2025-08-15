"""Test that inventory displays items in reverse order (newest first)."""

import unittest
from unittest.mock import MagicMock
from src.ui import UI
from src.player import Player
from src.items.consumables import HealthPotion


class TestInventoryReverseOrder(unittest.TestCase):
    """Test the inventory reverse order display."""
    
    def setUp(self):
        """Set up test environment."""
        self.ui = UI()
        self.player = Player(5, 5)
        # Create mock console
        self.console = MagicMock()
        self.console.clear = MagicMock()
        self.console.print = MagicMock()
        
    def test_inventory_displays_newest_first(self):
        """Test that inventory shows newest items first."""
        # Clear the starting inventory
        self.player.inventory.clear()
        
        # Add items in order
        item1 = HealthPotion(0, 0)
        item1.name = "First Potion"
        item2 = HealthPotion(0, 0) 
        item2.name = "Second Potion"
        item3 = HealthPotion(0, 0)
        item3.name = "Third Potion"
        
        self.player.inventory.append(item1)
        self.player.inventory.append(item2)
        self.player.inventory.append(item3)
        
        # Render inventory
        self.ui.render_inventory(self.console, self.player)
        
        # Check the order of display
        calls = self.console.print.call_args_list
        
        # Find the inventory item lines
        inventory_lines = []
        for call in calls:
            args = call[0]
            if len(args) >= 3:
                text = str(args[2])
                # Look for lines with item format (letter) [type] name
                if ") [C]" in text and "Potion" in text:
                    inventory_lines.append(text)
        
        # Should have 3 items displayed
        self.assertEqual(len(inventory_lines), 3)
        
        # Check that newest item (Third Potion) appears first in display
        # but has the correct letter (c) since it's at index 2
        self.assertIn("c) [C] Third Potion", inventory_lines[0])
        self.assertIn("b) [C] Second Potion", inventory_lines[1]) 
        self.assertIn("a) [C] First Potion", inventory_lines[2])
    
    def test_selection_works_with_reverse_order(self):
        """Test that item selection still works correctly with reverse display."""
        # Clear and add items
        self.player.inventory.clear()
        
        item1 = HealthPotion(0, 0)
        item1.name = "First Potion"
        item2 = HealthPotion(0, 0)
        item2.name = "Second Potion"
        
        self.player.inventory.append(item1)
        self.player.inventory.append(item2)
        
        # Select the first item (index 0, but displayed second due to reverse order)
        self.ui.render_inventory(self.console, self.player, selected_item_index=0)
        
        # Check that the correct item is highlighted
        calls = self.console.print.call_args_list
        
        first_item_highlighted = False
        second_item_highlighted = False
        
        for call in calls:
            args = call[0]
            kwargs = call[1] if len(call) > 1 else {}
            if len(args) >= 3:
                text = str(args[2])
                color = kwargs.get('fg')
                
                if "a) [C] First Potion" in text:
                    from constants import COLOR_GREEN
                    if color == COLOR_GREEN:
                        first_item_highlighted = True
                elif "b) [C] Second Potion" in text:
                    from constants import COLOR_GREEN
                    if color == COLOR_GREEN:
                        second_item_highlighted = True
        
        # First item (index 0) should be highlighted, second should not
        self.assertTrue(first_item_highlighted, "First item (index 0) should be highlighted")
        self.assertFalse(second_item_highlighted, "Second item should not be highlighted")


if __name__ == '__main__':
    unittest.main()