import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from player import Player
from event_emitter import EventEmitter
from traits import Trait
from status_effects import StatusEffects
from items.accessories.ace_of_swords import AceOfSwords


class TestAceOfSwords(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
        self.ace_of_swords = AceOfSwords(0, 0)

    def tearDown(self):
        """Clean up after tests."""
        self.emitter.clear_all_listeners()

    def test_creation(self):
        """Test that AceOfSwords is created correctly."""
        item = AceOfSwords(1, 2)
        
        self.assertEqual(item.x, 1)
        self.assertEqual(item.y, 2)
        self.assertEqual(item.name, "Ace of Swords")
        self.assertEqual(item.char, "#")  # Card character
        self.assertEqual(item.color, (255, 255, 255))  # COLOR_WHITE from accessory base
        self.assertEqual(item.market_value, 65)
        self.assertEqual(item.fov_bonus, 5)
        self.assertIn(Trait.MYSTIC, item.resistances)

    def test_fov_bonus(self):
        """Test that FOV bonus is correctly applied."""
        self.assertEqual(self.ace_of_swords.fov_bonus, 5)
        
        # Test when equipped
        self.player.accessories[0] = self.ace_of_swords
        total_fov = self.player.get_total_fov()
        base_fov = self.player.fov
        
        # Should include the +5 FOV bonus
        self.assertEqual(total_fov, base_fov + 5)

    def test_mystic_resistance(self):
        """Test that the item provides resistance to mystic damage."""
        self.assertIn(Trait.MYSTIC, self.ace_of_swords.resistances)
        
        # Test when equipped - check that the item is in accessories list
        self.player.accessories[0] = self.ace_of_swords
        equipped_accessories = list(self.player.equipped_accessories())
        
        self.assertIn(self.ace_of_swords, equipped_accessories)
        # The actual resistance application depends on combat system implementation

    def test_blindness_immunity(self):
        """Test that the item provides immunity to blindness."""
        # Test the blocks_status_effect method
        self.assertTrue(self.ace_of_swords.blocks_status_effect("blinded"))
        self.assertFalse(self.ace_of_swords.blocks_status_effect("poisoned"))
        self.assertFalse(self.ace_of_swords.blocks_status_effect("stunned"))
        self.assertFalse(self.ace_of_swords.blocks_status_effect("burned"))

    def test_blindness_immunity_integration(self):
        """Test that blindness immunity works with the status effects system."""
        # Equip the item
        self.player.accessories[0] = self.ace_of_swords
        
        # Try to apply blindness
        success = self.player.status_effects.apply_status("blinded", 3, self.player)
        
        # Should be blocked by the accessory
        self.assertFalse(success)
        self.assertEqual(self.player.status_effects.blinded, 0)

    def test_other_status_effects_not_blocked(self):
        """Test that other status effects are not blocked."""
        # Equip the item
        self.player.accessories[0] = self.ace_of_swords
        
        # Try to apply other status effects
        poison_success = self.player.status_effects.apply_status("poison", 2, self.player)
        burn_success = self.player.status_effects.apply_status("burn", 1, self.player)
        stun_success = self.player.status_effects.apply_status("stun", 1, self.player)
        
        # Should not be blocked
        self.assertTrue(poison_success)
        self.assertTrue(burn_success)
        self.assertTrue(stun_success)
        
        self.assertEqual(self.player.status_effects.poison, 2)
        self.assertEqual(self.player.status_effects.burn, 1)
        self.assertEqual(self.player.status_effects.stun, 1)

    def test_equipment_integration(self):
        """Test that the item works when equipped by the player."""
        # Add to an accessory slot manually (simulating equipment)
        self.player.accessories[0] = self.ace_of_swords
        
        # Verify it's in the accessory list
        equipped_accessories = list(self.player.equipped_accessories())
        self.assertIn(self.ace_of_swords, equipped_accessories)
        
        # Test all bonuses are applied
        total_fov = self.player.get_total_fov()
        
        self.assertEqual(total_fov, self.player.fov + 5)

    def test_multiple_blindness_attempts(self):
        """Test multiple attempts to apply blindness are all blocked."""
        # Equip the item
        self.player.accessories[0] = self.ace_of_swords
        
        # Try multiple applications
        for i in range(5):
            success = self.player.status_effects.apply_status("blinded", 1, self.player)
            self.assertFalse(success)
            self.assertEqual(self.player.status_effects.blinded, 0)

    def test_accessory_inheritance(self):
        """Test that AceOfSwords properly inherits from Accessory base class."""
        # Should have card-style character
        self.assertEqual(self.ace_of_swords.char, "#")
        
        # Should be an accessory type equipment
        self.assertEqual(self.ace_of_swords.equipment_slot, "accessory")

    def test_no_other_trait_resistances(self):
        """Test that only mystic resistance is provided."""
        # Should only resist mystic, not other traits
        self.assertEqual(len(self.ace_of_swords.resistances), 1)
        self.assertEqual(self.ace_of_swords.resistances[0], Trait.MYSTIC)
        
        # Should not resist other traits
        self.assertNotIn(Trait.FIRE, self.ace_of_swords.resistances)
        self.assertNotIn(Trait.ICE, self.ace_of_swords.resistances)
        self.assertNotIn(Trait.DARK, self.ace_of_swords.resistances)
        self.assertNotIn(Trait.HOLY, self.ace_of_swords.resistances)

    def test_no_weaknesses(self):
        """Test that the item doesn't introduce any weaknesses."""
        # Should have an empty weaknesses list
        self.assertEqual(len(self.ace_of_swords.weaknesses), 0)

    def test_item_has_proper_resistances(self):
        """Test that the item has the correct resistance configuration."""
        # Should have mystic resistance
        self.assertIn(Trait.MYSTIC, self.ace_of_swords.resistances)
        
        # Should be equipped properly
        self.player.accessories[0] = self.ace_of_swords
        equipped = list(self.player.equipped_accessories())
        self.assertIn(self.ace_of_swords, equipped)
        
        # Resistance application will be tested through integration with the combat system


if __name__ == '__main__':
    unittest.main()