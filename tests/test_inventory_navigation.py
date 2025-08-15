"""Test the new inventory navigation features with equipment selection."""

import unittest
from unittest.mock import MagicMock
from src.game import Game
from src.player import Player
from src.items.weapons import Sword
from src.items.armor import LeatherArmor
from src.items.accessories import RingOfPrecision
from src.items.consumables import HealthPotion
from src.ui import UI


class TestInventoryNavigation(unittest.TestCase):
    """Test the enhanced inventory navigation system."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = Game()
        self.game.player = Player(5, 5)
        self.game.ui = UI()
        self.game.player.xp = 100  # Give enough XP for equipment
        
    def test_navigation_between_inventory_and_equipment(self):
        """Test navigation between inventory items and equipped items."""
        # Add an item to inventory
        potion = HealthPotion(0, 0)
        self.game.player.inventory.append(potion)
        
        # Equip a weapon
        weapon = Sword(0, 0)
        self.game.player.weapon = weapon
        
        # Open inventory - should start in inventory mode
        self.game.game_state = 'INVENTORY'
        self.game.selected_item_index = 0
        self.game.selection_mode = "inventory"
        self.game.selected_equipment_index = None
        
        # Test navigation down from inventory to equipment
        self.game.navigate_down()  # Should move to equipment section
        self.assertEqual(self.game.selection_mode, "equipment")
        self.assertEqual(self.game.selected_equipment_index, 0)  # Weapon
        self.assertIsNone(self.game.selected_item_index)
        
        # Test navigation up from equipment back to inventory
        self.game.navigate_up()  # Should move back to inventory
        self.assertEqual(self.game.selection_mode, "inventory")
        self.assertEqual(self.game.selected_item_index, 0)  # Last inventory item
        self.assertIsNone(self.game.selected_equipment_index)
    
    def test_equipment_selection_cycling(self):
        """Test cycling through equipment slots."""
        # Equip items in all slots
        weapon = Sword(0, 0)
        armor = LeatherArmor(0, 0)
        accessory = RingOfPrecision(0, 0)
        
        self.game.player.weapon = weapon
        self.game.player.armor = armor
        self.game.player.accessories[0] = accessory
        
        # Start in equipment mode
        self.game.selection_mode = "equipment"
        self.game.selected_equipment_index = 0  # Weapon
        
        # Navigate through equipment
        self.game.navigate_down()
        self.assertEqual(self.game.selected_equipment_index, 1)  # Armor
        
        self.game.navigate_down()
        self.assertEqual(self.game.selected_equipment_index, 2)  # Accessory 1
        
        self.game.navigate_down()
        self.assertEqual(self.game.selected_equipment_index, 3)  # Accessory 2 (empty)
        
        self.game.navigate_down()
        self.assertEqual(self.game.selected_equipment_index, 4)  # Accessory 3 (empty)
    
    def test_get_selected_equipment_item(self):
        """Test getting the currently selected equipment item."""
        # Equip items
        weapon = Sword(0, 0)
        armor = LeatherArmor(0, 0)
        accessory = RingOfPrecision(0, 0)
        
        self.game.player.weapon = weapon
        self.game.player.armor = armor
        self.game.player.accessories[0] = accessory
        
        # Test weapon selection
        self.game.selected_equipment_index = 0
        self.assertEqual(self.game.get_selected_equipment_item(), weapon)
        
        # Test armor selection
        self.game.selected_equipment_index = 1
        self.assertEqual(self.game.get_selected_equipment_item(), armor)
        
        # Test accessory selection
        self.game.selected_equipment_index = 2
        self.assertEqual(self.game.get_selected_equipment_item(), accessory)
        
        # Test empty accessory slot
        self.game.selected_equipment_index = 3
        self.assertIsNone(self.game.get_selected_equipment_item())
    
    def test_unequip_functionality(self):
        """Test the unequip functionality."""
        # Equip a weapon
        weapon = Sword(0, 0)
        weapon.name = "Test Sword"
        self.game.player.weapon = weapon
        
        # Select the weapon in equipment mode
        self.game.selection_mode = "equipment"
        self.game.selected_equipment_index = 0
        
        # Test unequipping
        initial_inventory_size = len(self.game.player.inventory)
        self.game.unequip_selected_item()
        
        # Verify weapon was unequipped and added to inventory
        self.assertIsNone(self.game.player.weapon)
        self.assertEqual(len(self.game.player.inventory), initial_inventory_size + 1)
        self.assertIn(weapon, self.game.player.inventory)
    
    def test_unequip_with_full_inventory(self):
        """Test unequipping when inventory is full."""
        # Fill inventory to capacity
        for i in range(self.game.player.inventory_size):
            potion = HealthPotion(0, 0)
            self.game.player.inventory.append(potion)
        
        # Equip a weapon
        weapon = Sword(0, 0)
        self.game.player.weapon = weapon
        
        # Select the weapon
        self.game.selection_mode = "equipment"
        self.game.selected_equipment_index = 0
        
        # Try to unequip - should fail due to full inventory
        self.game.unequip_selected_item()
        
        # Verify weapon is still equipped
        self.assertEqual(self.game.player.weapon, weapon)
        self.assertNotIn(weapon, self.game.player.inventory)
    
    def test_unequip_empty_slot(self):
        """Test trying to unequip from an empty slot."""
        # Ensure weapon slot is empty
        self.game.player.weapon = None
        
        # Select the empty weapon slot
        self.game.selection_mode = "equipment"
        self.game.selected_equipment_index = 0
        
        # Try to unequip - should do nothing
        initial_inventory_size = len(self.game.player.inventory)
        self.game.unequip_selected_item()
        
        # Verify nothing changed
        self.assertIsNone(self.game.player.weapon)
        self.assertEqual(len(self.game.player.inventory), initial_inventory_size)
    
    def test_ui_rendering_with_equipment_selection(self):
        """Test that UI renders equipment selection correctly."""
        # Equip a weapon
        weapon = Sword(0, 0)
        weapon.name = "Test Sword"
        self.game.player.weapon = weapon
        
        # Create mock console
        console = MagicMock()
        console.print = MagicMock()
        
        # Test rendering with weapon selected
        self.game.ui.render_inventory(
            console, self.game.player, 
            selected_item_index=None,
            selected_equipment_index=0,
            selection_mode="equipment"
        )
        
        # Verify that weapon was highlighted (called with COLOR_GREEN)
        calls = console.print.call_args_list
        weapon_highlighted = False
        
        for call in calls:
            args = call[0]
            kwargs = call[1] if len(call) > 1 else {}
            if len(args) >= 3:
                text = str(args[2])
                color = kwargs.get('fg')
                if "Weapon:" in text and "Test Sword" in text:
                    from constants import COLOR_GREEN
                    if color == COLOR_GREEN:
                        weapon_highlighted = True
        
        self.assertTrue(weapon_highlighted, "Selected weapon should be highlighted")


if __name__ == '__main__':
    unittest.main()