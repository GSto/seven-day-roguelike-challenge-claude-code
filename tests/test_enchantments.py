"""
Unit tests for the enchantment system.
"""

import unittest
from unittest.mock import patch
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enchantments import (
    EnchantmentType, Enchantment, get_random_enchantment, 
    get_enchantment_by_type, should_spawn_with_enchantment
)
from items.weapons.base import Weapon
from items.weapons.sword import Sword
from items.consumables.barons_boon import BaronsBoon
from items.consumables.jewelers_boon import JewelersBoon
from items.consumables.miners_boon import MinersBoon
from items.consumables.clerics_boon import ClericsBoon
from items.consumables.jokers_boon import JokersBoon
# WardensBoon appears to not exist in the new structure - will need investigation


class TestEnchantment(unittest.TestCase):
    """Test the Enchantment class."""
    
    def test_quality_enchantment(self):
        """Test Quality enchantment provides correct bonuses."""
        enchantment = Enchantment(EnchantmentType.QUALITY)
        self.assertEqual(enchantment.name, "Quality")
        self.assertEqual(enchantment.get_attack_bonus(), 3)
        self.assertEqual(enchantment.get_defense_bonus(), 0)
        self.assertEqual(enchantment.get_fov_bonus(), 0)
        self.assertEqual(enchantment.get_attack_multiplier_bonus(), 0.0)
        self.assertEqual(enchantment.get_xp_multiplier_bonus(), 0.0)
        self.assertEqual(enchantment.get_health_aspect_bonus(), 0.0)
    
    def test_shiny_enchantment(self):
        """Test Shiny enchantment provides correct bonuses."""
        enchantment = Enchantment(EnchantmentType.SHINY)
        self.assertEqual(enchantment.name, "Shiny")
        self.assertEqual(enchantment.get_attack_bonus(), 0)
        self.assertEqual(enchantment.get_attack_multiplier_bonus(), 0.25)
    
    def test_glowing_enchantment(self):
        """Test Glowing enchantment provides correct bonuses."""
        enchantment = Enchantment(EnchantmentType.GLOWING)
        self.assertEqual(enchantment.name, "Glowing")
        self.assertEqual(enchantment.get_fov_bonus(), 2)
    
    def test_gilded_enchantment(self):
        """Test Gilded enchantment provides correct bonuses."""
        enchantment = Enchantment(EnchantmentType.GILDED)
        self.assertEqual(enchantment.name, "Gilded")
        self.assertEqual(enchantment.get_xp_multiplier_bonus(), 0.05)
    
    def test_blessed_enchantment(self):
        """Test Blessed enchantment provides correct bonuses."""
        enchantment = Enchantment(EnchantmentType.BLESSED)
        self.assertEqual(enchantment.name, "Blessed")
        self.assertEqual(enchantment.get_health_aspect_bonus(), 0.05)
    
    def test_bolstered_enchantment(self):
        """Test Bolstered enchantment provides correct bonuses."""
        enchantment = Enchantment(EnchantmentType.BOLSTERED)
        self.assertEqual(enchantment.name, "Bolstered")
        self.assertEqual(enchantment.get_defense_bonus(), 1)


