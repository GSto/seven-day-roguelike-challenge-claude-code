"""
Unit tests for the shop system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from shop import Shop
from shop_manager import ShopManager
from player import Player
from items.consumables.health_potion import HealthPotion
from items.weapons.sword import Sword
from items.armor.leather_armor import LeatherArmor
from level.level import Level


class TestShopSystem(unittest.TestCase):
    """Test the shop system functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.player = Player(5, 5)
        self.player.xp = 100  # Give player some XP to spend
        self.shop = Shop(floor_level=3)
        self.shop_manager = ShopManager()
    
    def test_market_values(self):
        """Test that items have proper market values."""
        # Test consumable
        potion = HealthPotion(0, 0)
        self.assertEqual(potion.market_value, 10)
        
        # Test weapon
        sword = Sword(0, 0)
        self.assertEqual(sword.market_value, 25)
        
        # Test armor
        armor = LeatherArmor(0, 0)
        self.assertEqual(armor.market_value, 25)
    
    def test_shop_generation(self):
        """Test that shop generates appropriate inventory."""
        shop = Shop(floor_level=5)
        
        # Check that inventory was generated
        self.assertGreater(len(shop.inventory), 0)
        
        # Check for guaranteed health potion
        has_health_potion = any(
            isinstance(item, HealthPotion) for item in shop.inventory if item
        )
        self.assertTrue(has_health_potion, "Shop should have at least one health potion")
        
        # Check that shop has a mix of item types
        item_types = set()
        for item in shop.inventory:
            if item:
                if hasattr(item, 'equipment_slot'):
                    item_types.add(item.equipment_slot)
                elif hasattr(item, 'use'):
                    item_types.add('consumable')
        
        self.assertGreater(len(item_types), 1, "Shop should have multiple item types")
    
    def test_no_duplicate_items_in_shop(self):
        """Test that shop doesn't contain duplicate item types."""
        shop = Shop(floor_level=5)
        
        item_types = []
        for item in shop.inventory:
            if item:
                item_type = type(item).__name__
                self.assertNotIn(item_type, item_types, f"Duplicate {item_type} found in shop")
                item_types.append(item_type)
    
    def test_buy_item_success(self):
        """Test successful item purchase."""
        # Add a specific item to shop
        potion = HealthPotion(0, 0)
        self.shop.inventory[0] = potion
        
        # Player has 100 XP, potion costs 10
        initial_xp = self.player.xp
        initial_inv_size = len(self.player.inventory)
        
        success, message = self.shop.buy_item(0, self.player)
        
        self.assertTrue(success)
        self.assertEqual(self.player.xp, initial_xp - 10)
        self.assertEqual(len(self.player.inventory), initial_inv_size + 1)
        self.assertIsNone(self.shop.inventory[0])  # Item removed from shop
        self.assertIn("Purchased", message)
    
    def test_buy_item_insufficient_xp(self):
        """Test buying with insufficient XP."""
        # Give player only 5 XP
        self.player.xp = 5
        
        # Add item that costs 10 XP
        potion = HealthPotion(0, 0)
        self.shop.inventory[0] = potion
        
        success, message = self.shop.buy_item(0, self.player)
        
        self.assertFalse(success)
        self.assertEqual(self.player.xp, 5)  # XP unchanged
        self.assertIsNotNone(self.shop.inventory[0])  # Item still in shop
        self.assertIn("Not enough XP", message)
    
    def test_buy_item_inventory_full(self):
        """Test buying when inventory is full."""
        # Fill player inventory
        for _ in range(self.player.inventory_size):
            self.player.inventory.append(HealthPotion(0, 0))
        
        potion = HealthPotion(0, 0)
        self.shop.inventory[0] = potion
        
        success, message = self.shop.buy_item(0, self.player)
        
        self.assertFalse(success)
        self.assertIn("inventory is full", message)
    
    def test_sell_item_success(self):
        """Test successful item sale."""
        # Give player an item to sell
        sword = Sword(0, 0)
        self.player.inventory.append(sword)
        
        initial_xp = self.player.xp
        
        success, message = self.shop.sell_item(sword, self.player)
        
        self.assertTrue(success)
        # Sell price is 50% of market value (25 // 2 = 12)
        self.assertEqual(self.player.xp, initial_xp + 12)
        self.assertNotIn(sword, self.player.inventory)
        self.assertIn("Sold", message)
    
    def test_sell_price_calculation(self):
        """Test that sell price is 50% of market value."""
        sword = Sword(0, 0)
        sell_price = self.shop.get_sell_price(sword)
        self.assertEqual(sell_price, sword.market_value // 2)
        
        potion = HealthPotion(0, 0)
        sell_price = self.shop.get_sell_price(potion)
        self.assertEqual(sell_price, potion.market_value // 2)
    
    def test_shop_manager_open_close(self):
        """Test shop manager opening and closing."""
        self.shop_manager.open_shop(self.shop, self.player)
        
        self.assertTrue(self.shop_manager.is_open)
        self.assertEqual(self.shop_manager.current_shop, self.shop)
        self.assertEqual(self.shop_manager.player, self.player)
        self.assertEqual(self.shop_manager.ui_mode, 'buy')
        
        self.shop_manager.close_shop()
        
        self.assertFalse(self.shop_manager.is_open)
        self.assertIsNone(self.shop_manager.current_shop)
        self.assertIsNone(self.shop_manager.player)
    
    def test_shop_manager_mode_switching(self):
        """Test switching between buy and sell modes."""
        self.shop_manager.open_shop(self.shop, self.player)
        
        self.assertEqual(self.shop_manager.ui_mode, 'buy')
        
        self.shop_manager.toggle_mode()
        self.assertEqual(self.shop_manager.ui_mode, 'sell')
        
        self.shop_manager.toggle_mode()
        self.assertEqual(self.shop_manager.ui_mode, 'buy')
    
    def test_shop_placement_in_level(self):
        """Test that shops are placed correctly in levels."""
        # Test floor 1-9 should have shops
        for floor in range(1, 10):
            level = Level(level_number=floor)
            self.assertIsNotNone(level.shop, f"Floor {floor} should have a shop")
            self.assertIsNotNone(level.shop.x, "Shop should have x coordinate")
            self.assertIsNotNone(level.shop.y, "Shop should have y coordinate")
        
        # Test floor 10 should NOT have a shop
        level10 = Level(level_number=10)
        self.assertIsNone(level10.shop, "Floor 10 should not have a shop")
    
    def test_shop_symbol_rendering(self):
        """Test that shop has correct symbol and color."""
        shop = Shop(floor_level=5)
        self.assertEqual(shop.symbol, '$')
        self.assertEqual(shop.color, (255, 215, 0))  # Gold color


if __name__ == '__main__':
    unittest.main()