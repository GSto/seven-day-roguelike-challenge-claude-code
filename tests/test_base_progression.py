"""
Unit tests for base progression system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from level_manager import LevelManager
from level.level import Level
from level.base import Base
from player import Player


class TestBaseProgression(unittest.TestCase):
    """Test the floor/base progression system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.level_manager = LevelManager()
        self.player = Player(5, 5)
    
    def test_initial_state(self):
        """Test that game starts on Floor 1."""
        self.assertEqual(self.level_manager.get_current_floor_number(), 1)
        self.assertFalse(self.level_manager.is_in_base())
        self.assertEqual(self.level_manager.get_display_name(), "Floor 1")
        self.assertIsInstance(self.level_manager.get_current_area(), Level)
    
    def test_floor_to_base_transition(self):
        """Test transition from floor to base."""
        # Start on Floor 1
        self.assertFalse(self.level_manager.is_in_base())
        
        # Transition down should go to Base 1
        result = self.level_manager.transition_down(self.player)
        self.assertTrue(result[0] if isinstance(result, tuple) else result)
        self.assertTrue(self.level_manager.is_in_base())
        self.assertEqual(self.level_manager.get_display_name(), "Base 1")
        self.assertIsInstance(self.level_manager.get_current_area(), Base)
    
    def test_base_to_floor_transition(self):
        """Test transition from base to floor."""
        # Start on Floor 1, transition to Base 1
        self.level_manager.transition_down(self.player)
        self.assertTrue(self.level_manager.is_in_base())
        
        # Transition down should go to Floor 2
        result = self.level_manager.transition_down(self.player)
        success = result[0] if isinstance(result, tuple) else result
        self.assertTrue(success)
        self.assertFalse(self.level_manager.is_in_base())
        self.assertEqual(self.level_manager.get_current_floor_number(), 2)
        self.assertEqual(self.level_manager.get_display_name(), "Floor 2")
        self.assertIsInstance(self.level_manager.get_current_area(), Level)
    
    def test_complete_progression_sequence(self):
        """Test the complete floor/base sequence."""
        expected_sequence = [
            ("Floor 1", False),
            ("Base 1", True),
            ("Floor 2", False),
            ("Base 2", True),
            ("Floor 3", False),
            ("Base 3", True),
            ("Floor 4", False),
        ]
        
        for expected_name, expected_in_base in expected_sequence:
            self.assertEqual(self.level_manager.get_display_name(), expected_name)
            self.assertEqual(self.level_manager.is_in_base(), expected_in_base)
            
            if expected_name != "Floor 4":  # Don't transition after the last check
                result = self.level_manager.transition_down(self.player)
                success = result[0] if isinstance(result, tuple) else result
                self.assertTrue(success)
    
    def test_floor_10_completion(self):
        """Test that Floor 10 is the final floor."""
        # Progress to Floor 10
        for _ in range(18):  # 9 floors + 9 bases = 18 transitions to reach Floor 10
            success = self.level_manager.transition_down(self.player)
            self.assertTrue(success)
        
        self.assertEqual(self.level_manager.get_display_name(), "Floor 10")
        self.assertFalse(self.level_manager.is_in_base())
        
        # Trying to transition down from Floor 10 should fail
        result = self.level_manager.transition_down(self.player)
        success = result[0] if isinstance(result, tuple) else result
        self.assertFalse(success)
    
    def test_base_shop_inventory_scaling(self):
        """Test that base shops have correct inventory for next floor."""
        # Start on Floor 1, go to Base 1
        self.level_manager.transition_down(self.player)
        
        base1 = self.level_manager.get_current_area()
        self.assertIsInstance(base1, Base)
        self.assertEqual(base1.shop.floor_level, 2)  # Base 1 has Floor 2 items
        
        # Go to Floor 2, then Base 2
        self.level_manager.transition_down(self.player)  # To Floor 2
        self.level_manager.transition_down(self.player)  # To Base 2
        
        base2 = self.level_manager.get_current_area()
        self.assertIsInstance(base2, Base)
        self.assertEqual(base2.shop.floor_level, 3)  # Base 2 has Floor 3 items
    
    def test_safe_zone_detection(self):
        """Test that safe zones are correctly detected."""
        # Floor should not be safe zone
        self.assertFalse(self.level_manager.get_safe_zone_status())
        
        # Base should be safe zone
        self.level_manager.transition_down(self.player)
        self.assertTrue(self.level_manager.get_safe_zone_status())
        
        # Floor again should not be safe zone
        self.level_manager.transition_down(self.player)
        self.assertFalse(self.level_manager.get_safe_zone_status())
    
    def test_can_attack_in_areas(self):
        """Test that combat is only allowed in floors, not bases."""
        # Combat allowed on floors
        self.assertTrue(self.level_manager.can_attack())
        
        # Combat not allowed in bases
        self.level_manager.transition_down(self.player)
        self.assertFalse(self.level_manager.can_attack())
        
        # Combat allowed again on floors
        self.level_manager.transition_down(self.player)
        self.assertTrue(self.level_manager.can_attack())


if __name__ == '__main__':
    unittest.main()