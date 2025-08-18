#!/usr/bin/env python3
"""
Test the enchantment override system for weapons and armor.
"""

import unittest
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enchantments import EnchantmentType, get_weapon_enchantment_by_type, get_armor_enchantment_by_type
from items.weapons.clerics_staff import ClericsStaff
from items.armor.base import Armor
from player import Player


class TestEnchantmentOverride(unittest.TestCase):
    """Test the enchantment override system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.player = Player(5, 5)
    
    def test_clerics_staff_blessed_override(self):
        """Test that Cleric's Staff gets special bonuses with BLESSED enchantment."""
        staff = ClericsStaff(0, 0)
        blessed_enchant = get_weapon_enchantment_by_type(EnchantmentType.BLESSED)
        
        # Add the enchantment
        success = staff.add_enchantment(blessed_enchant)
        self.assertTrue(success)
        
        # Test attack bonus (should be base blessed bonus + 4)
        attack_bonus = staff.get_attack_bonus(self.player)
        expected_attack = staff.attack_bonus + blessed_enchant.get_weapon_attack_bonus() + 4
        self.assertEqual(attack_bonus, expected_attack)
        
        # Test health aspect bonus (should be base staff bonus + blessed enchant bonus + override bonus)
        health_bonus = staff.get_health_aspect_bonus(self.player)
        # Staff base: 0.2, Blessed enchant: 0.1, Override bonus: 0.1 = 0.4 total
        expected_health = 0.2 + 0.1 + 0.1
        self.assertAlmostEqual(health_bonus, expected_health, places=5)
    
    def test_clerics_staff_holy_override(self):
        """Test that Cleric's Staff gets special bonuses with HOLY enchantment."""
        staff = ClericsStaff(0, 0)
        holy_enchant = get_weapon_enchantment_by_type(EnchantmentType.HOLY)
        
        # Add the enchantment
        success = staff.add_enchantment(holy_enchant)
        self.assertTrue(success)
        
        # Test attack bonus (should include +4 bonus)
        attack_bonus = staff.get_attack_bonus(self.player)
        expected_attack = staff.attack_bonus + holy_enchant.get_weapon_attack_bonus() + 4
        self.assertEqual(attack_bonus, expected_attack)
        
        # Test health aspect bonus (should include +0.10 bonus)
        health_bonus = staff.get_health_aspect_bonus(self.player)
        expected_health = staff.health_aspect_bonus + holy_enchant.get_health_aspect_bonus() + 0.10
        self.assertEqual(health_bonus, expected_health)
    
    def test_clerics_staff_other_enchantments(self):
        """Test that other enchantments work normally on Cleric's Staff."""
        staff = ClericsStaff(0, 0)
        quality_enchant = get_weapon_enchantment_by_type(EnchantmentType.QUALITY)
        
        # Add the enchantment
        success = staff.add_enchantment(quality_enchant)
        self.assertTrue(success)
        
        # Test attack bonus (should be normal quality bonus only)
        attack_bonus = staff.get_attack_bonus(self.player)
        expected_attack = staff.attack_bonus + quality_enchant.get_weapon_attack_bonus()
        self.assertEqual(attack_bonus, expected_attack)
    
    def test_regular_weapon_no_override(self):
        """Test that regular weapons don't get special bonuses."""
        from items.weapons.sword import Sword
        
        sword = Sword(0, 0)
        blessed_enchant = get_weapon_enchantment_by_type(EnchantmentType.BLESSED)
        
        # Add the enchantment
        success = sword.add_enchantment(blessed_enchant)
        self.assertTrue(success)
        
        # Test attack bonus (should be normal blessed bonus only)
        attack_bonus = sword.get_attack_bonus(self.player)
        expected_attack = sword.attack_bonus + blessed_enchant.get_weapon_attack_bonus()
        self.assertEqual(attack_bonus, expected_attack)
    
    def test_armor_enchantment_bonuses(self):
        """Test that armor enchantments work correctly."""
        armor = Armor(0, 0, "Test Armor", '[', 2)
        quality_enchant = get_armor_enchantment_by_type(EnchantmentType.QUALITY)
        
        # Add the enchantment
        success = armor.add_enchantment(quality_enchant)
        self.assertTrue(success)
        
        # Test defense bonus
        defense_bonus = armor.get_defense_bonus(self.player)
        expected_defense = armor.defense_bonus + quality_enchant.get_armor_defense_bonus()
        self.assertEqual(defense_bonus, expected_defense)
    
    def test_armor_balanced_enchantment(self):
        """Test that BALANCED enchantment gives attack bonus to armor."""
        armor = Armor(0, 0, "Test Armor", '[', 2)
        balanced_enchant = get_armor_enchantment_by_type(EnchantmentType.BALANCED)
        
        # Add the enchantment
        success = armor.add_enchantment(balanced_enchant)
        self.assertTrue(success)
        
        # Test attack bonus (spiked armor should give +1 attack)
        attack_bonus = armor.get_attack_bonus(self.player)
        expected_attack = armor.attack_bonus + balanced_enchant.get_armor_attack_bonus()
        self.assertEqual(attack_bonus, expected_attack)
        self.assertEqual(expected_attack, 1)  # Should be +1 from spiked


if __name__ == '__main__':
    unittest.main()