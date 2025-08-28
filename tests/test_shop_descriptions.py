"""
Unit tests for shop item description display.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from shop import Shop
from shop_manager import ShopManager
from player import Player
from items.weapons.sword import Sword
from items.consumables.health_potion import HealthPotion
from items.armor.leather_armor import LeatherArmor


class TestShopDescriptions(unittest.TestCase):
    """Test the shop description display functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.player = Player(5, 5)
        self.player.xp = 100
        self.shop = Shop(floor_level=3)
        self.shop_manager = ShopManager()
        self.shop_manager.open_shop(self.shop, self.player)
    
    def test_get_selected_item_in_buy_mode(self):
        """Test getting selected item in buy mode."""
        # Set to buy mode
        self.shop_manager.ui_mode = 'buy'
        self.shop_manager.selected_index = 0
        
        # Add a specific item to shop for testing
        test_sword = Sword(0, 0)
        self.shop.inventory[0] = test_sword
        
        selected_item = self.shop_manager.get_selected_item()
        self.assertIsNotNone(selected_item)
        self.assertEqual(selected_item.name, test_sword.name)
    
    def test_get_selected_item_in_sell_mode(self):
        """Test getting selected item in sell mode."""
        # Add item to player inventory
        test_item = HealthPotion(0, 0)
        self.player.inventory.append(test_item)
        
        # Set to sell mode
        self.shop_manager.ui_mode = 'sell'
        self.shop_manager.selected_index = 0
        
        selected_item = self.shop_manager.get_selected_item()
        self.assertIsNotNone(selected_item)
        self.assertEqual(selected_item.name, test_item.name)
    
    def test_get_selected_item_invalid_index(self):
        """Test getting selected item with invalid index."""
        # Set invalid index
        self.shop_manager.selected_index = 999
        
        selected_item = self.shop_manager.get_selected_item()
        self.assertIsNone(selected_item)
    
    def test_get_selected_item_empty_inventory(self):
        """Test getting selected item when no items available."""
        # Clear shop inventory
        self.shop.inventory = [None] * 15
        
        # Set to buy mode
        self.shop_manager.ui_mode = 'buy'
        self.shop_manager.selected_index = 0
        
        selected_item = self.shop_manager.get_selected_item()
        self.assertIsNone(selected_item)
    
    def test_item_descriptions_exist(self):
        """Test that items have descriptions."""
        # Test various item types have descriptions
        sword = Sword(0, 0)
        health_potion = HealthPotion(0, 0)
        armor = LeatherArmor(0, 0)
        
        self.assertIsNotNone(sword.description)
        self.assertIsNotNone(health_potion.description)
        self.assertIsNotNone(armor.description)
        
        # Descriptions should be non-empty strings
        self.assertTrue(isinstance(sword.description, str))
        self.assertTrue(len(sword.description.strip()) > 0)
    
    def test_description_word_wrapping(self):
        """Test that long descriptions are properly handled."""
        # Create an item with a very long description
        test_item = Sword(0, 0)
        original_desc = test_item.description
        
        # Set a very long description
        long_description = "This is a very long description that should definitely wrap across multiple lines when displayed in the shop interface because it exceeds the maximum width."
        test_item.description = long_description
        
        # Add to shop and select
        self.shop.inventory[0] = test_item
        self.shop_manager.ui_mode = 'buy'
        self.shop_manager.selected_index = 0
        
        selected_item = self.shop_manager.get_selected_item()
        self.assertIsNotNone(selected_item)
        self.assertEqual(selected_item.description, long_description)
        
        # Restore original description
        test_item.description = original_desc
    
    def test_shop_manager_selection_bounds(self):
        """Test that selection stays within valid bounds."""
        # Add a few items to shop
        for i in range(3):
            self.shop.inventory[i] = HealthPotion(0, 0)
        
        self.shop_manager.ui_mode = 'buy'
        self.shop_manager.selected_index = 0
        
        # Test moving selection up and down
        self.shop_manager.move_selection(1)  # Should go to index 1
        selected_item = self.shop_manager.get_selected_item()
        self.assertIsNotNone(selected_item)
        
        self.shop_manager.move_selection(1)  # Should go to index 2  
        selected_item = self.shop_manager.get_selected_item()
        self.assertIsNotNone(selected_item)
        
        self.shop_manager.move_selection(1)  # Should stay at index 2 (max)
        selected_item = self.shop_manager.get_selected_item()
        self.assertIsNotNone(selected_item)
        
        self.shop_manager.move_selection(-1)  # Should go to index 1
        selected_item = self.shop_manager.get_selected_item()
        self.assertIsNotNone(selected_item)


if __name__ == '__main__':
    unittest.main()