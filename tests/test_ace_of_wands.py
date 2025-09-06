import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from player import Player
from event_emitter import EventEmitter
from event_type import EventType
from event_context import HealContext
from items.accessories.ace_of_wands import AceOfWands


class TestAceOfWands(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
        self.ace_of_wands = AceOfWands(0, 0)

    def tearDown(self):
        """Clean up after tests."""
        self.emitter.clear_all_listeners()

    def test_creation(self):
        """Test that AceOfWands is created correctly."""
        item = AceOfWands(1, 2)
        
        self.assertEqual(item.x, 1)
        self.assertEqual(item.y, 2)
        self.assertEqual(item.name, "Ace of Wands")
        self.assertEqual(item.char, "#")  # Card character
        self.assertEqual(item.color, (255, 255, 255))  # COLOR_WHITE from accessory base
        self.assertEqual(item.market_value, 45)
        self.assertIn(EventType.PLAYER_HEAL, item.event_subscriptions)

    def test_player_heal_grants_xp(self):
        """Test that player healing triggers XP gain."""
        # Record initial XP
        initial_xp = self.player.xp
        
        # Simulate a player heal event
        context = HealContext(
            player=self.player,
            amount_healed=20
        )
        
        self.ace_of_wands.on_event(EventType.PLAYER_HEAL, context)
        
        # Player should have gained 10 XP
        self.assertEqual(self.player.xp, initial_xp + 10)

    def test_multiple_heals_grant_multiple_xp(self):
        """Test that multiple heal events grant XP each time."""
        initial_xp = self.player.xp
        
        # Simulate multiple heal events
        for i in range(5):
            context = HealContext(
                player=self.player,
                amount_healed=15
            )
            self.ace_of_wands.on_event(EventType.PLAYER_HEAL, context)
        
        # Player should have gained 50 XP total (10 * 5)
        self.assertEqual(self.player.xp, initial_xp + 50)

    def test_different_heal_amounts_same_xp_bonus(self):
        """Test that XP bonus is independent of heal amount."""
        initial_xp = self.player.xp
        
        # Test different heal amounts
        heal_amounts = [1, 10, 50, 100]
        
        for heal_amount in heal_amounts:
            context = HealContext(
                player=self.player,
                amount_healed=heal_amount
            )
            self.ace_of_wands.on_event(EventType.PLAYER_HEAL, context)
        
        # Should have gained 40 XP total (10 * 4 heal events)
        self.assertEqual(self.player.xp, initial_xp + 40)

    def test_non_heal_events_ignored(self):
        """Test that non-heal events are ignored."""
        initial_xp = self.player.xp
        
        context = HealContext(
            player=self.player,
            amount_healed=25
        )
        
        # Try other event types - should be ignored
        self.ace_of_wands.on_event(EventType.PLAYER_CONSUME_ITEM, context)
        self.ace_of_wands.on_event(EventType.CRITICAL_HIT, context)
        self.ace_of_wands.on_event(EventType.LEVEL_UP, context)
        self.ace_of_wands.on_event(EventType.SUCCESSFUL_DODGE, context)
        
        # XP should remain unchanged
        self.assertEqual(self.player.xp, initial_xp)

    def test_wrong_context_type_ignored(self):
        """Test that events with wrong context types are ignored."""
        initial_xp = self.player.xp
        
        # Try with wrong context type
        self.ace_of_wands.on_event(EventType.PLAYER_HEAL, "not a heal context")
        self.ace_of_wands.on_event(EventType.PLAYER_HEAL, None)
        
        # XP should remain unchanged
        self.assertEqual(self.player.xp, initial_xp)

    def test_equipment_integration(self):
        """Test that the item works when equipped by the player."""
        # Add to an accessory slot manually (simulating equipment)
        self.player.accessories[0] = self.ace_of_wands
        
        # Verify it's in the accessory list
        equipped_accessories = list(self.player.equipped_accessories())
        self.assertIn(self.ace_of_wands, equipped_accessories)
        
        # Record initial XP
        initial_xp = self.player.xp
        
        # Simulate heal event
        context = HealContext(
            player=self.player,
            amount_healed=30
        )
        
        self.ace_of_wands.on_event(EventType.PLAYER_HEAL, context)
        
        # Verify XP was gained
        self.assertEqual(self.player.xp, initial_xp + 10)

    def test_zero_heal_amount_still_grants_xp(self):
        """Test that even zero heal amount triggers XP bonus."""
        initial_xp = self.player.xp
        
        # Simulate zero heal (e.g., healing at full health)
        context = HealContext(
            player=self.player,
            amount_healed=0
        )
        
        self.ace_of_wands.on_event(EventType.PLAYER_HEAL, context)
        
        # Should still grant XP because heal event occurred
        self.assertEqual(self.player.xp, initial_xp + 10)

    def test_level_up_interaction(self):
        """Test behavior when XP gain triggers level up."""
        # Set player close to level up (assuming level up at some XP threshold)
        initial_level = self.player.level
        
        # Give player XP to be very close to next level
        # This is implementation dependent - adjust if needed
        self.player.xp = self.player.xp_to_next - 5
        
        # Heal event that should trigger level up
        context = HealContext(
            player=self.player,
            amount_healed=50
        )
        
        self.ace_of_wands.on_event(EventType.PLAYER_HEAL, context)
        
        # Should have gained XP (whether it levels up depends on implementation)
        # The XP gain should be at least 10 (with possible multiplier)
        final_xp = self.player.xp
        expected_min_xp = (self.player.xp_to_next - 5) + 10  # Initial XP + 10 XP bonus
        self.assertGreaterEqual(final_xp, expected_min_xp)

    def test_card_inheritance(self):
        """Test that AceOfWands properly inherits from Card base class."""
        # Should have card-specific properties
        self.assertEqual(self.ace_of_wands.char, "#")
        
        # Should be an accessory type equipment
        self.assertEqual(self.ace_of_wands.equipment_slot, "accessory")


if __name__ == '__main__':
    unittest.main()