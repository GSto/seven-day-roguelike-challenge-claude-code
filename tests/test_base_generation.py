"""
Unit tests for Base level generation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from level.base import Base
from constants import TILE_WALL, TILE_FLOOR, TILE_STAIRS_UP, TILE_STAIRS_DOWN


class TestBaseGeneration(unittest.TestCase):
    """Test the Base class generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base = Base(base_number=1)
    
    def test_base_initialization(self):
        """Test that base initializes with correct properties."""
        self.assertEqual(self.base.base_number, 1)
        self.assertEqual(len(self.base.monsters), 0)
        self.assertEqual(len(self.base.items), 0)
        self.assertTrue(self.base.is_safe_zone())
    
    def test_fixed_room_dimensions(self):
        """Test that the room has fixed dimensions."""
        # Count floor tiles to verify room size
        floor_tiles = 0
        for x in range(self.base.width):
            for y in range(self.base.height):
                if self.base.tiles[x, y] == TILE_FLOOR:
                    floor_tiles += 1
        
        # Interior of 18x11 room = (18-2) x (11-2) = 16 x 9 = 144 tiles
        # But we also have 2 stair tiles
        expected_floor_tiles = (Base.ROOM_WIDTH - 2) * (Base.ROOM_HEIGHT - 2)
        total_walkable = floor_tiles + 2  # Add stairs
        
        self.assertGreater(floor_tiles, 100)  # Should have substantial floor space
        self.assertLess(floor_tiles, 200)  # But not too much
    
    def test_stairs_placement(self):
        """Test that stairs are placed correctly."""
        # Check stairs up exists
        self.assertIsNotNone(self.base.stairs_up_pos)
        up_x, up_y = self.base.stairs_up_pos
        self.assertEqual(self.base.tiles[up_x, up_y], TILE_STAIRS_UP)
        
        # Check stairs down exists
        self.assertIsNotNone(self.base.stairs_down_pos)
        down_x, down_y = self.base.stairs_down_pos
        self.assertEqual(self.base.tiles[down_x, down_y], TILE_STAIRS_DOWN)
        
        # Verify stairs are vertically aligned (same x coordinate)
        self.assertEqual(up_x, down_x)
        
        # Verify stairs up is below stairs down
        self.assertGreater(up_y, down_y)
    
    def test_shop_placement(self):
        """Test that shop is placed in correct position."""
        self.assertIsNotNone(self.base.shop)
        
        # Shop should be in top-right area of room
        shop_x, shop_y = self.base.shop.x, self.base.shop.y
        
        # Verify shop is within room bounds
        self.assertGreater(shop_x, self.base.room_x1)
        self.assertLess(shop_x, self.base.room_x2)
        self.assertGreater(shop_y, self.base.room_y1)
        self.assertLess(shop_y, self.base.room_y2)
        
        # Shop should be in the right half of the room
        room_center_x = (self.base.room_x1 + self.base.room_x2) // 2
        self.assertGreater(shop_x, room_center_x)
        
        # Shop should be in the top half of the room
        room_center_y = (self.base.room_y1 + self.base.room_y2) // 2
        self.assertLess(shop_y, room_center_y)
    
    def test_shop_inventory_scaling(self):
        """Test that shop has items for the next floor."""
        # Base 1 should have items for floor 2
        base1 = Base(base_number=1)
        self.assertEqual(base1.shop.floor_level, 2)
        
        # Base 5 should have items for floor 6
        base5 = Base(base_number=5)
        self.assertEqual(base5.shop.floor_level, 6)
        
        # Base 9 should have items for floor 10 (boss items)
        base9 = Base(base_number=9)
        self.assertEqual(base9.shop.floor_level, 10)
    
    def test_no_random_elements(self):
        """Test that base layout is consistent (not random)."""
        # Create multiple bases with same number
        bases = [Base(base_number=3) for _ in range(5)]
        
        # All should have stairs at same positions
        first_up = bases[0].stairs_up_pos
        first_down = bases[0].stairs_down_pos
        first_shop = (bases[0].shop.x, bases[0].shop.y)
        
        for base in bases[1:]:
            self.assertEqual(base.stairs_up_pos, first_up)
            self.assertEqual(base.stairs_down_pos, first_down)
            self.assertEqual((base.shop.x, base.shop.y), first_shop)
    
    def test_safe_zone_mechanics(self):
        """Test that bases are safe zones."""
        self.assertTrue(self.base.is_safe_zone())
        
        # No monsters should exist
        self.assertEqual(len(self.base.monsters), 0)
        self.assertIsNone(self.base.get_monster_at(10, 10))
        self.assertFalse(self.base.is_position_occupied(10, 10))
        
        # No random items should exist
        self.assertEqual(len(self.base.items), 0)
        self.assertIsNone(self.base.get_item_at(10, 10))
    
    def test_walkability(self):
        """Test that floor tiles are walkable and walls are not."""
        # Test floor tile is walkable
        floor_x = (self.base.room_x1 + self.base.room_x2) // 2
        floor_y = (self.base.room_y1 + self.base.room_y2) // 2
        self.assertTrue(self.base.is_walkable(floor_x, floor_y))
        
        # Test wall is not walkable
        self.assertFalse(self.base.is_walkable(0, 0))
        
        # Test out of bounds is not walkable
        self.assertFalse(self.base.is_walkable(-1, -1))
        self.assertFalse(self.base.is_walkable(1000, 1000))
    
    def test_fov_functionality(self):
        """Test that FOV works in bases."""
        # Update FOV from center of room
        center_x = (self.base.room_x1 + self.base.room_x2) // 2
        center_y = (self.base.room_y1 + self.base.room_y2) // 2
        
        self.base.update_fov(center_x, center_y, fov_radius=8)
        
        # Center should be visible
        self.assertTrue(self.base.fov[center_x, center_y])
        
        # Center should be explored
        self.assertTrue(self.base.explored[center_x, center_y])
        
        # Far corner should not be visible
        self.assertFalse(self.base.fov[0, 0])


if __name__ == '__main__':
    unittest.main()