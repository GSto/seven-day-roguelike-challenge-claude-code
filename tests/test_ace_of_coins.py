import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from player import Player
from event_emitter import EventEmitter
from items.accessories.ace_of_coins import AceOfCoins


class TestAceOfCoins(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
        self.ace_of_coins = AceOfCoins(0, 0)

    def tearDown(self):
        """Clean up after tests."""
        self.emitter.clear_all_listeners()

    def test_creation(self):
        """Test that AceOfCoins is created correctly."""
        item = AceOfCoins(1, 2)
        
        self.assertEqual(item.x, 1)
        self.assertEqual(item.y, 2)
        self.assertEqual(item.name, "Ace of Coins")
        self.assertEqual(item.char, "#")  # Card character
        self.assertEqual(item.color, (255, 255, 255))  # COLOR_WHITE from accessory base
        self.assertEqual(item.market_value, 80)
        self.assertEqual(item.xp_multiplier_bonus, 1.2)  # +20% XP multiplier

    def test_xp_multiplier_bonus(self):
        """Test that XP multiplier bonus is correctly applied."""
        self.assertEqual(self.ace_of_coins.xp_multiplier_bonus, 1.2)
        
        # Test when equipped
        self.player.accessories[0] = self.ace_of_coins
        total_xp_multiplier = self.player.get_total_xp_multiplier()
        
        # Should multiply base XP multiplier by 1.2 (20% increase)
        # Base XP multiplier is 1.0, so total should be 1.0 * 1.2 = 1.2
        self.assertEqual(total_xp_multiplier, 1.2)

    def test_equipment_integration(self):
        """Test that the item works when equipped by the player."""
        # Record initial XP and multiplier
        initial_xp = self.player.xp
        base_xp_multiplier = self.player.get_total_xp_multiplier()
        
        # Add to an accessory slot manually (simulating equipment)
        self.player.accessories[0] = self.ace_of_coins
        
        # Verify it's in the accessory list
        equipped_accessories = list(self.player.equipped_accessories())
        self.assertIn(self.ace_of_coins, equipped_accessories)
        
        # Test XP multiplier is applied
        enhanced_xp_multiplier = self.player.get_total_xp_multiplier()
        self.assertEqual(enhanced_xp_multiplier, base_xp_multiplier * 1.2)

    def test_xp_gain_with_multiplier(self):
        """Test that XP gains are multiplied correctly when equipped."""
        # Equip the item
        self.player.accessories[0] = self.ace_of_coins
        
        # Record initial XP
        initial_xp = self.player.xp
        
        # Gain some XP
        self.player.gain_xp(100)
        
        # Should gain 100 * 1.2 = 120 XP total
        expected_xp = initial_xp + (100 * 1.2)
        self.assertEqual(self.player.xp, expected_xp)

    def test_multiple_xp_gains_with_multiplier(self):
        """Test multiple XP gains with the multiplier."""
        # Equip the item
        self.player.accessories[0] = self.ace_of_coins
        
        # Record initial XP
        initial_xp = self.player.xp
        
        # Multiple XP gains
        xp_amounts = [10, 25, 50, 15]
        total_base_xp = sum(xp_amounts)
        
        for xp_amount in xp_amounts:
            self.player.gain_xp(xp_amount)
        
        # Should gain total_base_xp * 1.2
        expected_xp = initial_xp + (total_base_xp * 1.2)
        self.assertEqual(self.player.xp, expected_xp)

    def test_no_other_bonuses(self):
        """Test that only XP multiplier bonus is provided."""
        # Should not have other bonuses
        self.assertEqual(self.ace_of_coins.attack_bonus, 0)
        self.assertEqual(self.ace_of_coins.defense_bonus, 0)
        self.assertEqual(self.ace_of_coins.fov_bonus, 0)
        self.assertEqual(self.ace_of_coins.evade_bonus, 0.0)
        self.assertEqual(self.ace_of_coins.crit_bonus, 0.0)
        self.assertEqual(self.ace_of_coins.crit_multiplier_bonus, 0.0)
        self.assertEqual(self.ace_of_coins.attack_multiplier_bonus, 1.0)
        self.assertEqual(self.ace_of_coins.defense_multiplier_bonus, 1.0)
        self.assertEqual(self.ace_of_coins.health_aspect_bonus, 0.0)

    def test_no_traits_or_resistances(self):
        """Test that the item has no attack traits or resistances."""
        self.assertEqual(len(self.ace_of_coins.attack_traits), 0)
        self.assertEqual(len(self.ace_of_coins.resistances), 0)
        self.assertEqual(len(self.ace_of_coins.weaknesses), 0)

    def test_accessory_inheritance(self):
        """Test that AceOfCoins properly inherits from Accessory base class."""
        # Should have card-style character
        self.assertEqual(self.ace_of_coins.char, "#")
        
        # Should be an accessory type equipment
        self.assertEqual(self.ace_of_coins.equipment_slot, "accessory")

    def test_xp_multiplier_stacks_with_other_bonuses(self):
        """Test that XP multiplier stacks with other equipment bonuses."""
        # Create another accessory with XP multiplier bonus (if any exist)
        # For now, just test with base player multiplier
        
        # Equip the item
        self.player.accessories[0] = self.ace_of_coins
        
        # Manually add additional XP multiplier to test stacking
        original_multiplier = self.player.xp_multiplier
        self.player.xp_multiplier = 1.1  # Simulate another 10% bonus
        
        # Total should be base (1.1) * equipment (1.2) = 1.32
        total_multiplier = self.player.get_total_xp_multiplier()
        self.assertAlmostEqual(total_multiplier, 1.32, places=6)
        
        # Restore original value
        self.player.xp_multiplier = original_multiplier

    def test_unequipped_no_bonus(self):
        """Test that XP multiplier bonus is not applied when unequipped."""
        # Don't equip the item
        initial_multiplier = self.player.get_total_xp_multiplier()
        
        # Gain XP
        initial_xp = self.player.xp
        self.player.gain_xp(100)
        
        # Should gain exactly 100 * base_multiplier (no bonus)
        expected_xp = initial_xp + (100 * initial_multiplier)
        self.assertEqual(self.player.xp, expected_xp)

    def test_equipment_slot_limitations(self):
        """Test that the item properly occupies accessory slots."""
        # Should start with empty accessory slots
        equipped = list(self.player.equipped_accessories())
        self.assertEqual(len(equipped), 0)
        
        # Equip the item in first slot
        self.player.accessories[0] = self.ace_of_coins
        equipped = list(self.player.equipped_accessories())
        self.assertEqual(len(equipped), 1)
        self.assertIn(self.ace_of_coins, equipped)
        
        # Should still be able to equip other accessories in remaining slots
        self.assertIsNone(self.player.accessories[1])
        self.assertIsNone(self.player.accessories[2])

    def test_high_market_value(self):
        """Test that the item has appropriately high market value."""
        # Should be worth more than common accessories due to powerful effect
        self.assertGreater(self.ace_of_coins.market_value, 60)  # Higher than uncommon range
        self.assertEqual(self.ace_of_coins.market_value, 80)


if __name__ == '__main__':
    unittest.main()