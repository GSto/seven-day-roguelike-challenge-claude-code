"""Test the new numbered equipment slot system."""

import unittest
from unittest.mock import MagicMock
from src.game import Game
from src.player import Player
from src.items.weapons import Sword
from src.items.armor import LeatherArmor
from src.items.accessories import RingOfPrecision
from src.ui import UI


class TestInventorySlotSystem(unittest.TestCase):
    """Test the new numbered equipment slot system."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = Game()
        self.game.player = Player(5, 5)
        self.game.ui = UI()
        self.game.player.xp = 100  # Give enough XP for equipment
        
    def test_equipment_slot_selection(self):
        """Test that number keys 1-5 select the correct equipment slots."""
        # Start in inventory mode
        self.game.selection_mode = "inventory"
        self.game.selected_item_index = 0
        self.game.selected_equipment_index = None
        
        # Test slot 1 (weapon)
        self.game.select_equipment_slot(0)  # Key '1' maps to index 0
        self.assertEqual(self.game.selection_mode, "equipment")
        self.assertEqual(self.game.selected_equipment_index, 0)
        self.assertIsNone(self.game.selected_item_index)
        
        # Test slot 2 (armor)
        self.game.select_equipment_slot(1)  # Key '2' maps to index 1
        self.assertEqual(self.game.selected_equipment_index, 1)
        
        # Test slot 3 (accessory 1)
        self.game.select_equipment_slot(2)  # Key '3' maps to index 2
        self.assertEqual(self.game.selected_equipment_index, 2)
        
        # Test slot 4 (accessory 2)
        self.game.select_equipment_slot(3)  # Key '4' maps to index 3
        self.assertEqual(self.game.selected_equipment_index, 3)
        
        # Test slot 5 (accessory 3)
        self.game.select_equipment_slot(4)  # Key '5' maps to index 4
        self.assertEqual(self.game.selected_equipment_index, 4)
    
    def test_ui_displays_numbered_slots(self):
        """Test that UI displays equipment with correct slot numbers."""
        # Equip some items
        weapon = Sword(0, 0)
        weapon.name = "Test Sword"
        armor = LeatherArmor(0, 0)
        armor.name = "Test Armor"
        accessory = RingOfPrecision(0, 0)
        
        self.game.player.weapon = weapon
        self.game.player.armor = armor
        self.game.player.accessories[0] = accessory
        
        # Create mock console
        console = MagicMock()
        console.print = MagicMock()
        
        # Render inventory
        self.game.ui.render_inventory(
            console, self.game.player,
            selected_item_index=None,
            selected_equipment_index=None,
            selection_mode="inventory"
        )
        
        # Check that slots are numbered correctly
        calls = console.print.call_args_list
        
        slot_1_found = False  # Weapon
        slot_2_found = False  # Armor
        slot_3_found = False  # Accessory 1
        slot_4_found = False  # Empty accessory 2
        slot_5_found = False  # Empty accessory 3
        
        for call in calls:
            args = call[0]
            if len(args) >= 3:
                text = str(args[2])
                if "1) Weapon:" in text and "Test Sword" in text:
                    slot_1_found = True
                elif "2) Armor:" in text and "Test Armor" in text:
                    slot_2_found = True
                elif "3) Accessory:" in text and "Ring of Precision" in text:
                    slot_3_found = True
                elif "4) Accessory: Empty" in text:
                    slot_4_found = True
                elif "5) Accessory: Empty" in text:
                    slot_5_found = True
        
        self.assertTrue(slot_1_found, "Slot 1 (weapon) should be displayed")
        self.assertTrue(slot_2_found, "Slot 2 (armor) should be displayed")
        self.assertTrue(slot_3_found, "Slot 3 (accessory) should be displayed")
        self.assertTrue(slot_4_found, "Slot 4 (empty accessory) should be displayed")
        self.assertTrue(slot_5_found, "Slot 5 (empty accessory) should be displayed")
    
    def test_empty_weapon_and_armor_display(self):
        """Test that empty weapon/armor slots show 'Empty'."""
        # Ensure weapon and armor are not equipped
        self.game.player.weapon = None
        self.game.player.armor = None
        
        # Create mock console
        console = MagicMock()
        console.print = MagicMock()
        
        # Render inventory
        self.game.ui.render_inventory(
            console, self.game.player,
            selected_item_index=None,
            selected_equipment_index=None,
            selection_mode="inventory"
        )
        
        # Check for empty slots
        calls = console.print.call_args_list
        
        empty_weapon_found = False
        empty_armor_found = False
        
        for call in calls:
            args = call[0]
            if len(args) >= 3:
                text = str(args[2])
                if "1) Weapon: Empty" in text:
                    empty_weapon_found = True
                elif "2) Armor: Empty" in text:
                    empty_armor_found = True
        
        self.assertTrue(empty_weapon_found, "Empty weapon slot should display 'Empty'")
        self.assertTrue(empty_armor_found, "Empty armor slot should display 'Empty'")
    
    def test_equipment_slot_highlighting(self):
        """Test that selected equipment slots are highlighted."""
        # Equip a weapon
        weapon = Sword(0, 0)
        weapon.name = "Test Sword"
        self.game.player.weapon = weapon
        
        # Create mock console
        console = MagicMock()
        console.print = MagicMock()
        
        # Render with weapon slot selected (index 0)
        self.game.ui.render_inventory(
            console, self.game.player,
            selected_item_index=None,
            selected_equipment_index=0,
            selection_mode="equipment"
        )
        
        # Check that weapon slot was highlighted with COLOR_GREEN
        calls = console.print.call_args_list
        weapon_highlighted = False
        
        for call in calls:
            args = call[0]
            kwargs = call[1] if len(call) > 1 else {}
            if len(args) >= 3:
                text = str(args[2])
                color = kwargs.get('fg')
                if "1) Weapon:" in text and "Test Sword" in text:
                    from constants import COLOR_GREEN
                    if color == COLOR_GREEN:
                        weapon_highlighted = True
        
        self.assertTrue(weapon_highlighted, "Selected weapon slot should be highlighted")
    
    def test_unequip_selected_equipment(self):
        """Test that 'U' key unequips the currently selected equipment."""
        # Equip a weapon
        weapon = Sword(0, 0)
        weapon.name = "Test Sword"
        self.game.player.weapon = weapon
        
        # Select the weapon slot and switch to equipment mode
        self.game.selection_mode = "equipment"
        self.game.selected_equipment_index = 0
        
        # Test unequipping
        initial_inventory_size = len(self.game.player.inventory)
        self.game.unequip_selected_item()
        
        # Verify weapon was unequipped and added to inventory
        self.assertIsNone(self.game.player.weapon)
        self.assertEqual(len(self.game.player.inventory), initial_inventory_size + 1)
        self.assertIn(weapon, self.game.player.inventory)
    
    def test_slot_index_mapping(self):
        """Test that slot indices map correctly to equipment positions."""
        # Test the mapping used by select_equipment_slot
        test_cases = [
            (0, "weapon slot"),      # Slot 1 -> equipment index 0
            (1, "armor slot"),       # Slot 2 -> equipment index 1
            (2, "accessory 1 slot"), # Slot 3 -> equipment index 2
            (3, "accessory 2 slot"), # Slot 4 -> equipment index 3
            (4, "accessory 3 slot"), # Slot 5 -> equipment index 4
        ]
        
        for slot_index, description in test_cases:
            with self.subTest(slot_index=slot_index, description=description):
                self.game.select_equipment_slot(slot_index)
                self.assertEqual(self.game.selected_equipment_index, slot_index)


if __name__ == '__main__':
    unittest.main()