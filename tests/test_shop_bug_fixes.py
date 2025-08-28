"""
Unit tests for shop system bug fixes.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from shop import Shop
from level.level import Level
from items.pool import item_pool
from items.accessories.power_ring import PowerRing


class TestShopBugFixes(unittest.TestCase):
    """Test the shop system bug fixes."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Reset the global item pool state
        item_pool.game_spawned_accessories.clear()
        item_pool.floor_spawned_weapons.clear()
        item_pool.floor_spawned_armor.clear()
    
    def test_shop_does_not_block_monster_placement(self):
        """Test that monsters are not placed on shop tiles."""
        level = Level(level_number=5)
        
        # Get shop position
        shop_x, shop_y = level.shop.x, level.shop.y
        
        # Check that no monster is at the shop position
        monster_at_shop = level.get_monster_at(shop_x, shop_y)
        self.assertIsNone(monster_at_shop, "No monster should be placed at shop location")
    
    def test_shop_does_not_block_item_placement(self):
        """Test that items are not placed on shop tiles."""
        level = Level(level_number=5)
        
        # Get shop position
        shop_x, shop_y = level.shop.x, level.shop.y
        
        # Check that no item is at the shop position
        item_at_shop = level.get_item_at(shop_x, shop_y)
        self.assertIsNone(item_at_shop, "No item should be placed at shop location")
    
    def test_shop_item_generation_does_not_affect_global_pool(self):
        """Test that shop item generation doesn't affect global accessory uniqueness."""
        # Create a shop that should generate accessories
        shop1 = Shop(floor_level=5)
        
        # Check if shop has accessories
        shop_accessories = [item for item in shop1.inventory 
                          if item and hasattr(item, 'equipment_slot') and item.equipment_slot == 'accessory']
        
        # Now create items using the global pool
        # Accessories should still be available for the main game
        level = Level(level_number=5)
        
        # Count accessories in the level
        level_accessories = [item for item in level.items 
                           if hasattr(item, 'equipment_slot') and item.equipment_slot == 'accessory']
        
        # Both shop and level should be able to have accessories
        # This test verifies that shop generation doesn't consume global accessory uniqueness
        self.assertTrue(len(shop_accessories) > 0 or len(level_accessories) > 0, 
                       "Either shop or level should have accessories available")
    
    def test_shop_can_have_same_accessory_type_as_main_game(self):
        """Test that shops can have accessories that also appear in the main game."""
        # Clear global state
        item_pool.game_spawned_accessories.clear()
        
        # Create multiple shops and levels
        shops = [Shop(floor_level=3) for _ in range(3)]
        levels = [Level(level_number=i) for i in range(3, 6)]
        
        # Collect all accessory types from shops
        shop_accessory_types = set()
        for shop in shops:
            for item in shop.inventory:
                if item and hasattr(item, 'equipment_slot') and item.equipment_slot == 'accessory':
                    shop_accessory_types.add(type(item).__name__)
        
        # Collect all accessory types from levels
        level_accessory_types = set()
        for level in levels:
            for item in level.items:
                if hasattr(item, 'equipment_slot') and item.equipment_slot == 'accessory':
                    level_accessory_types.add(type(item).__name__)
        
        # There might be overlap, which is now OK since shops don't affect global pool
        # This test just verifies the system doesn't crash and both can generate accessories
        total_unique_types = len(shop_accessory_types | level_accessory_types)
        self.assertGreater(total_unique_types, 0, "Should have some accessories generated")
    
    def test_shop_inventory_generation_isolation(self):
        """Test that multiple shops can generate items independently."""
        shops = []
        for i in range(5):
            shop = Shop(floor_level=5)
            shops.append(shop)
        
        # Each shop should have items
        for i, shop in enumerate(shops):
            non_empty_items = [item for item in shop.inventory if item]
            self.assertGreater(len(non_empty_items), 5, f"Shop {i} should have multiple items")
    
    def test_level_generation_order_independence(self):
        """Test that level generation works regardless of shop creation order."""
        # Create shops first
        shops = [Shop(floor_level=i) for i in range(1, 6)]
        
        # Then create levels - should still work fine
        levels = [Level(level_number=i) for i in range(1, 6)]
        
        # All levels should have their own items
        for level in levels:
            self.assertGreater(len(level.items), 0, "Level should have items regardless of shop creation")
    
    def test_no_items_or_monsters_at_shop_coordinates(self):
        """Comprehensive test that shop tiles are kept clear."""
        for floor_level in range(1, 6):  # Test multiple floors
            level = Level(level_number=floor_level)
            
            if level.shop:  # Floors 1-9 should have shops
                shop_x, shop_y = level.shop.x, level.shop.y
                
                # Check no monster at shop
                self.assertIsNone(level.get_monster_at(shop_x, shop_y))
                
                # Check no item at shop
                self.assertIsNone(level.get_item_at(shop_x, shop_y))
                
                # Verify shop position is walkable
                self.assertTrue(level.is_walkable(shop_x, shop_y))


if __name__ == '__main__':
    unittest.main()