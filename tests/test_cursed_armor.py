"""
Test suite for Cursed Armor.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from player import Player
from items.armor.cursed_armor import CursedArmor
from traits import Trait
from event_emitter import EventEmitter


class TestCursedArmor(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Clear any existing EventEmitter instance
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        
        # Create test instances
        self.player = Player(5, 5)
        self.armor = CursedArmor(0, 0)
    
    def tearDown(self):
        """Clean up after each test."""
        self.emitter.clear_all_listeners()
    
    def test_creation(self):
        """Test that Cursed Armor is created with correct properties."""
        armor = CursedArmor(3, 4)
        
        self.assertEqual(armor.x, 3)
        self.assertEqual(armor.y, 4)
        self.assertEqual(armor.name, "Cursed Armor")
        self.assertEqual(armor.char, "[")
        self.assertEqual(armor.defense_bonus, 9)
        self.assertEqual(armor.equipment_slot, "armor")
        self.assertEqual(armor.market_value, 55)
        
        # Check description contains key information
        self.assertIn("9 DEF", armor.description)
        self.assertIn("weakness", armor.description.lower())
        self.assertIn("Fire", armor.description)
        self.assertIn("Ice", armor.description)
        self.assertIn("Holy", armor.description)
        self.assertIn("Dark", armor.description)
    
    def test_weaknesses(self):
        """Test that Cursed Armor has the correct weaknesses."""
        expected_weaknesses = [Trait.FIRE, Trait.ICE, Trait.HOLY, Trait.DARK]
        
        self.assertEqual(len(self.armor.weaknesses), 4)
        for weakness in expected_weaknesses:
            self.assertIn(weakness, self.armor.weaknesses)
    
    def test_defense_bonus(self):
        """Test that the armor provides +9 defense bonus."""
        defense_bonus = self.armor.get_defense_bonus(self.player)
        self.assertEqual(defense_bonus, 9)
    
    def test_no_resistances(self):
        """Test that Cursed Armor has no resistances (only weaknesses)."""
        resistances = self.armor.get_resistances()
        self.assertEqual(len(resistances), 0)
    
    def test_no_attack_traits(self):
        """Test that Cursed Armor has no attack traits."""
        attack_traits = self.armor.get_attack_traits()
        self.assertEqual(len(attack_traits), 0)
    
    def test_equip_functionality(self):
        """Test that the armor can be equipped and provides bonuses."""
        # Equip the armor
        self.player.armor = self.armor
        
        # Check that it's equipped
        self.assertEqual(self.player.armor, self.armor)
        
        # Check that defense bonus is applied
        expected_defense = self.player.get_total_defense()
        self.assertGreaterEqual(expected_defense, 9)
    
    def test_weakness_integration(self):
        """Test that weaknesses are properly integrated with the equipment system."""
        # Equip the armor
        self.player.armor = self.armor
        
        # Test that the player now has these weaknesses
        player_weaknesses = self.player.get_total_weaknesses()
        
        expected_weaknesses = [Trait.FIRE, Trait.ICE, Trait.HOLY, Trait.DARK]
        for weakness in expected_weaknesses:
            self.assertIn(weakness, player_weaknesses)
    
    def test_market_value(self):
        """Test that Cursed Armor has appropriate market value for uncommon mid-game armor."""
        # Market value should be reasonable for uncommon mid-game armor
        self.assertEqual(self.armor.get_market_value(), 55)
        self.assertGreaterEqual(self.armor.market_value, 35)  # Uncommon minimum
        self.assertLessEqual(self.armor.market_value, 60)    # Uncommon maximum
    
    def test_armor_stats_only(self):
        """Test that Cursed Armor only affects defense and weaknesses, no other stats."""
        # Test that other bonuses are zero/default
        self.assertEqual(self.armor.attack_bonus, 0)
        self.assertEqual(self.armor.fov_bonus, 0)
        self.assertEqual(self.armor.health_aspect_bonus, 0.0)
        self.assertEqual(self.armor.attack_multiplier_bonus, 1.0)
        self.assertEqual(self.armor.defense_multiplier_bonus, 1.0)
        self.assertEqual(self.armor.xp_multiplier_bonus, 1.0)
        self.assertEqual(self.armor.evade_bonus, 0.0)
        self.assertEqual(self.armor.crit_bonus, 0.0)
        self.assertEqual(self.armor.crit_multiplier_bonus, 0.0)
    
    def test_enchantment_support(self):
        """Test that Cursed Armor supports the enchantment system."""
        # Should inherit enchantment support from base Armor class
        self.assertEqual(len(self.armor.enchantments), 0)
        self.assertTrue(hasattr(self.armor, 'add_enchantment'))
        self.assertTrue(hasattr(self.armor, '_update_display_name'))
    
    def test_comparison_with_other_armor(self):
        """Test that Cursed Armor provides competitive defense for its level range."""
        # At +9 DEF, this should be strong mid-game armor
        # Should be stronger than early armor but have the weakness tradeoff
        self.assertGreaterEqual(self.armor.defense_bonus, 5)  # Better than early armor
        self.assertLessEqual(self.armor.defense_bonus, 12)    # Not overpowered
    
    def test_weakness_traits_are_elemental(self):
        """Test that all weakness traits are properly elemental types."""
        for weakness in self.armor.weaknesses:
            self.assertTrue(weakness.is_elemental, f"{weakness} should be elemental")
    
    def test_balanced_design(self):
        """Test that the armor follows balanced design principles."""
        # High defense but significant weaknesses = balanced tradeoff
        weakness_count = len(self.armor.weaknesses)
        defense_value = self.armor.defense_bonus
        
        # Should have substantial weaknesses to offset high defense
        self.assertGreaterEqual(weakness_count, 3, "Should have multiple weaknesses for balance")
        self.assertGreaterEqual(defense_value, 8, "Should provide substantial defense")


if __name__ == '__main__':
    unittest.main()