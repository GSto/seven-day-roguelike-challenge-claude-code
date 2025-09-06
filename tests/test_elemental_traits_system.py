"""Test the new elemental traits system with catalysts and cancellation logic."""

import unittest
from src.player import Player
from traits import Trait
from src.items.consumables import (
    FireAttackCatalyst, IceAttackCatalyst, HolyAttackCatalyst, DarkAttackCatalyst
)


class TestElementalTraitsSystem(unittest.TestCase):
    """Test the enhanced traits system with elemental properties and cancellation."""
    
    def setUp(self):
        """Set up test environment."""
        self.player = Player(5, 5)
        # Clear starting traits
        self.player.attack_traits.clear()
        self.player.resistances.clear()
        self.player.weaknesses.clear()
        
    def test_trait_elemental_properties(self):
        """Test that traits correctly identify as elemental or not."""
        # Test elemental traits
        self.assertTrue(Trait.FIRE.is_elemental)
        self.assertTrue(Trait.ICE.is_elemental)
        self.assertTrue(Trait.HOLY.is_elemental)
        self.assertTrue(Trait.DARK.is_elemental)
        
        # Test non-elemental traits
        self.assertFalse(Trait.STRIKE.is_elemental)
        self.assertFalse(Trait.SLASH.is_elemental)
        self.assertFalse(Trait.DEMONSLAYER.is_elemental)
        self.assertFalse(Trait.MYSTIC.is_elemental)
    
    def test_opposing_elements(self):
        """Test that opposing elements are correctly identified."""
        self.assertEqual(Trait.FIRE.opposing_element, Trait.ICE)
        self.assertEqual(Trait.ICE.opposing_element, Trait.FIRE)
        self.assertEqual(Trait.HOLY.opposing_element, Trait.DARK)
        self.assertEqual(Trait.DARK.opposing_element, Trait.HOLY)
        
        # Non-elemental traits should have no opposing element
        self.assertIsNone(Trait.STRIKE.opposing_element)
        self.assertIsNone(Trait.SLASH.opposing_element)
    
    def test_fire_attack_catalyst(self):
        """Test Fire Attack Catalyst adds fire trait and ice weakness."""
        catalyst = FireAttackCatalyst(0, 0)
        
        # Verify initial state
        self.assertEqual(len(self.player.attack_traits), 0)
        self.assertEqual(len(self.player.weaknesses), 0)
        
        # Use catalyst
        success, message = catalyst.use(self.player)
        
        # Verify effects
        self.assertTrue(success)
        self.assertIn(Trait.FIRE, self.player.attack_traits)
        self.assertIn(Trait.ICE, self.player.weaknesses)
        self.assertIn("fire", message.lower())
        self.assertIn("ice", message.lower())
    
    def test_ice_attack_catalyst(self):
        """Test Ice Attack Catalyst adds ice trait and fire weakness."""
        catalyst = IceAttackCatalyst(0, 0)
        
        success, message = catalyst.use(self.player)
        
        self.assertTrue(success)
        self.assertIn(Trait.ICE, self.player.attack_traits)
        self.assertIn(Trait.FIRE, self.player.weaknesses)
    
    def test_holy_attack_catalyst(self):
        """Test Holy Attack Catalyst adds holy trait and dark weakness."""
        catalyst = HolyAttackCatalyst(0, 0)
        
        success, message = catalyst.use(self.player)
        
        self.assertTrue(success)
        self.assertIn(Trait.HOLY, self.player.attack_traits)
        self.assertIn(Trait.DARK, self.player.weaknesses)
    
    def test_dark_attack_catalyst(self):
        """Test Dark Attack Catalyst adds dark trait and holy weakness."""
        catalyst = DarkAttackCatalyst(0, 0)
        
        success, message = catalyst.use(self.player)
        
        self.assertTrue(success)
        self.assertIn(Trait.DARK, self.player.attack_traits)
        self.assertIn(Trait.HOLY, self.player.weaknesses)
    
    
    def test_trait_cancellation_weakness_vs_resistance(self):
        """Test that matching weakness and resistance cancel each other out."""
        # Add fire resistance
        self.player.resistances.append(Trait.FIRE)
        # Add fire weakness  
        self.player.weaknesses.append(Trait.FIRE)
        
        # Both should cancel out
        final_resistances = self.player.get_total_resistances()
        final_weaknesses = self.player.get_total_weaknesses()
        
        self.assertNotIn(Trait.FIRE, final_resistances)
        self.assertNotIn(Trait.FIRE, final_weaknesses)
    
    def test_trait_cancellation_partial(self):
        """Test that only matching traits cancel, others remain."""
        # Add multiple resistances and weaknesses
        self.player.resistances.extend([Trait.FIRE, Trait.ICE])
        self.player.weaknesses.extend([Trait.FIRE, Trait.HOLY])  # Fire will cancel, Holy and Ice remain
        
        final_resistances = self.player.get_total_resistances()
        final_weaknesses = self.player.get_total_weaknesses()
        
        # Fire should be cancelled from both
        self.assertNotIn(Trait.FIRE, final_resistances)
        self.assertNotIn(Trait.FIRE, final_weaknesses)
        
        # Ice resistance should remain (no matching weakness)
        self.assertIn(Trait.ICE, final_resistances)
        
        # Holy weakness should remain (no matching resistance)
        self.assertIn(Trait.HOLY, final_weaknesses)
    
    def test_attack_catalyst_does_not_duplicate_traits(self):
        """Test that using the same attack catalyst twice doesn't duplicate traits."""
        catalyst = FireAttackCatalyst(0, 0)
        
        # Use catalyst twice
        catalyst.use(self.player)
        catalyst.use(self.player)
        
        # Should only have one of each trait
        fire_attack_count = self.player.attack_traits.count(Trait.FIRE)
        ice_weakness_count = self.player.weaknesses.count(Trait.ICE)
        
        self.assertEqual(fire_attack_count, 1)
        self.assertEqual(ice_weakness_count, 1)
    
    
    


if __name__ == '__main__':
    unittest.main()