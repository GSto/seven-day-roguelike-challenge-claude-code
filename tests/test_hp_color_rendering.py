#!/usr/bin/env python3

import unittest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from ui import UI
from constants import COLOR_GREEN, COLOR_RED, COLOR_WHITE
import tcod.console


class TestHPColorRendering(unittest.TestCase):
    """Test the HP color rendering based on player health status."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.player = Player(5, 5)
        self.ui = UI()
        self.console = tcod.console.Console(80, 50)
    
    def test_high_hp_renders_green(self):
        """Test that high HP (>=80%) renders in green."""
        # Set player to high HP (80% or more)
        self.player.hp = int(self.player.max_hp * 0.8)
        self.assertTrue(self.player.has_high_hp())
        self.assertFalse(self.player.has_low_hp())
        
        # This test verifies the logic exists - actual rendering test would require
        # mocking console.print or checking the rendered output
        self.assertTrue(self.player.has_high_hp())
    
    def test_low_hp_renders_red(self):
        """Test that low HP (<30% or <30 absolute) renders in red."""
        # Set player to low HP
        self.player.hp = int(self.player.max_hp * 0.2)  # 20% HP
        self.assertTrue(self.player.has_low_hp())
        self.assertFalse(self.player.has_high_hp())
        
        # This test verifies the logic exists - actual rendering test would require
        # mocking console.print or checking the rendered output
        self.assertTrue(self.player.has_low_hp())
    
    def test_normal_hp_renders_white(self):
        """Test that normal HP (between low and high) renders in white."""
        # Set player to normal HP (between 30% and 80%)
        self.player.hp = int(self.player.max_hp * 0.5)  # 50% HP
        self.assertFalse(self.player.has_high_hp())
        self.assertFalse(self.player.has_low_hp())
        
        # This test verifies the logic exists - actual rendering test would require
        # mocking console.print or checking the rendered output
        self.assertFalse(self.player.has_high_hp())
        self.assertFalse(self.player.has_low_hp())
    
    def test_hp_thresholds(self):
        """Test the HP threshold boundaries."""
        # Test high HP threshold (80%)
        self.player.hp = int(self.player.max_hp * 0.8)
        self.assertTrue(self.player.has_high_hp())
        
        self.player.hp = int(self.player.max_hp * 0.8) - 1
        self.assertFalse(self.player.has_high_hp())
        
        # Test low HP threshold (30% or 30 absolute, whichever is lower)
        low_threshold = min(int(self.player.max_hp * 0.3), 30)
        self.player.hp = low_threshold - 1
        self.assertTrue(self.player.has_low_hp())
        
        self.player.hp = low_threshold
        self.assertFalse(self.player.has_low_hp())


if __name__ == '__main__':
    unittest.main()