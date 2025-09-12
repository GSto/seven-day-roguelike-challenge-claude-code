"""
Test suite for Ghost Pepper.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from player import Player
from items.consumables.ghost_pepper import GhostPepper
from event_emitter import EventEmitter


class TestGhostPepper(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Clear any existing EventEmitter instance
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        
        # Create test instances
        self.player = Player(5, 5)
        self.pepper = GhostPepper(0, 0)
    
    def tearDown(self):
        """Clean up after each test."""
        self.emitter.clear_all_listeners()
    
    def test_creation(self):
        """Test that Ghost Pepper is created with correct properties."""
        pepper = GhostPepper(3, 4)
        
        self.assertEqual(pepper.x, 3)
        self.assertEqual(pepper.y, 4)
        self.assertEqual(pepper.name, "Ghost Pepper")
        self.assertEqual(pepper.char, 'p')
        self.assertEqual(pepper.effect_value, 7)
        self.assertEqual(pepper.market_value, 65)
        
        # Check description contains key information
        self.assertIn("7 Max HP", pepper.description)
        self.assertIn("3 burn", pepper.description)
        self.assertIn("spicy", pepper.description.lower())
    
    def test_max_hp_increase(self):
        """Test that Ghost Pepper increases max HP by 7."""
        initial_max_hp = self.player.max_hp
        
        success, message = self.pepper.use(self.player)
        
        self.assertTrue(success)
        self.assertEqual(self.player.max_hp, initial_max_hp + 7)
        self.assertIn("Max HP +7", message)
    
    def test_burn_application(self):
        """Test that Ghost Pepper applies 3 burn status effect."""
        initial_burn = self.player.status_effects.burn
        
        success, message = self.pepper.use(self.player)
        
        self.assertTrue(success)
        self.assertEqual(self.player.status_effects.burn, initial_burn + 3)
        self.assertIn("3 burn applied", message)
    
    def test_use_return_values(self):
        """Test that use() returns correct success and message."""
        success, message = self.pepper.use(self.player)
        
        self.assertTrue(success)
        self.assertIsInstance(message, str)
        self.assertIn("ghost pepper", message.lower())
        self.assertIn("burning", message.lower())
    
    def test_effect_value_property(self):
        """Test that effect_value is properly set and used."""
        self.assertEqual(self.pepper.effect_value, 7)
        
        # Test that it's actually used in the use() method
        initial_max_hp = self.player.max_hp
        self.pepper.use(self.player)
        self.assertEqual(self.player.max_hp, initial_max_hp + self.pepper.effect_value)
    
    def test_market_value(self):
        """Test that Ghost Pepper has appropriate market value for rare consumable."""
        # Market value should be reasonable for rare consumable
        self.assertEqual(self.pepper.market_value, 65)
        self.assertGreaterEqual(self.pepper.market_value, 60)   # Rare minimum
        self.assertLessEqual(self.pepper.market_value, 100)    # Reasonable maximum
    
    def test_consumable_properties(self):
        """Test that Ghost Pepper has correct consumable properties."""
        # Should not have charges (single use)
        self.assertIsNone(self.pepper.charges)
        self.assertIsNone(self.pepper.max_charges)
        
        # Should not have multiplier effects
        self.assertEqual(self.pepper.attack_multiplier_effect, 0.0)
        self.assertEqual(self.pepper.defense_multiplier_effect, 0.0)
        self.assertEqual(self.pepper.xp_multiplier_effect, 0.0)
        
        # Should not have traits
        self.assertEqual(len(self.pepper.attack_traits), 0)
        self.assertEqual(len(self.pepper.weaknesses), 0)
        self.assertEqual(len(self.pepper.resistances), 0)
    
    def test_multiple_uses_stack(self):
        """Test that using multiple Ghost Peppers stacks the effects."""
        initial_max_hp = self.player.max_hp
        initial_burn = self.player.status_effects.burn
        
        # Use first pepper
        pepper1 = GhostPepper(0, 0)
        pepper1.use(self.player)
        
        # Use second pepper
        pepper2 = GhostPepper(0, 0)
        pepper2.use(self.player)
        
        # Check that effects stack
        self.assertEqual(self.player.max_hp, initial_max_hp + 14)  # +7 + 7
        self.assertEqual(self.player.status_effects.burn, initial_burn + 6)  # +3 + 3
    
    def test_burn_immunity_interaction(self):
        """Test interaction with burn immunity (if player had immunity)."""
        # Note: This test assumes the apply_status method respects immunity
        # Even if the player were immune to burn, max HP should still increase
        initial_max_hp = self.player.max_hp
        
        success, message = self.pepper.use(self.player)
        
        # Max HP increase should work regardless of burn immunity
        self.assertTrue(success)
        self.assertEqual(self.player.max_hp, initial_max_hp + 7)
    
    def test_risk_reward_balance(self):
        """Test that Ghost Pepper provides good risk-reward balance."""
        # +7 Max HP is substantial
        hp_gain = self.pepper.effect_value
        self.assertGreaterEqual(hp_gain, 5, "Should provide meaningful HP boost")
        self.assertLessEqual(hp_gain, 10, "Should not be overpowered")
        
        # 3 burn is significant but not crippling
        initial_burn = self.player.status_effects.burn
        self.pepper.use(self.player)
        burn_applied = self.player.status_effects.burn - initial_burn
        
        self.assertGreaterEqual(burn_applied, 2, "Should apply meaningful burn")
        self.assertLessEqual(burn_applied, 5, "Should not be crippling")
    
    def test_display_name(self):
        """Test that display name is correct (no charges)."""
        display_name = self.pepper.get_display_name()
        self.assertEqual(display_name, "Ghost Pepper")
        # Should not include charges since it doesn't have any
        self.assertNotIn("(", display_name)
        self.assertNotIn(")", display_name)
    
    def test_thematic_consistency(self):
        """Test that Ghost Pepper is thematically consistent."""
        # Should be red colored (spicy/hot)
        from constants import COLOR_RED
        self.assertEqual(self.pepper.color, COLOR_RED)
        
        # Description should convey the spicy/burning theme
        description = self.pepper.description.lower()
        self.assertTrue(any(word in description for word in ['spicy', 'pepper', 'burn', 'hot', 'tongue']))
    
    def test_rare_item_characteristics(self):
        """Test that Ghost Pepper has characteristics of a rare item."""
        # Should have higher market value than common consumables
        self.assertGreater(self.pepper.market_value, 35, "Should be more valuable than common items")
        
        # Should provide significant benefits to justify rarity
        self.assertGreaterEqual(self.pepper.effect_value, 5, "Should provide substantial HP gain")
        
        # Should have meaningful drawback to balance the benefit
        self.pepper.use(self.player)
        self.assertGreater(self.player.status_effects.burn, 0, "Should apply meaningful drawback")
    
    def test_status_effect_integration(self):
        """Test that Ghost Pepper properly integrates with status effect system."""
        # Test that burn is applied through the proper status system
        self.pepper.use(self.player)
        
        # Should use the status_effects.apply_status method
        self.assertGreater(self.player.status_effects.burn, 0)
        
        # Should allow for immunity checks if implemented
        # (The apply_status method handles immunity checking)
    
    def test_food_category_consistency(self):
        """Test that Ghost Pepper fits well in the food category."""
        # Should be a consumable food item (like other peppers/vegetables)
        self.assertIsInstance(self.pepper, GhostPepper)
        
        # Should provide permanent benefit like other stat foods
        initial_max_hp = self.player.max_hp
        self.pepper.use(self.player)
        final_max_hp = self.player.max_hp
        self.assertGreater(final_max_hp, initial_max_hp, "Should provide permanent stat increase")


if __name__ == '__main__':
    unittest.main()