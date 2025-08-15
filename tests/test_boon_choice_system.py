#!/usr/bin/env python3
"""
Test the new boon choice system for weapons and armor.
"""

import unittest
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from items.consumables import BaronsBoon
from items.weapons import Sword
from items.armor import LeatherArmor
from player import Player


class TestBoonChoiceSystem(unittest.TestCase):
    """Test the boon choice system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.player = Player(5, 5)
        self.sword = Sword(0, 0)
        self.armor = LeatherArmor(0, 0)
    
    def test_weapon_only_eligible(self):
        """Test that boon applies to weapon when only weapon is eligible."""
        # Clear armor and equip only weapon
        self.player.armor = None
        self.player.weapon = self.sword
        
        boon = BaronsBoon(0, 0)
        success, message = boon.use(self.player)
        
        self.assertTrue(success)
        self.assertIn("shines with new power", message)
        self.assertEqual(len(self.player.weapon.enchantments), 1)
        self.assertEqual(self.player.weapon.enchantments[0].name, "refined")
    
    def test_armor_only_eligible(self):
        """Test that boon applies to armor when only armor is eligible."""
        # Clear weapon and equip only armor
        self.player.weapon = None
        self.player.armor = self.armor
        
        boon = BaronsBoon(0, 0)
        success, message = boon.use(self.player)
        
        self.assertTrue(success)
        self.assertIn("gleams with new protection", message)
        self.assertEqual(len(self.player.armor.enchantments), 1)
        self.assertEqual(self.player.armor.enchantments[0].name, "refined")
    
    def test_both_eligible_defaults_to_weapon(self):
        """Test that when both are eligible, weapon is chosen by default."""
        # Equip both weapon and armor
        self.player.weapon = self.sword
        self.player.armor = self.armor
        
        boon = BaronsBoon(0, 0)
        success, message = boon.use(self.player)
        
        self.assertTrue(success)
        self.assertIn("shines with new power", message)
        self.assertEqual(len(self.player.weapon.enchantments), 1)
        self.assertEqual(len(self.player.armor.enchantments), 0)
    
    def test_neither_eligible(self):
        """Test that boon fails when neither weapon nor armor can be enchanted."""
        # Clear both weapon and armor  
        self.player.weapon = None
        self.player.armor = None
        
        boon = BaronsBoon(0, 0)
        success, message = boon.use(self.player)
        
        self.assertFalse(success)
        self.assertIn("need equipped items", message)
    
    def test_weapon_full_enchantments(self):
        """Test that boon applies to armor when weapon is full."""
        from items.enchantments import EnchantmentType, get_weapon_enchantment_by_type
        
        # Equip both and fill weapon enchantments
        self.player.weapon = self.sword
        self.player.armor = self.armor
        
        # Add two enchantments to weapon
        enchant1 = get_weapon_enchantment_by_type(EnchantmentType.QUALITY)
        enchant2 = get_weapon_enchantment_by_type(EnchantmentType.GLOWING)
        self.sword.add_enchantment(enchant1)
        self.sword.add_enchantment(enchant2)
        
        boon = BaronsBoon(0, 0)
        success, message = boon.use(self.player)
        
        self.assertTrue(success)
        self.assertIn("gleams with new protection", message)
        self.assertEqual(len(self.player.weapon.enchantments), 2)  # Still full
        self.assertEqual(len(self.player.armor.enchantments), 1)   # Boon applied here
    
    def test_duplicate_enchantment_prevention(self):
        """Test that duplicate enchantments are prevented."""
        from items.enchantments import EnchantmentType, get_weapon_enchantment_by_type, get_armor_enchantment_by_type
        
        # Equip both weapon and armor, give both SHINY enchantment
        self.player.weapon = self.sword
        self.player.armor = self.armor
        
        weapon_enchant = get_weapon_enchantment_by_type(EnchantmentType.SHINY)
        armor_enchant = get_armor_enchantment_by_type(EnchantmentType.SHINY)
        self.sword.add_enchantment(weapon_enchant)
        self.armor.add_enchantment(armor_enchant)
        
        # Try to apply another SHINY via boon - should fail since both already have it
        boon = BaronsBoon(0, 0)
        success, message = boon.use(self.player)
        
        self.assertFalse(success)
        self.assertIn("need equipped items", message)
        self.assertEqual(len(self.player.weapon.enchantments), 1)
        self.assertEqual(len(self.player.armor.enchantments), 1)


if __name__ == '__main__':
    unittest.main()