class TestWeaponEnchantments(unittest.TestCase):
    """Test weapon enchantment functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.weapon = Sword(10, 10)
        self.original_attack = self.weapon.attack_bonus
    
    def test_weapon_starts_with_no_enchantments(self):
        """Test weapon starts with empty enchantments list."""
        self.assertEqual(len(self.weapon.enchantments), 0)
        self.assertEqual(self.weapon.name, "Sword")
        self.assertEqual(self.weapon.base_name, "Sword")
    
    def test_add_quality_enchantment(self):
        """Test adding Quality enchantment to weapon."""
        enchantment = Enchantment(EnchantmentType.QUALITY)
        result = self.weapon.add_enchantment(enchantment)
        
        self.assertTrue(result)
        self.assertEqual(len(self.weapon.enchantments), 1)
        self.assertEqual(self.weapon.name, "Quality Sword")
        self.assertEqual(self.weapon.attack_bonus, self.original_attack + 3)
    
    def test_add_multiple_enchantments(self):
        """Test adding multiple enchantments to weapon."""
        quality_enchantment = Enchantment(EnchantmentType.QUALITY)
        glowing_enchantment = Enchantment(EnchantmentType.GLOWING)
        
        result1 = self.weapon.add_enchantment(quality_enchantment)
        result2 = self.weapon.add_enchantment(glowing_enchantment)
        
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertEqual(len(self.weapon.enchantments), 2)
        self.assertEqual(self.weapon.name, "Quality Glowing Sword")
        self.assertEqual(self.weapon.attack_bonus, self.original_attack + 3)
        self.assertEqual(self.weapon.fov_bonus, 2)
    
    def test_cannot_add_more_than_two_enchantments(self):
        """Test weapon cannot have more than 2 enchantments."""
        enchantments = [
            Enchantment(EnchantmentType.QUALITY),
            Enchantment(EnchantmentType.GLOWING),
            Enchantment(EnchantmentType.SHINY)
        ]
        
        result1 = self.weapon.add_enchantment(enchantments[0])
        result2 = self.weapon.add_enchantment(enchantments[1])
        result3 = self.weapon.add_enchantment(enchantments[2])
        
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertFalse(result3)
        self.assertEqual(len(self.weapon.enchantments), 2)
    
    def test_cannot_add_duplicate_enchantment_type(self):
        """Test weapon cannot have duplicate enchantment types."""
        enchantment1 = Enchantment(EnchantmentType.QUALITY)
        enchantment2 = Enchantment(EnchantmentType.QUALITY)
        
        result1 = self.weapon.add_enchantment(enchantment1)
        result2 = self.weapon.add_enchantment(enchantment2)
        
        self.assertTrue(result1)
        self.assertFalse(result2)
        self.assertEqual(len(self.weapon.enchantments), 1)


class TestEnchantmentFunctions(unittest.TestCase):
    """Test enchantment utility functions."""
    
    def test_get_enchantment_by_type(self):
        """Test getting enchantment by specific type."""
        enchantment = get_enchantment_by_type(EnchantmentType.SHINY)
        self.assertEqual(enchantment.type, EnchantmentType.SHINY)
        self.assertEqual(enchantment.name, "Shiny")
    
    def test_get_random_enchantment(self):
        """Test getting random enchantment."""
        enchantment = get_random_enchantment()
        self.assertIn(enchantment.type, list(EnchantmentType))
        self.assertIsInstance(enchantment, Enchantment)
    
    @patch('items.enchantments.random.random', return_value=0.1)
    def test_should_spawn_with_enchantment_true(self, mock_random):
        """Test 25% chance returns True when random < 0.25."""
        result = should_spawn_with_enchantment()
        self.assertTrue(result)
    
    @patch('items.enchantments.random.random', return_value=0.5)
    def test_should_spawn_with_enchantment_false(self, mock_random):
        """Test 25% chance returns False when random >= 0.25."""
        result = should_spawn_with_enchantment()
        self.assertFalse(result)


class TestEnchantmentBoons(unittest.TestCase):
    """Test enchantment boon consumables."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock player with equipped weapon
        self.player = type('MockPlayer', (), {})()
        self.weapon = Sword(10, 10)
        self.player.weapon = self.weapon
    
    def test_barons_boon_applies_shiny_enchantment(self):
        """Test Baron's Boon applies Shiny enchantment."""
        boon = BaronsBoon(5, 5)
        original_multiplier = self.weapon.attack_multiplier_bonus
        
        success, message = boon.use(self.player)
        
        self.assertTrue(success)
        self.assertIn("shines with new power", message)
        self.assertEqual(len(self.weapon.enchantments), 1)
        self.assertEqual(self.weapon.enchantments[0].type, EnchantmentType.SHINY)
        self.assertEqual(self.weapon.attack_multiplier_bonus, original_multiplier + 0.25)
    
    def test_jewelers_boon_applies_gilded_enchantment(self):
        """Test Jeweler's Boon applies Gilded enchantment."""
        boon = JewelersBoon(5, 5)
        original_xp_multiplier = self.weapon.xp_multiplier_bonus
        
        success, message = boon.use(self.player)
        
        self.assertTrue(success)
        self.assertIn("gleams with golden light", message)
        self.assertEqual(len(self.weapon.enchantments), 1)
        self.assertEqual(self.weapon.enchantments[0].type, EnchantmentType.GILDED)
        self.assertEqual(self.weapon.xp_multiplier_bonus, original_xp_multiplier + 0.05)
    
    def test_miners_boon_applies_glowing_enchantment(self):
        """Test Miner's Boon applies Glowing enchantment."""
        boon = MinersBoon(5, 5)
        original_fov = self.weapon.fov_bonus
        
        success, message = boon.use(self.player)
        
        self.assertTrue(success)
        self.assertIn("begins to glow softly", message)
        self.assertEqual(len(self.weapon.enchantments), 1)
        self.assertEqual(self.weapon.enchantments[0].type, EnchantmentType.GLOWING)
        self.assertEqual(self.weapon.fov_bonus, original_fov + 2)
    
    def test_clerics_boon_applies_blessed_enchantment(self):
        """Test Cleric's Boon applies Blessed enchantment."""
        boon = ClericsBoon(5, 5)
        original_health_aspect = self.weapon.health_aspect_bonus
        
        success, message = boon.use(self.player)
        
        self.assertTrue(success)
        self.assertIn("blessed with divine power", message)
        self.assertEqual(len(self.weapon.enchantments), 1)
        self.assertEqual(self.weapon.enchantments[0].type, EnchantmentType.BLESSED)
        self.assertEqual(self.weapon.health_aspect_bonus, original_health_aspect + 0.05)
    
    def test_wardens_boon_applies_bolstered_enchantment(self):
        """Test Warden's Boon applies Bolstered enchantment."""
        boon = WardensBoon(5, 5)
        original_defense = self.weapon.defense_bonus
        
        success, message = boon.use(self.player)
        
        self.assertTrue(success)
        self.assertIn("feels more solid and protective", message)
        self.assertEqual(len(self.weapon.enchantments), 1)
        self.assertEqual(self.weapon.enchantments[0].type, EnchantmentType.BOLSTERED)
        self.assertEqual(self.weapon.defense_bonus, original_defense + 1)
    
    def test_jokers_boon_applies_random_enchantment(self):
        """Test Joker's Boon applies a random enchantment."""
        boon = JokersBoon(5, 5)
        
        success, message = boon.use(self.player)
        
        self.assertTrue(success)
        self.assertIn("is enchanted with", message)
        self.assertIn("power!", message)
        self.assertEqual(len(self.weapon.enchantments), 1)
        self.assertIn(self.weapon.enchantments[0].type, list(EnchantmentType))
    
    def test_boon_fails_without_equipped_weapon(self):
        """Test boon fails when player has no equipped weapon."""
        boon = BaronsBoon(5, 5)
        self.player.weapon = None  # Remove the weapon
        
        success, message = boon.use(self.player)
        
        self.assertFalse(success)
        self.assertEqual(message, "You need to have a weapon equipped to use this!")
    
    def test_boon_fails_on_fully_enchanted_weapon(self):
        """Test boon fails when weapon already has 2 enchantments."""
        boon = BaronsBoon(5, 5)
        
        # Add 2 enchantments to fill up the weapon
        self.weapon.add_enchantment(Enchantment(EnchantmentType.QUALITY))
        self.weapon.add_enchantment(Enchantment(EnchantmentType.GLOWING))
        
        success, message = boon.use(self.player)
        
        self.assertFalse(success)
        self.assertIn("cannot be further enhanced", message)


if __name__ == '__main__':
    unittest.main()