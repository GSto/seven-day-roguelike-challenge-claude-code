"""
Unit tests for the Event System implementation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import MagicMock
from event_emitter import EventEmitter
from event_type import EventType
from event_context import EventContext, HealContext, ConsumeContext, AttackContext, DeathContext, LevelUpContext, FloorContext
from player import Player

class TestEventEmitter(unittest.TestCase):
    
    def setUp(self):
        # Reset singleton instance for each test
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
    
    def tearDown(self):
        # Clear all listeners after each test
        self.emitter.clear_all_listeners()
        EventEmitter._instance = None
    
    def test_singleton_pattern(self):
        """Test that EventEmitter follows singleton pattern."""
        emitter1 = EventEmitter()
        emitter2 = EventEmitter()
        self.assertIs(emitter1, emitter2)
    
    def test_subscribe_and_emit(self):
        """Test basic subscription and emission."""
        callback = MagicMock()
        context = EventContext(player=self.player)
        
        self.emitter.subscribe(EventType.PLAYER_HEAL, callback)
        self.emitter.emit(EventType.PLAYER_HEAL, context)
        
        callback.assert_called_once_with(EventType.PLAYER_HEAL, context)
    
    def test_unsubscribe(self):
        """Test unsubscribing from events."""
        callback = MagicMock()
        context = EventContext(player=self.player)
        
        self.emitter.subscribe(EventType.PLAYER_HEAL, callback)
        self.emitter.unsubscribe(EventType.PLAYER_HEAL, callback)
        self.emitter.emit(EventType.PLAYER_HEAL, context)
        
        callback.assert_not_called()
    
    def test_multiple_listeners(self):
        """Test multiple listeners for the same event."""
        callback1 = MagicMock()
        callback2 = MagicMock()
        context = EventContext(player=self.player)
        
        self.emitter.subscribe(EventType.PLAYER_HEAL, callback1)
        self.emitter.subscribe(EventType.PLAYER_HEAL, callback2)
        self.emitter.emit(EventType.PLAYER_HEAL, context)
        
        callback1.assert_called_once_with(EventType.PLAYER_HEAL, context)
        callback2.assert_called_once_with(EventType.PLAYER_HEAL, context)
    
    def test_no_listeners(self):
        """Test emitting events with no listeners."""
        context = EventContext(player=self.player)
        # Should not raise any exceptions
        self.emitter.emit(EventType.PLAYER_HEAL, context)
    
    def test_get_listener_count(self):
        """Test getting listener count."""
        callback1 = MagicMock()
        callback2 = MagicMock()
        
        self.assertEqual(self.emitter.get_listener_count(), 0)
        
        self.emitter.subscribe(EventType.PLAYER_HEAL, callback1)
        self.assertEqual(self.emitter.get_listener_count(EventType.PLAYER_HEAL), 1)
        self.assertEqual(self.emitter.get_listener_count(), 1)
        
        self.emitter.subscribe(EventType.MONSTER_DEATH, callback2)
        self.assertEqual(self.emitter.get_listener_count(EventType.MONSTER_DEATH), 1)
        self.assertEqual(self.emitter.get_listener_count(), 2)
    
    def test_clear_all_listeners(self):
        """Test clearing all listeners."""
        callback1 = MagicMock()
        callback2 = MagicMock()
        
        self.emitter.subscribe(EventType.PLAYER_HEAL, callback1)
        self.emitter.subscribe(EventType.MONSTER_DEATH, callback2)
        
        self.emitter.clear_all_listeners()
        self.assertEqual(self.emitter.get_listener_count(), 0)
    
    def test_debug_mode(self):
        """Test debug mode functionality."""
        self.emitter.set_debug_mode(True)
        callback = MagicMock()
        context = EventContext(player=self.player)
        
        self.emitter.subscribe(EventType.PLAYER_HEAL, callback)
        # This should print debug messages (manual verification)
        self.emitter.emit(EventType.PLAYER_HEAL, context)
        
        callback.assert_called_once()
        self.emitter.set_debug_mode(False)


class TestEventContexts(unittest.TestCase):
    
    def setUp(self):
        self.player = Player(5, 5)
    
    def test_heal_context(self):
        """Test HealContext creation and attributes."""
        context = HealContext(player=self.player, amount_healed=10)
        
        self.assertEqual(context.player, self.player)
        self.assertEqual(context.amount_healed, 10)
        self.assertIsInstance(context.timestamp, float)
    
    def test_consume_context(self):
        """Test ConsumeContext creation and attributes."""
        from items.consumables.health_potion import HealthPotion
        potion = HealthPotion(0, 0)
        
        context = ConsumeContext(player=self.player, item_type="HealthPotion", item=potion)
        
        self.assertEqual(context.player, self.player)
        self.assertEqual(context.item_type, "HealthPotion")
        self.assertEqual(context.item, potion)
    
    def test_attack_context(self):
        """Test AttackContext creation and attributes."""
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        
        context = AttackContext(
            player=self.player,
            attacker=self.player,
            defender=goblin,
            damage=15,
            is_critical=True,
            is_miss=False,
            trait_interaction="weakness"
        )
        
        self.assertEqual(context.player, self.player)
        self.assertEqual(context.attacker, self.player)
        self.assertEqual(context.defender, goblin)
        self.assertEqual(context.damage, 15)
        self.assertTrue(context.is_critical)
        self.assertFalse(context.is_miss)
        self.assertEqual(context.trait_interaction, "weakness")
    
    def test_death_context(self):
        """Test DeathContext creation and attributes."""
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        
        context = DeathContext(player=self.player, monster=goblin, experience_gained=25)
        
        self.assertEqual(context.player, self.player)
        self.assertEqual(context.monster, goblin)
        self.assertEqual(context.experience_gained, 25)
    
    def test_level_up_context(self):
        """Test LevelUpContext creation and attributes."""
        stat_increases = {"attack": 1, "max_hp": 10}
        
        context = LevelUpContext(player=self.player, new_level=3, stat_increases=stat_increases)
        
        self.assertEqual(context.player, self.player)
        self.assertEqual(context.new_level, 3)
        self.assertEqual(context.stat_increases, stat_increases)
    
    def test_floor_context(self):
        """Test FloorContext creation and attributes."""
        context = FloorContext(player=self.player, floor_number=5, previous_floor=4)
        
        self.assertEqual(context.player, self.player)
        self.assertEqual(context.floor_number, 5)
        self.assertEqual(context.previous_floor, 4)


class TestEventSystemIntegration(unittest.TestCase):
    """Integration tests to verify events are emitted correctly."""
    
    def setUp(self):
        # Reset singleton
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
        self.callback = MagicMock()
    
    def tearDown(self):
        self.emitter.clear_all_listeners()
        EventEmitter._instance = None
    
    def test_player_heal_event(self):
        """Test that healing emits PLAYER_HEAL event."""
        self.emitter.subscribe(EventType.PLAYER_HEAL, self.callback)
        
        # Damage player first so heal has effect
        self.player.hp = 30
        self.player.heal(10)
        
        self.callback.assert_called_once()
        call_args = self.callback.call_args[0]
        self.assertEqual(call_args[0], EventType.PLAYER_HEAL)
        self.assertIsInstance(call_args[1], HealContext)
        self.assertEqual(call_args[1].amount_healed, 10)
    
    def test_player_level_up_event(self):
        """Test that leveling up emits LEVEL_UP event."""
        self.emitter.subscribe(EventType.LEVEL_UP, self.callback)
        
        self.player.level_up()
        
        self.callback.assert_called_once()
        call_args = self.callback.call_args[0]
        self.assertEqual(call_args[0], EventType.LEVEL_UP)
        self.assertIsInstance(call_args[1], LevelUpContext)
        self.assertEqual(call_args[1].new_level, 2)
    
    def test_no_heal_event_when_full_health(self):
        """Test that no heal event is emitted when player is at full health."""
        self.emitter.subscribe(EventType.PLAYER_HEAL, self.callback)
        
        # Player starts at full health
        self.player.heal(10)
        
        # No event should be emitted since no actual healing occurred
        self.callback.assert_not_called()


class TestEquipmentEventHandling(unittest.TestCase):
    """Test equipment event handling functionality."""
    
    def setUp(self):
        # Reset singleton
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
        self.callback = MagicMock()
    
    def tearDown(self):
        self.emitter.clear_all_listeners()
        EventEmitter._instance = None
    
    def create_test_equipment(self, subscribed_events):
        """Create a test equipment that subscribes to specific events."""
        from items.equipment import Equipment
        
        class TestEquipment(Equipment):
            def __init__(self):
                super().__init__(0, 0, "Test Equipment", "T", (255, 255, 255))
                self.event_subscriptions = subscribed_events
                self.event_calls = []
            
            def on_event(self, event_type, context):
                self.event_calls.append((event_type, context))
        
        return TestEquipment()
    
    def test_equipment_event_subscription(self):
        """Test that equipment can subscribe to events."""
        test_equipment = self.create_test_equipment({EventType.PLAYER_HEAL})
        
        # Simulate equipping
        self.emitter.subscribe(EventType.PLAYER_HEAL, test_equipment.on_event)
        
        # Emit event
        context = HealContext(player=self.player, amount_healed=10)
        self.emitter.emit(EventType.PLAYER_HEAL, context)
        
        # Check that equipment received the event
        self.assertEqual(len(test_equipment.event_calls), 1)
        self.assertEqual(test_equipment.event_calls[0][0], EventType.PLAYER_HEAL)
        self.assertEqual(test_equipment.event_calls[0][1].amount_healed, 10)
    
    def test_equipment_multiple_event_subscription(self):
        """Test that equipment can subscribe to multiple events."""
        test_equipment = self.create_test_equipment({EventType.PLAYER_HEAL, EventType.MONSTER_DEATH})
        
        # Simulate equipping
        self.emitter.subscribe(EventType.PLAYER_HEAL, test_equipment.on_event)
        self.emitter.subscribe(EventType.MONSTER_DEATH, test_equipment.on_event)
        
        # Emit both events
        heal_context = HealContext(player=self.player, amount_healed=10)
        self.emitter.emit(EventType.PLAYER_HEAL, heal_context)
        
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        death_context = DeathContext(player=self.player, monster=goblin, experience_gained=25)
        self.emitter.emit(EventType.MONSTER_DEATH, death_context)
        
        # Check that equipment received both events
        self.assertEqual(len(test_equipment.event_calls), 2)
        event_types = [call[0] for call in test_equipment.event_calls]
        self.assertIn(EventType.PLAYER_HEAL, event_types)
        self.assertIn(EventType.MONSTER_DEATH, event_types)
    
    def test_equipment_unsubscription(self):
        """Test that equipment can unsubscribe from events."""
        test_equipment = self.create_test_equipment({EventType.PLAYER_HEAL})
        
        # Simulate equipping and unequipping
        self.emitter.subscribe(EventType.PLAYER_HEAL, test_equipment.on_event)
        self.emitter.unsubscribe(EventType.PLAYER_HEAL, test_equipment.on_event)
        
        # Emit event
        context = HealContext(player=self.player, amount_healed=10)
        self.emitter.emit(EventType.PLAYER_HEAL, context)
        
        # Check that equipment did not receive the event
        self.assertEqual(len(test_equipment.event_calls), 0)
    
    def test_get_subscribed_events(self):
        """Test that equipment returns correct subscribed events."""
        subscribed_events = {EventType.PLAYER_HEAL, EventType.CRITICAL_HIT}
        test_equipment = self.create_test_equipment(subscribed_events)
        
        returned_events = test_equipment.get_subscribed_events()
        self.assertEqual(returned_events, subscribed_events)
    
    def test_equipment_no_event_subscriptions(self):
        """Test equipment with no event subscriptions."""
        test_equipment = self.create_test_equipment(set())
        
        # Should return empty set
        self.assertEqual(test_equipment.get_subscribed_events(), set())
        
        # Should not crash when events are emitted
        context = HealContext(player=self.player, amount_healed=10)
        self.emitter.emit(EventType.PLAYER_HEAL, context)
        
        self.assertEqual(len(test_equipment.event_calls), 0)


if __name__ == '__main__':
    unittest.main()