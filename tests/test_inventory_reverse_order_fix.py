"""Test that inventory reverse order display and navigation work correctly."""

import unittest
from unittest.mock import MagicMock
from src.game import Game
from src.player import Player
from src.items.consumables import HealthPotion
from src.ui import UI


class TestInventoryReverseOrderFix(unittest.TestCase):
    """Test the fixed inventory reverse order system."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = Game()
        self.game.player = Player(5, 5)
        self.game.ui = UI()
        # Clear starting inventory
        self.game.player.inventory.clear()
        
    def test_newest_item_gets_letter_a(self):
        """Test that the newest item gets letter 'a'."""
        # Add items in chronological order
        item1 = HealthPotion(0, 0)
        item1.name = "First Potion"
        item2 = HealthPotion(0, 0)
        item2.name = "Second Potion"
        item3 = HealthPotion(0, 0)
        item3.name = "Third Potion"
        
        self.game.player.inventory.append(item1)
        self.game.player.inventory.append(item2)
        self.game.player.inventory.append(item3)
        
        # Create mock console
        console = MagicMock()
        console.print = MagicMock()
        
        # Render inventory
        self.game.ui.render_inventory(console, self.game.player)
        
        # Find the inventory item lines
        calls = console.print.call_args_list
        inventory_lines = []
        for call in calls:
            args = call[0]
            if len(args) >= 3:
                text = str(args[2])
                if ") [C]" in text and "Potion" in text:
                    inventory_lines.append(text)
        
        # Should have 3 items displayed
        self.assertEqual(len(inventory_lines), 3)
        
        # Check that newest item (Third Potion) has letter 'a'
        self.assertIn("a) [C] Third Potion", inventory_lines[0])
        self.assertIn("b) [C] Second Potion", inventory_lines[1])
        self.assertIn("c) [C] First Potion", inventory_lines[2])
    
    def test_letter_selection_selects_correct_item(self):
        """Test that pressing 'a' selects the newest item."""
        # Add items
        item1 = HealthPotion(0, 0)
        item1.name = "First Potion"  
        item2 = HealthPotion(0, 0)
        item2.name = "Second Potion"
        item3 = HealthPotion(0, 0)
        item3.name = "Third Potion"
        
        self.game.player.inventory.append(item1)
        self.game.player.inventory.append(item2)
        self.game.player.inventory.append(item3)
        
        # Set up inventory state
        self.game.game_state = 'INVENTORY'
        self.game.selection_mode = "inventory"
        
        # Simulate pressing 'a' (should select newest item)
        import tcod.event
        key_event = tcod.event.KeyDown(sym=ord('a'), mod=0, scancode=0)
        self.game.handle_keydown(key_event)
        
        # Should select the third item (newest, index 2 in actual inventory)
        self.assertEqual(self.game.selected_item_index, 2)
        self.assertEqual(self.game.selection_mode, "inventory")
        
        # Simulate pressing 'c' (should select oldest item)
        key_event = tcod.event.KeyDown(sym=ord('c'), mod=0, scancode=0)
        self.game.handle_keydown(key_event)
        
        # Should select the first item (oldest, index 0 in actual inventory)
        self.assertEqual(self.game.selected_item_index, 0)
    
    def test_navigation_up_down_works_correctly(self):
        """Test that up/down navigation works intuitively with display order."""
        # Add items
        item1 = HealthPotion(0, 0)
        item1.name = "First Potion"
        item2 = HealthPotion(0, 0) 
        item2.name = "Second Potion"
        item3 = HealthPotion(0, 0)
        item3.name = "Third Potion"
        
        self.game.player.inventory.append(item1)
        self.game.player.inventory.append(item2)
        self.game.player.inventory.append(item3)
        
        # Start at newest item (should be selected by default)
        self.game.game_state = 'INVENTORY'
        self.game.selection_mode = "inventory"
        self.game.selected_item_index = 2  # Third item (newest)
        
        # Navigate down should go to second item
        self.game.navigate_down()
        self.assertEqual(self.game.selected_item_index, 1)  # Second item
        
        # Navigate down again should go to first item (oldest)
        self.game.navigate_down()
        self.assertEqual(self.game.selected_item_index, 0)  # First item
        
        # Navigate up should go back to second item
        self.game.navigate_up()
        self.assertEqual(self.game.selected_item_index, 1)  # Second item
        
        # Navigate up again should go back to third item (newest)
        self.game.navigate_up()
        self.assertEqual(self.game.selected_item_index, 2)  # Third item
    
    def test_inventory_opens_with_newest_selected(self):
        """Test that opening inventory starts with newest item selected."""
        # Add items
        item1 = HealthPotion(0, 0)
        item1.name = "First Potion"
        item2 = HealthPotion(0, 0)
        item2.name = "Second Potion"
        
        self.game.player.inventory.append(item1)
        self.game.player.inventory.append(item2)
        
        # Simulate opening inventory
        self.game.game_state = 'PLAYING'
        import tcod.event
        key_event = tcod.event.KeyDown(sym=ord('i'), mod=0, scancode=0)
        self.game.handle_keydown(key_event)
        
        # Should start with newest item selected
        self.assertEqual(self.game.game_state, 'INVENTORY')
        self.assertEqual(self.game.selection_mode, "inventory")
        self.assertEqual(self.game.selected_item_index, 1)  # Second item (newest)
    
    def test_selection_highlighting_works_with_reverse_order(self):
        """Test that selection highlighting works correctly with reverse display."""
        # Add items
        item1 = HealthPotion(0, 0)
        item1.name = "First Potion"
        item2 = HealthPotion(0, 0)
        item2.name = "Second Potion"
        
        self.game.player.inventory.append(item1)
        self.game.player.inventory.append(item2)
        
        # Create mock console
        console = MagicMock()
        console.print = MagicMock()
        
        # Render with newest item selected (index 1)
        self.game.ui.render_inventory(console, self.game.player, selected_item_index=1)
        
        # Check that newest item (displayed first) is highlighted
        calls = console.print.call_args_list
        newest_highlighted = False
        oldest_not_highlighted = False
        
        for call in calls:
            args = call[0]
            kwargs = call[1] if len(call) > 1 else {}
            if len(args) >= 3:
                text = str(args[2])
                color = kwargs.get('fg')
                
                if "a) [C] Second Potion" in text:  # Newest item with 'a'
                    from constants import COLOR_GREEN
                    if color == COLOR_GREEN:
                        newest_highlighted = True
                elif "b) [C] First Potion" in text:  # Oldest item with 'b'
                    from constants import COLOR_WHITE
                    if color == COLOR_WHITE:
                        oldest_not_highlighted = True
        
        self.assertTrue(newest_highlighted, "Newest item should be highlighted when selected")
        self.assertTrue(oldest_not_highlighted, "Oldest item should not be highlighted")


if __name__ == '__main__':
    unittest.main()