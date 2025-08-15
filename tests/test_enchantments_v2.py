#!/usr/bin/env python3
"""
Test the new unified enchantment system.
"""

import unittest
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from items.enchantments import (
    EnchantmentType, 
    Enchantment,
    get_random_weapon_enchantment,
    get_random_armor_enchantment,
    get_weapon_enchantment_by_type,
    get_armor_enchantment_by_type
)
from traits import Trait


class TestEnchantmentsV2(unittest.TestCase):
    """Test the new unified enchantment system."""
    
    def test_enchantment_type_flags(self):
        """Test that enchantment type flags work correctly."""
        # SHADOW can only enchant armor
        self.assertFalse(EnchantmentType.SHADOW.can_enchant_weapon)
        self.assertTrue(EnchantmentType.SHADOW.can_enchant_armor)
        
        # RENDING can only enchant weapons
        self.assertTrue(EnchantmentType.RENDING.can_enchant_weapon)
        self.assertFalse(EnchantmentType.RENDING.can_enchant_armor)
        
        # QUALITY can enchant both
        self.assertTrue(EnchantmentType.QUALITY.can_enchant_weapon)
        self.assertTrue(EnchantmentType.QUALITY.can_enchant_armor)
    
    def test_enchantment_labels(self):
        """Test that enchantment labels are correct."""
        # Test same labels for both
        self.assertEqual(EnchantmentType.QUALITY.get_weapon_label(), "quality")
        self.assertEqual(EnchantmentType.QUALITY.get_armor_label(), "quality")
        
        # Test different labels
        self.assertEqual(EnchantmentType.BALANCED.get_weapon_label(), "bolstered")
        self.assertEqual(EnchantmentType.BALANCED.get_armor_label(), "spiked")
        
        # Test elemental labels
        self.assertEqual(EnchantmentType.FIRE.get_weapon_label(), "flaming")
        self.assertEqual(EnchantmentType.FIRE.get_armor_label(), "fireproof")
    
    def test_weapon_enchantment_bonuses(self):
        """Test weapon enchantment bonuses."""
        quality = Enchantment(EnchantmentType.QUALITY, "weapon")
        self.assertEqual(quality.get_weapon_attack_bonus(), 3)
        self.assertEqual(quality.get_weapon_defense_bonus(), 0)
        
        balanced = Enchantment(EnchantmentType.BALANCED, "weapon") 
        self.assertEqual(balanced.get_weapon_attack_bonus(), 0)
        self.assertEqual(balanced.get_weapon_defense_bonus(), 1)
        
        shiny = Enchantment(EnchantmentType.SHINY, "weapon")
        self.assertEqual(shiny.get_weapon_attack_multiplier_bonus(), 0.25)
        
        rending = Enchantment(EnchantmentType.RENDING, "weapon")
        self.assertEqual(rending.get_weapon_crit_bonus(), 0.05)
    
    def test_armor_enchantment_bonuses(self):
        """Test armor enchantment bonuses."""
        quality = Enchantment(EnchantmentType.QUALITY, "armor")
        self.assertEqual(quality.get_armor_defense_bonus(), 3)
        self.assertEqual(quality.get_armor_attack_bonus(), 0)
        
        balanced = Enchantment(EnchantmentType.BALANCED, "armor")
        self.assertEqual(balanced.get_armor_attack_bonus(), 1)  # Spiked
        self.assertEqual(balanced.get_armor_defense_bonus(), 0)
        
        shiny = Enchantment(EnchantmentType.SHINY, "armor")
        self.assertEqual(shiny.get_armor_defense_multiplier_bonus(), 0.25)
        
        shadow = Enchantment(EnchantmentType.SHADOW, "armor")
        self.assertEqual(shadow.get_armor_evade_bonus(), 0.05)
    
    def test_shared_bonuses(self):
        """Test bonuses that work the same on weapons and armor."""
        weapon_glowing = Enchantment(EnchantmentType.GLOWING, "weapon")
        armor_glowing = Enchantment(EnchantmentType.GLOWING, "armor")
        
        self.assertEqual(weapon_glowing.get_weapon_fov_bonus(), 3)
        self.assertEqual(armor_glowing.get_armor_fov_bonus(), 3)
        
        weapon_blessed = Enchantment(EnchantmentType.BLESSED, "weapon")
        armor_blessed = Enchantment(EnchantmentType.BLESSED, "armor")
        
        self.assertEqual(weapon_blessed.get_health_aspect_bonus(), 0.10)
        self.assertEqual(armor_blessed.get_health_aspect_bonus(), 0.10)
    
    def test_trait_enchantments(self):
        """Test trait-based enchantments."""
        fire_weapon = Enchantment(EnchantmentType.FIRE, "weapon")
        self.assertEqual(fire_weapon.attack_traits, [Trait.FIRE])
        self.assertEqual(fire_weapon.resistances, [])
        
        fire_armor = Enchantment(EnchantmentType.FIRE, "armor")
        self.assertEqual(fire_armor.attack_traits, [])
        self.assertEqual(fire_armor.resistances, [Trait.FIRE])
    
    def test_random_enchantment_generation(self):
        """Test random enchantment generation respects flags."""
        # Generate many random weapon enchantments
        for _ in range(50):
            weapon_enchant = get_random_weapon_enchantment()
            self.assertTrue(weapon_enchant.type.can_enchant_weapon)
            self.assertEqual(weapon_enchant.target_type, "weapon")
            
        # Generate many random armor enchantments  
        for _ in range(50):
            armor_enchant = get_random_armor_enchantment()
            self.assertTrue(armor_enchant.type.can_enchant_armor)
            self.assertEqual(armor_enchant.target_type, "armor")
    
    def test_enchantment_by_type_validation(self):
        """Test that enchantment creation validates compatibility."""
        # Valid combinations should work
        weapon_quality = get_weapon_enchantment_by_type(EnchantmentType.QUALITY)
        self.assertEqual(weapon_quality.type, EnchantmentType.QUALITY)
        
        armor_shadow = get_armor_enchantment_by_type(EnchantmentType.SHADOW)
        self.assertEqual(armor_shadow.type, EnchantmentType.SHADOW)
        
        # Invalid combinations should raise errors
        with self.assertRaises(ValueError):
            get_weapon_enchantment_by_type(EnchantmentType.SHADOW)
            
        with self.assertRaises(ValueError):
            get_armor_enchantment_by_type(EnchantmentType.RENDING)


if __name__ == '__main__':
    unittest.main()