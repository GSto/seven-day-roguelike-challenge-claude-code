#!/usr/bin/env python3

import unittest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from items.weapons.sword import Sword
from items.armor.leather_armor import LeatherArmor
from items.accessories.ring import Ring
from enchantments import get_weapon_enchantment_by_type, get_armor_enchantment_by_type, EnchantmentType


class TestEquipmentMarketValue(unittest.TestCase):
    """Test that equipment market value includes enchantment bonuses."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sword = Sword(0, 0)
        self.armor = LeatherArmor(0, 0) 
        self.ring = Ring(0, 0, "Test Ring")
    
    def test_base_equipment_market_value(self):
        """Test that base equipment returns default market value."""
        # All equipment should have a base market value
        self.assertGreater(self.sword.get_market_value(), 0)
        self.assertGreater(self.armor.get_market_value(), 0)
        self.assertGreater(self.ring.get_market_value(), 0)
        
        # Should equal the stored market_value for unenchanted equipment
        self.assertEqual(self.sword.get_market_value(), self.sword.market_value)
        self.assertEqual(self.armor.get_market_value(), self.armor.market_value)
        self.assertEqual(self.ring.get_market_value(), self.ring.market_value)
    
    def test_weapon_enchantment_increases_value(self):
        """Test that weapon enchantments increase market value by +10 each."""
        base_value = self.sword.get_market_value()
        
        # Add first enchantment
        quality_enchantment = get_weapon_enchantment_by_type(EnchantmentType.QUALITY)
        self.sword.add_enchantment(quality_enchantment)
        
        # Market value should increase by 10
        self.assertEqual(self.sword.get_market_value(), base_value + 10)
        
        # Add second enchantment
        blessed_enchantment = get_weapon_enchantment_by_type(EnchantmentType.BLESSED)
        self.sword.add_enchantment(blessed_enchantment)
        
        # Market value should increase by another 10 (total +20)
        self.assertEqual(self.sword.get_market_value(), base_value + 20)
    
    def test_armor_enchantment_increases_value(self):
        """Test that armor enchantments increase market value by +10 each."""
        base_value = self.armor.get_market_value()
        
        # Add first enchantment
        quality_enchantment = get_armor_enchantment_by_type(EnchantmentType.QUALITY)
        self.armor.add_enchantment(quality_enchantment)
        
        # Market value should increase by 10
        self.assertEqual(self.armor.get_market_value(), base_value + 10)
        
        # Add second enchantment
        blessed_enchantment = get_armor_enchantment_by_type(EnchantmentType.BLESSED)
        self.armor.add_enchantment(blessed_enchantment)
        
        # Market value should increase by another 10 (total +20)
        self.assertEqual(self.armor.get_market_value(), base_value + 20)
    
    def test_accessories_no_enchantment_bonus(self):
        """Test that accessories don't get enchantment bonuses (they don't have enchantments)."""
        base_value = self.ring.get_market_value()
        
        # Accessories don't have enchantments system, so value should remain the same
        # This test ensures accessories use the base get_market_value implementation
        self.assertEqual(self.ring.get_market_value(), base_value)
        
        # Verify accessories don't have enchantments attribute or it's empty
        if hasattr(self.ring, 'enchantments'):
            self.assertEqual(len(self.ring.enchantments), 0)
    
    def test_market_value_is_consistent(self):
        """Test that market value calculations are consistent."""
        # Create multiple instances and verify consistent behavior
        sword1 = Sword(0, 0)
        sword2 = Sword(0, 0)
        
        # Base values should be the same
        self.assertEqual(sword1.get_market_value(), sword2.get_market_value())
        
        # Add same enchantment to both
        enchantment1 = get_weapon_enchantment_by_type(EnchantmentType.QUALITY)
        enchantment2 = get_weapon_enchantment_by_type(EnchantmentType.QUALITY)
        
        sword1.add_enchantment(enchantment1)
        sword2.add_enchantment(enchantment2)
        
        # Values should still be the same
        self.assertEqual(sword1.get_market_value(), sword2.get_market_value())


if __name__ == '__main__':
    unittest.main()