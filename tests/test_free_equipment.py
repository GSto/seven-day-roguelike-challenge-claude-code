#!/usr/bin/env python3

import unittest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items.weapons.dagger import Dagger
from items.armor.leather_armor import LeatherArmor
from items.accessories.ring import Ring
from game import Game
import tcod


class TestFreeEquipment(unittest.TestCase):
    """Test that equipment can be equipped freely without XP costs."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.player = Player(5, 5)
        self.dagger = Dagger(0, 0)
        self.armor = LeatherArmor(0, 0)
        self.ring = Ring(0, 0, "Test Ring")
    
    def test_can_equip_always_true(self):
        """Test that can_equip always returns True."""
        self.assertTrue(self.dagger.can_equip(self.player))
        self.assertTrue(self.armor.can_equip(self.player))
        self.assertTrue(self.ring.can_equip(self.player))
        
        # Even with 0 XP, should still be able to equip
        self.player.xp = 0
        self.assertTrue(self.dagger.can_equip(self.player))
        self.assertTrue(self.armor.can_equip(self.player))
        self.assertTrue(self.ring.can_equip(self.player))
    
    def test_equipment_has_no_xp_cost_attribute(self):
        """Test that equipment no longer has xp_cost attribute."""
        self.assertFalse(hasattr(self.dagger, 'xp_cost'))
        self.assertFalse(hasattr(self.armor, 'xp_cost'))
        self.assertFalse(hasattr(self.ring, 'xp_cost'))
    
    def test_equipping_doesnt_deduct_xp(self):
        """Test that equipping items doesn't deduct XP."""
        initial_xp = 100
        self.player.xp = initial_xp
        
        # Add items to inventory
        self.player.add_item(self.dagger)
        self.player.add_item(self.armor)
        self.player.add_item(self.ring)
        
        # Create game instance to test equipping
        game = Game()
        game.player = self.player
        
        # Mock the UI to capture messages
        class MockUI:
            def __init__(self):
                self.messages = []
            def add_message(self, message):
                self.messages.append(message)
        
        game.ui = MockUI()
        
        # Equip items
        game.equip_item(self.dagger)
        game.equip_item(self.armor)
        game.equip_item(self.ring)
        
        # XP should be unchanged
        self.assertEqual(self.player.xp, initial_xp)
        
        # Check that items were equipped
        self.assertEqual(self.player.weapon, self.dagger)
        self.assertEqual(self.player.armor, self.armor)
        self.assertIn(self.ring, self.player.accessories)
    
    def test_equipment_messages_no_xp_reference(self):
        """Test that equipment messages don't mention XP costs."""
        initial_xp = 50
        self.player.xp = initial_xp
        
        # Add items to inventory
        self.player.add_item(self.dagger)
        
        # Create game instance to test equipping
        game = Game()
        game.player = self.player
        
        # Mock the UI to capture messages
        class MockUI:
            def __init__(self):
                self.messages = []
            def add_message(self, message):
                self.messages.append(message)
        
        game.ui = MockUI()
        
        # Equip item
        game.equip_item(self.dagger)
        
        # Check that no messages contain XP references
        for message in game.ui.messages:
            self.assertNotIn("XP", message)
            self.assertNotIn("xp", message.lower())
            self.assertNotIn("cost", message.lower())


if __name__ == '__main__':
    unittest.main()