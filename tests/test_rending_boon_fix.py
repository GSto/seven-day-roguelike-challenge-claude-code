"""Test that Rending Boon correctly applies crit percentage boost."""

import unittest
from src.player import Player
from src.items.weapons import Sword
from src.items.consumables import ReapersBoon
from src.items.enchantments import EnchantmentType


class TestRendingBoonFix(unittest.TestCase):
    """Test the Rending Boon crit bonus functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.player = Player(5, 5)
        self.player.xp = 100  # Enough XP to equip weapon
        
    def test_rending_boon_applies_crit_bonus(self):
        """Test that Rending Boon correctly increases crit chance."""
        # Equip a weapon
        weapon = Sword(0, 0)
        self.player.weapon = weapon
        
        # Record initial crit chance
        initial_crit = self.player.get_total_crit()
        
        # Use Reaper's Boon to apply Rending enchantment
        boon = ReapersBoon(0, 0)
        success, message = boon.use(self.player)
        
        # Verify boon was applied successfully
        self.assertTrue(success)
        self.assertIn("Rending", message)
        
        # Verify weapon has the enchantment
        self.assertEqual(len(self.player.weapon.enchantments), 1)
        enchantment = self.player.weapon.enchantments[0]
        self.assertEqual(enchantment.type, EnchantmentType.RENDING)
        
        # Verify crit chance increased by 5%
        final_crit = self.player.get_total_crit()
        expected_crit = initial_crit + 0.05
        
        self.assertAlmostEqual(final_crit, expected_crit, places=3)
        self.assertGreater(final_crit, initial_crit)
    
    def test_rending_enchantment_provides_crit_bonus(self):
        """Test that Rending enchantment directly provides the correct crit bonus."""
        # Equip a weapon
        weapon = Sword(0, 0)
        self.player.weapon = weapon
        
        # Add Rending enchantment directly
        from src.items.enchantments import get_enchantment_by_type
        rending = get_enchantment_by_type(EnchantmentType.RENDING)
        weapon.add_enchantment(rending)
        
        # Test that enchantment provides 0.05 crit bonus
        crit_bonus = rending.get_weapon_crit_bonus()
        self.assertEqual(crit_bonus, 0.05)
        
        # Test that weapon includes enchantment bonus
        weapon_crit_bonus = weapon.get_crit_bonus(self.player)
        self.assertEqual(weapon_crit_bonus, 0.05)  # Base 0 + enchantment 0.05
    
    def test_multiple_crit_sources_stack(self):
        """Test that crit bonuses from different sources stack correctly."""
        # Use a weapon with base crit bonus
        from src.items.weapons import Katana
        weapon = Katana(0, 0)  # Has 0.15 base crit bonus
        self.player.weapon = weapon
        
        initial_crit = self.player.get_total_crit()
        expected_base_crit = self.player.crit + 0.15  # Player base + weapon base
        self.assertAlmostEqual(initial_crit, expected_base_crit, places=3)
        
        # Apply Rending enchantment
        boon = ReapersBoon(0, 0)
        success, message = boon.use(self.player)
        self.assertTrue(success)
        
        # Verify both bonuses are applied
        final_crit = self.player.get_total_crit()
        expected_final_crit = self.player.crit + 0.15 + 0.05  # Player + weapon + enchantment
        self.assertAlmostEqual(final_crit, expected_final_crit, places=3)
    
    def test_rending_boon_fails_without_weapon(self):
        """Test that Rending Boon fails when no weapon is equipped."""
        # Ensure no weapon is equipped
        self.player.weapon = None
        
        # Try to use Reaper's Boon
        boon = ReapersBoon(0, 0)
        success, message = boon.use(self.player)
        
        # Should fail
        self.assertFalse(success)
        self.assertIn("weapon equipped", message)
    
    def test_crit_bonus_method_calls_include_enchantments(self):
        """Test that equipment bonus methods properly include enchantment bonuses."""
        # Create weapon with Rending enchantment
        weapon = Sword(0, 0)
        from src.items.enchantments import get_enchantment_by_type
        rending = get_enchantment_by_type(EnchantmentType.RENDING)
        weapon.add_enchantment(rending)
        
        self.player.weapon = weapon
        
        # Test that get_crit_bonus includes enchantments
        weapon_crit = weapon.get_crit_bonus(self.player)
        self.assertEqual(weapon_crit, 0.05)
        
        # Test that player's total crit includes weapon's enchantment bonus
        total_crit = self.player.get_total_crit()
        expected_crit = self.player.crit + 0.05
        self.assertAlmostEqual(total_crit, expected_crit, places=3)


if __name__ == '__main__':
    unittest.main()