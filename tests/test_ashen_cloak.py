"""
Test suite for Ashen Cloak.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from player import Player
from items.armor.ashen_cloak import AshenCloak
from traits import Trait
from event_emitter import EventEmitter


class TestAshenCloak(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Clear any existing EventEmitter instance
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        
        # Create test instances
        self.player = Player(5, 5)
        self.cloak = AshenCloak(0, 0)
    
    def tearDown(self):
        """Clean up after each test."""
        self.emitter.clear_all_listeners()
    
    def test_creation(self):
        """Test that Ashen Cloak is created with correct properties."""
        cloak = AshenCloak(3, 4)
        
        self.assertEqual(cloak.x, 3)
        self.assertEqual(cloak.y, 4)
        self.assertEqual(cloak.name, "Ashen Cloak")
        self.assertEqual(cloak.char, "[")
        self.assertEqual(cloak.defense_bonus, 0)
        self.assertEqual(cloak.evade_bonus, 0.16)
        self.assertEqual(cloak.equipment_slot, "armor")
        self.assertEqual(cloak.market_value, 75)
        
        # Check description contains key information
        self.assertIn("16% EVD", cloak.description)
        self.assertIn("resistance", cloak.description.lower())
        self.assertIn("Fire", cloak.description)
        self.assertIn("Ice", cloak.description)
        self.assertIn("Poison", cloak.description)
    
    def test_resistances(self):
        """Test that Ashen Cloak has the correct resistances."""
        expected_resistances = [Trait.FIRE, Trait.ICE, Trait.POISON]
        
        resistances = self.cloak.get_resistances()
        self.assertEqual(len(resistances), 3)
        for resistance in expected_resistances:
            self.assertIn(resistance, resistances)
    
    def test_evade_bonus(self):
        """Test that the cloak provides +16% evasion bonus."""
        evade_bonus = self.cloak.get_evade_bonus(self.player)
        self.assertEqual(evade_bonus, 0.16)
    
    def test_no_defense_bonus(self):
        """Test that Ashen Cloak provides no defense bonus (evasion-focused)."""
        defense_bonus = self.cloak.get_defense_bonus(self.player)
        self.assertEqual(defense_bonus, 0)
    
    def test_no_weaknesses(self):
        """Test that Ashen Cloak has no weaknesses (only resistances)."""
        weaknesses = self.cloak.get_weaknesses()
        self.assertEqual(len(weaknesses), 0)
    
    def test_no_attack_traits(self):
        """Test that Ashen Cloak has no attack traits."""
        attack_traits = self.cloak.get_attack_traits()
        self.assertEqual(len(attack_traits), 0)
    
    def test_equip_functionality(self):
        """Test that the cloak can be equipped and provides bonuses."""
        # Equip the cloak
        self.player.armor = self.cloak
        
        # Check that it's equipped
        self.assertEqual(self.player.armor, self.cloak)
        
        # Check that evade bonus is applied
        expected_evade = self.player.get_total_evade()
        self.assertGreaterEqual(expected_evade, 0.16)
    
    def test_resistance_integration(self):
        """Test that resistances are properly integrated with the equipment system."""
        # Equip the cloak
        self.player.armor = self.cloak
        
        # Test that the player now has these resistances
        player_resistances = self.player.get_total_resistances()
        
        expected_resistances = [Trait.FIRE, Trait.ICE, Trait.POISON]
        for resistance in expected_resistances:
            self.assertIn(resistance, player_resistances)
    
    def test_market_value(self):
        """Test that Ashen Cloak has appropriate market value for rare mid-game armor."""
        # Market value should be reasonable for rare mid-game armor
        self.assertEqual(self.cloak.get_market_value(), 75)
        self.assertGreaterEqual(self.cloak.market_value, 60)   # Rare minimum
        self.assertLessEqual(self.cloak.market_value, 100)    # Reasonable maximum
    
    def test_evasion_focused_stats(self):
        """Test that Ashen Cloak is focused on evasion, not other stats."""
        # Test that other bonuses are zero/default except evasion
        self.assertEqual(self.cloak.attack_bonus, 0)
        self.assertEqual(self.cloak.defense_bonus, 0)
        self.assertEqual(self.cloak.fov_bonus, 0)
        self.assertEqual(self.cloak.health_aspect_bonus, 0.0)
        self.assertEqual(self.cloak.attack_multiplier_bonus, 1.0)
        self.assertEqual(self.cloak.defense_multiplier_bonus, 1.0)
        self.assertEqual(self.cloak.xp_multiplier_bonus, 1.0)
        self.assertEqual(self.cloak.crit_bonus, 0.0)
        self.assertEqual(self.cloak.crit_multiplier_bonus, 0.0)
        
        # Only evasion should be non-zero
        self.assertEqual(self.cloak.evade_bonus, 0.16)
    
    def test_enchantment_support(self):
        """Test that Ashen Cloak supports the enchantment system."""
        # Should inherit enchantment support from base Armor class
        self.assertEqual(len(self.cloak.enchantments), 0)
        self.assertTrue(hasattr(self.cloak, 'add_enchantment'))
        self.assertTrue(hasattr(self.cloak, '_update_display_name'))
    
    def test_comparison_with_other_cloaks(self):
        """Test that Ashen Cloak provides competitive evasion for its level range."""
        # At +16% EVD, this should be strong evasion armor
        self.assertGreaterEqual(self.cloak.evade_bonus, 0.15)  # Better than basic cloaks
        self.assertLessEqual(self.cloak.evade_bonus, 0.25)     # Not overpowered
    
    def test_resistance_traits_are_elemental(self):
        """Test that all resistance traits are properly elemental types."""
        for resistance in self.cloak.resistances:
            self.assertTrue(resistance.is_elemental, f"{resistance} should be elemental")
    
    def test_balanced_design(self):
        """Test that the cloak follows balanced design principles."""
        # High evasion with useful resistances but no defense = balanced tradeoff
        resistance_count = len(self.cloak.resistances)
        evade_value = self.cloak.evade_bonus
        
        # Should have meaningful resistances and strong evasion
        self.assertGreaterEqual(resistance_count, 3, "Should have multiple resistances")
        self.assertGreaterEqual(evade_value, 0.15, "Should provide substantial evasion")
        self.assertEqual(self.cloak.defense_bonus, 0, "Should have no defense for balance")
    
    def test_resistance_coverage(self):
        """Test that resistances cover a good spread of damage types."""
        resistances = set(self.cloak.resistances)
        
        # Should cover different elemental types
        self.assertIn(Trait.FIRE, resistances, "Should resist fire")
        self.assertIn(Trait.ICE, resistances, "Should resist ice")
        self.assertIn(Trait.POISON, resistances, "Should resist poison")
        
        # Should not have overlapping opposites (fire vs ice is fine since both resisted)
        # This is a design choice - resisting both opposites shows magical nature
    
    def test_mid_game_appropriate(self):
        """Test that the item is appropriate for mid-game (floors 5-8)."""
        # Should be powerful enough for mid-game but not game-breaking
        total_power_level = self.cloak.evade_bonus + (len(self.cloak.resistances) * 0.05)
        self.assertGreaterEqual(total_power_level, 0.25, "Should be substantial for mid-game")
        self.assertLessEqual(total_power_level, 0.5, "Should not be overpowered")
    
    def test_unique_identity(self):
        """Test that Ashen Cloak has a unique identity among armor."""
        # Should be the premier evasion + resistance armor
        self.assertEqual(self.cloak.defense_bonus, 0, "Pure evasion focus")
        self.assertGreater(self.cloak.evade_bonus, 0.1, "Strong evasion bonus")
        self.assertGreaterEqual(len(self.cloak.resistances), 3, "Multiple resistances")


if __name__ == '__main__':
    unittest.main()