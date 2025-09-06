import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from player import Player
from event_emitter import EventEmitter
from event_type import EventType
from event_context import ConsumeContext
from items.accessories.ace_of_cups import AceOfCups
from items.consumables.health_potion import HealthPotion


class TestAceOfCups(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
        self.ace_of_cups = AceOfCups(0, 0)
        
        # Set player to have some damage so healing is visible
        self.player.take_damage(20)

    def tearDown(self):
        """Clean up after tests."""
        self.emitter.clear_all_listeners()

    def test_creation(self):
        """Test that AceOfCups is created correctly."""
        item = AceOfCups(1, 2)
        
        self.assertEqual(item.x, 1)
        self.assertEqual(item.y, 2)
        self.assertEqual(item.name, "Ace of Cups")
        self.assertEqual(item.char, "#")  # Card character
        self.assertEqual(item.color, (255, 255, 255))  # COLOR_WHITE from accessory base
        self.assertEqual(item.market_value, 50)
        self.assertIn(EventType.PLAYER_CONSUME_ITEM, item.event_subscriptions)

    def test_player_consume_item_heals_hp(self):
        """Test that player consuming item triggers healing."""
        # Record initial HP
        initial_hp = self.player.hp
        
        # Create a mock consumable item
        health_potion = HealthPotion(0, 0)
        
        # Simulate a player consume item event
        context = ConsumeContext(
            player=self.player,
            item_type="health_potion",
            item=health_potion
        )
        
        self.ace_of_cups.on_event(EventType.PLAYER_CONSUME_ITEM, context)
        
        # Player should have gained exactly 5 HP
        self.assertEqual(self.player.hp, initial_hp + 5)

    def test_multiple_consumptions_heal_multiple_times(self):
        """Test that multiple consume events heal each time."""
        initial_hp = self.player.hp
        
        # Simulate multiple consume events
        for i in range(3):
            health_potion = HealthPotion(0, 0)
            context = ConsumeContext(
                player=self.player,
                item_type="health_potion",
                item=health_potion
            )
            self.ace_of_cups.on_event(EventType.PLAYER_CONSUME_ITEM, context)
        
        # Player should have gained 15 HP total (5 * 3)
        self.assertEqual(self.player.hp, initial_hp + 15)

    def test_different_consumable_types_all_heal(self):
        """Test that different types of consumables all trigger healing."""
        # Set player to lower HP to ensure we don't hit max HP
        self.player.take_damage(30)  # Now at 20 HP (50 - 20 - 10 more = 20)
        initial_hp = self.player.hp
        
        # Test different consumable types
        consumable_types = ["health_potion", "food", "catalyst", "boon"]
        
        for consumable_type in consumable_types:
            context = ConsumeContext(
                player=self.player,
                item_type=consumable_type,
                item=None  # Item can be None
            )
            self.ace_of_cups.on_event(EventType.PLAYER_CONSUME_ITEM, context)
        
        # Should have gained 20 HP total (5 * 4 consume events)
        self.assertEqual(self.player.hp, initial_hp + 20)

    def test_healing_respects_max_hp(self):
        """Test that healing doesn't exceed max HP."""
        # Set player to near max HP
        self.player.hp = self.player.max_hp - 2
        initial_hp = self.player.hp
        
        context = ConsumeContext(
            player=self.player,
            item_type="health_potion",
            item=None
        )
        
        self.ace_of_cups.on_event(EventType.PLAYER_CONSUME_ITEM, context)
        
        # Should not exceed max HP
        self.assertLessEqual(self.player.hp, self.player.max_hp)
        self.assertGreater(self.player.hp, initial_hp)  # But should have increased

    def test_healing_at_full_hp(self):
        """Test behavior when player is at full HP."""
        # Set player to full HP
        self.player.hp = self.player.max_hp
        initial_hp = self.player.hp
        
        context = ConsumeContext(
            player=self.player,
            item_type="health_potion",
            item=None
        )
        
        self.ace_of_cups.on_event(EventType.PLAYER_CONSUME_ITEM, context)
        
        # HP should remain at max
        self.assertEqual(self.player.hp, self.player.max_hp)
        self.assertEqual(self.player.hp, initial_hp)

    def test_non_consume_events_ignored(self):
        """Test that non-consume events are ignored."""
        initial_hp = self.player.hp
        
        context = ConsumeContext(
            player=self.player,
            item_type="health_potion",
            item=None
        )
        
        # Try other event types - should be ignored
        self.ace_of_cups.on_event(EventType.PLAYER_HEAL, context)
        self.ace_of_cups.on_event(EventType.CRITICAL_HIT, context)
        self.ace_of_cups.on_event(EventType.LEVEL_UP, context)
        self.ace_of_cups.on_event(EventType.SUCCESSFUL_DODGE, context)
        
        # HP should remain unchanged
        self.assertEqual(self.player.hp, initial_hp)

    def test_wrong_context_type_ignored(self):
        """Test that events with wrong context types are ignored."""
        initial_hp = self.player.hp
        
        # Try with wrong context type
        self.ace_of_cups.on_event(EventType.PLAYER_CONSUME_ITEM, "not a consume context")
        self.ace_of_cups.on_event(EventType.PLAYER_CONSUME_ITEM, None)
        
        # HP should remain unchanged
        self.assertEqual(self.player.hp, initial_hp)

    def test_equipment_integration(self):
        """Test that the item works when equipped by the player."""
        # Add to an accessory slot manually (simulating equipment)
        self.player.accessories[0] = self.ace_of_cups
        
        # Verify it's in the accessory list
        equipped_accessories = list(self.player.equipped_accessories())
        self.assertIn(self.ace_of_cups, equipped_accessories)
        
        # Record initial HP
        initial_hp = self.player.hp
        
        # Simulate consume event
        context = ConsumeContext(
            player=self.player,
            item_type="health_potion",
            item=None
        )
        
        self.ace_of_cups.on_event(EventType.PLAYER_CONSUME_ITEM, context)
        
        # Verify healing occurred
        self.assertEqual(self.player.hp, initial_hp + 5)

    def test_healing_ignores_health_aspect_bonus(self):
        """Test that healing ignores health aspect bonuses and always heals 5 HP."""
        # Manually set a health aspect bonus for testing
        original_health_aspect = self.player.health_aspect
        self.player.health_aspect = 2.0  # 200% healing bonus
        
        initial_hp = self.player.hp
        
        context = ConsumeContext(
            player=self.player,
            item_type="health_potion",
            item=None
        )
        
        self.ace_of_cups.on_event(EventType.PLAYER_CONSUME_ITEM, context)
        
        # Should heal exactly 5 HP regardless of health aspect
        self.assertEqual(self.player.hp, initial_hp + 5)
        
        # Restore original value
        self.player.health_aspect = original_health_aspect

    def test_card_inheritance(self):
        """Test that AceOfCups properly inherits from Card base class."""
        # Should have card-specific properties
        self.assertEqual(self.ace_of_cups.char, "#")
        
        # Should be an accessory type equipment
        self.assertEqual(self.ace_of_cups.equipment_slot, "accessory")

    def test_empty_item_context_still_heals(self):
        """Test that healing occurs even when item is None in context."""
        initial_hp = self.player.hp
        
        # Context with no specific item
        context = ConsumeContext(
            player=self.player,
            item_type="unknown",
            item=None
        )
        
        self.ace_of_cups.on_event(EventType.PLAYER_CONSUME_ITEM, context)
        
        # Should still heal exactly 5 HP
        self.assertEqual(self.player.hp, initial_hp + 5)


if __name__ == '__main__':
    unittest.main()