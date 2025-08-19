"""Test that boon selection UI properly displays instructions."""

import unittest
from unittest.mock import Mock, MagicMock
from src.ui import UI
from src.player import Player
from src.items.consumables.fire_boon import FireBoon
from src.items.weapons.sword import Sword
from src.items.armor.leather_armor import LeatherArmor
from constants import SCREEN_HEIGHT, COLOR_GREEN, COLOR_WHITE, COLOR_YELLOW


class TestBoonUIVisibility(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.ui = UI()
        self.player = Player(5, 5)
        self.console = Mock()
        self.console.clear = Mock()
        self.console.print = Mock()
        
        # Equip weapon and armor for testing
        self.player.weapon = Sword(0, 0)
        self.player.armor = LeatherArmor(0, 0)
        
        # Create a boon for testing
        self.boon = FireBoon(0, 0)
        
    def test_boon_choice_instructions_displayed(self):
        """Test that BOON_CHOICE state displays proper instructions."""
        # Render inventory in BOON_CHOICE state
        self.ui.render_inventory(
            self.console, 
            self.player,
            selected_item_index=None,
            selected_equipment_index=None,
            selection_mode="inventory",
            game_state="BOON_CHOICE",
            pending_boon=self.boon
        )
        
        # Check that the proper instructions were printed
        calls = self.console.print.call_args_list
        
        # Extract the text from all print calls
        printed_texts = []
        for call in calls:
            # Handle both positional and keyword arguments
            if len(call[0]) >= 3:
                printed_texts.append(call[0][2])
            elif 'text' in call[1]:
                printed_texts.append(call[1]['text'])
        
        # Check for boon choice specific instructions
        expected_messages = [
            f"Choose enchantment target for {self.boon.name}:",
            f"[W] Apply to Weapon: {self.player.weapon.name}",
            f"[A] Apply to Armor: {self.player.armor.name}",
            "Press W for weapon, A for armor, or ESC to cancel"
        ]
        
        for expected in expected_messages:
            self.assertIn(expected, printed_texts, 
                         f"Expected message '{expected}' not found in UI output")
        
        # Verify these messages appear at the bottom of the screen
        bottom_calls = [call for call in calls if call[0][1] >= SCREEN_HEIGHT - 5]
        self.assertTrue(len(bottom_calls) >= 4, 
                       "Expected at least 4 lines of instructions at bottom of screen")
        
    def test_normal_inventory_instructions_displayed(self):
        """Test that normal INVENTORY state displays regular instructions."""
        # Render inventory in normal INVENTORY state
        self.ui.render_inventory(
            self.console,
            self.player,
            selected_item_index=None,
            selected_equipment_index=None,
            selection_mode="inventory",
            game_state="INVENTORY"
        )
        
        # Check that normal inventory instructions were printed
        calls = self.console.print.call_args_list
        printed_texts = []
        for call in calls:
            if len(call[0]) >= 3:
                printed_texts.append(call[0][2])
        
        # Check for normal inventory instructions
        expected_messages = [
            "Controls:",
            "Arrow keys: Navigate  Letter: Select inventory item",
            "[Enter] Use/Equip  [D] Drop  [U] Unequip selected",
            "1-5: Select equipment slots",
            "Press ESC to close inventory"
        ]
        
        for expected in expected_messages:
            self.assertIn(expected, printed_texts,
                         f"Expected normal instruction '{expected}' not found")
        
        # Verify boon-specific messages are NOT shown
        self.assertNotIn("Choose enchantment target", " ".join(printed_texts))
        self.assertNotIn("[W] Apply to Weapon", " ".join(printed_texts))
        self.assertNotIn("[A] Apply to Armor", " ".join(printed_texts))


if __name__ == '__main__':
    unittest.main()