"""Test for equipment swap bug where weapons disappear when inventory is full."""

import unittest
from unittest.mock import MagicMock
from src.game import Game
from src.player import Player
from src.items.weapons import Sword, Dagger
from src.items.armor import LeatherArmor, PlateArmor
from src.items.consumables import HealthPotion
from src.ui import UI


class TestEquipmentSwapBug(unittest.TestCase):
    """Test that equipment doesn't disappear when swapping with full inventory."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = Game()
        self.game.player = Player(5, 5)
        self.game.ui = UI()
        
    def test_weapon_swap_with_full_inventory(self):
        """Test weapon swap when inventory is full doesn't lose the old weapon."""
        # Give player enough XP
        self.game.player.xp = 100
        
        # Fill the inventory to max capacity
        for i in range(self.game.player.inventory_size):
            potion = HealthPotion(0, 0)
            potion.name = f"Potion {i}"
            self.game.player.inventory.append(potion)
        
        # Equip initial weapon
        initial_weapon = Sword(0, 0)
        initial_weapon.name = "Initial Sword"
        self.game.player.weapon = initial_weapon
        
        # Try to equip new weapon (should fail due to full inventory)
        new_weapon = Dagger(0, 0)
        new_weapon.name = "New Dagger"
        self.game.player.inventory.append(new_weapon)  # This would overflow, but we're testing the swap
        self.game.player.inventory.pop()  # Remove it to fit max capacity
        self.game.player.inventory.append(new_weapon)  # Add back to test
        
        # Equipment should fail and old weapon should remain equipped
        self.game.equip_item(new_weapon)
        
        # Verify the original weapon is still equipped
        self.assertEqual(self.game.player.weapon, initial_weapon)
        self.assertEqual(self.game.player.weapon.name, "Initial Sword")
        
        # Verify the new weapon is still in inventory
        self.assertIn(new_weapon, self.game.player.inventory)
    
    def test_weapon_swap_with_space_works(self):
        """Test weapon swap when inventory has space works correctly."""
        # Give player enough XP
        self.game.player.xp = 100
        
        # Don't fill inventory completely - leave one space
        for i in range(self.game.player.inventory_size - 2):
            potion = HealthPotion(0, 0)
            potion.name = f"Potion {i}"
            self.game.player.inventory.append(potion)
        
        # Equip initial weapon
        initial_weapon = Sword(0, 0)
        initial_weapon.name = "Initial Sword"
        self.game.player.weapon = initial_weapon
        
        # Add new weapon to inventory
        new_weapon = Dagger(0, 0)
        new_weapon.name = "New Dagger"
        self.game.player.inventory.append(new_weapon)
        
        # Equipment should succeed
        self.game.equip_item(new_weapon)
        
        # Verify the new weapon is equipped
        self.assertEqual(self.game.player.weapon, new_weapon)
        self.assertEqual(self.game.player.weapon.name, "New Dagger")
        
        # Verify the old weapon is back in inventory
        self.assertIn(initial_weapon, self.game.player.inventory)
        
        # Verify the new weapon is no longer in inventory
        self.assertNotIn(new_weapon, self.game.player.inventory)
    
    def test_armor_swap_with_full_inventory(self):
        """Test armor swap when inventory is full doesn't lose the old armor."""
        # Give player enough XP
        self.game.player.xp = 100
        
        # Fill the inventory to max capacity
        for i in range(self.game.player.inventory_size):
            potion = HealthPotion(0, 0)
            potion.name = f"Potion {i}"
            self.game.player.inventory.append(potion)
        
        # Equip initial armor
        initial_armor = LeatherArmor(0, 0)
        initial_armor.name = "Initial Leather"
        self.game.player.armor = initial_armor
        
        # Try to equip new armor (should fail due to full inventory)
        new_armor = PlateArmor(0, 0)
        new_armor.name = "New Plate"
        self.game.player.inventory.append(new_armor)  # This would overflow, but we're testing
        self.game.player.inventory.pop()  # Remove to fit max capacity
        self.game.player.inventory.append(new_armor)  # Add back to test
        
        # Equipment should fail and old armor should remain equipped
        self.game.equip_item(new_armor)
        
        # Verify the original armor is still equipped
        self.assertEqual(self.game.player.armor, initial_armor)
        self.assertEqual(self.game.player.armor.name, "Initial Leather")
        
        # Verify the new armor is still in inventory
        self.assertIn(new_armor, self.game.player.inventory)
    
    def test_no_current_equipment_swap_works(self):
        """Test equipping when no current equipment works normally."""
        # Store the starting weapon first
        starting_weapon = self.game.player.weapon
        
        # Clear inventory and put starting weapon there
        self.game.player.inventory.clear()
        self.game.player.inventory.append(starting_weapon)
        
        # Ensure no weapon equipped
        self.game.player.weapon = None
        
        # Give player enough XP to equip weapon
        self.game.player.xp = 100
        
        # Add weapon to inventory
        weapon = Sword(0, 0)
        weapon.name = "Test Sword"
        self.game.player.inventory.append(weapon)
        
        # Equipment should succeed
        self.game.equip_item(weapon)
        
        # Verify the weapon is equipped
        self.assertEqual(self.game.player.weapon, weapon)
        self.assertEqual(self.game.player.weapon.name, "Test Sword")
        
        # Verify the weapon is no longer in inventory
        self.assertNotIn(weapon, self.game.player.inventory)


if __name__ == '__main__':
    unittest.main()