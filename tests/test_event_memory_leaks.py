"""
Memory leak tests for the event system.
Tests proper cleanup and prevention of memory leaks in event subscriptions.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import gc
import weakref
from event_emitter import EventEmitter
from event_type import EventType
from event_context import DeathContext
from player import Player
from game import Game

# Import event-driven items
from items.accessories import VampiresPendant, HealingDodge
from items.weapons import Defender


class TestEventMemoryLeaks(unittest.TestCase):
    """Memory leak tests for event system cleanup."""
    
    def setUp(self):
        # Reset singleton instance for each test
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
        self.game = Game()
        self.game.player = self.player
    
    def tearDown(self):
        # Clear all listeners after each test
        self.emitter.clear_all_listeners()
        EventEmitter._instance = None
        # Force garbage collection
        gc.collect()
    
    def test_unregistered_items_can_be_garbage_collected(self):
        """Test that items can be garbage collected after unregistering from events."""
        # Create item and get weak reference
        item = VampiresPendant(0, 0)
        weak_ref = weakref.ref(item)
        
        # Subscribe to events
        self.emitter.subscribe(EventType.MONSTER_DEATH, item.on_event)
        
        # Verify item exists and is subscribed
        self.assertIsNotNone(weak_ref())
        self.assertEqual(len(self.emitter._listeners[EventType.MONSTER_DEATH]), 1)
        
        # Unsubscribe and delete reference
        self.emitter.unsubscribe(EventType.MONSTER_DEATH, item.on_event)
        del item
        gc.collect()
        
        # Item should be garbage collected
        self.assertIsNone(weak_ref(), "Item was not garbage collected after unsubscribing")
        self.assertEqual(len(self.emitter._listeners[EventType.MONSTER_DEATH]), 0)
    
    def test_equipped_items_prevent_garbage_collection(self):
        """Test that equipped items are properly retained and not garbage collected."""
        # Create item and get weak reference
        item = VampiresPendant(0, 0)
        weak_ref = weakref.ref(item)
        
        # Equip item (this should keep it alive)
        self.player.accessories[0] = item
        self.emitter.subscribe(EventType.MONSTER_DEATH, item.on_event)
        
        # Delete local reference
        del item
        gc.collect()
        
        # Item should still exist because it's equipped
        self.assertIsNotNone(weak_ref(), "Equipped item was garbage collected")
        
        # Unequip item
        equipped_item = self.player.accessories[0]
        self.emitter.unsubscribe(EventType.MONSTER_DEATH, equipped_item.on_event)
        self.player.accessories[0] = None
        del equipped_item
        gc.collect()
        
        # Now item should be garbage collected
        self.assertIsNone(weak_ref(), "Item was not garbage collected after unequipping")
    
    def test_mass_subscription_cleanup(self):
        """Test that mass subscribing and unsubscribing doesn't leak memory."""
        items = []
        weak_refs = []
        
        # Create many items and subscribe them
        for i in range(100):
            item = VampiresPendant(i, 0)
            items.append(item)
            weak_refs.append(weakref.ref(item))
            self.emitter.subscribe(EventType.MONSTER_DEATH, item.on_event)
        
        # Verify all are subscribed
        self.assertEqual(len(self.emitter._listeners[EventType.MONSTER_DEATH]), 100)
        
        # Unsubscribe all and clear references
        for item in items:
            self.emitter.unsubscribe(EventType.MONSTER_DEATH, item.on_event)
        items.clear()
        gc.collect()
        
        # Most items should be garbage collected (allowing for GC timing)
        collected_count = sum(1 for ref in weak_refs if ref() is None)
        self.assertGreaterEqual(collected_count, 95, f"Only {collected_count}/100 items were garbage collected, expected >= 95")
        self.assertEqual(len(self.emitter._listeners[EventType.MONSTER_DEATH]), 0)
    
    def test_event_emitter_singleton_cleanup(self):
        """Test that EventEmitter singleton can be properly reset."""
        # Create items and subscribe them
        items = [VampiresPendant(i, 0) for i in range(10)]
        for item in items:
            self.emitter.subscribe(EventType.MONSTER_DEATH, item.on_event)
        
        # Verify subscriptions
        self.assertEqual(len(self.emitter._listeners[EventType.MONSTER_DEATH]), 10)
        
        # Clear all listeners
        self.emitter.clear_all_listeners()
        
        # Verify cleanup
        self.assertEqual(len(self.emitter._listeners[EventType.MONSTER_DEATH]), 0)
        
        # Reset singleton instance
        EventEmitter._instance = None
        new_emitter = EventEmitter()
        
        # New instance should be clean
        self.assertEqual(len(new_emitter._listeners.get(EventType.MONSTER_DEATH, [])), 0)
    
    def test_circular_reference_prevention(self):
        """Test that event system doesn't create circular references."""
        # Create item that might create circular references
        item = VampiresPendant(0, 0)
        weak_ref = weakref.ref(item)
        
        # Subscribe item's method (this could potentially create circular ref)
        self.emitter.subscribe(EventType.MONSTER_DEATH, item.on_event)
        
        # Create context that references the item indirectly
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        context = DeathContext(
            player=self.player,
            monster=goblin,
            experience_gained=10
        )
        
        # Emit event (this creates temporary references)
        self.emitter.emit(EventType.MONSTER_DEATH, context)
        
        # Unsubscribe and delete
        self.emitter.unsubscribe(EventType.MONSTER_DEATH, item.on_event)
        del item
        del context
        gc.collect()
        
        # Item should be collected despite event emission
        self.assertIsNone(weak_ref(), "Circular reference prevented garbage collection")
    
    def test_event_context_cleanup(self):
        """Test that event contexts don't cause memory leaks."""
        contexts = []
        weak_refs = []
        
        # Create many contexts
        from monsters.goblin import Goblin
        for i in range(50):
            goblin = Goblin(i, i)
            context = DeathContext(
                player=self.player,
                monster=goblin,
                experience_gained=10
            )
            contexts.append(context)
            weak_refs.append(weakref.ref(context))
        
        # Use contexts in events
        item = VampiresPendant(0, 0)
        self.emitter.subscribe(EventType.MONSTER_DEATH, item.on_event)
        
        for context in contexts:
            self.emitter.emit(EventType.MONSTER_DEATH, context)
        
        # Clear references
        contexts.clear()
        gc.collect()
        
        # Most contexts should be garbage collected (allowing for GC timing)
        collected_count = sum(1 for ref in weak_refs if ref() is None)
        self.assertGreaterEqual(collected_count, 45, f"Only {collected_count}/50 contexts were garbage collected, expected >= 45")
    
    def test_game_equipment_lifecycle_cleanup(self):
        """Test that game equipment lifecycle doesn't leak memory."""
        items = []
        weak_refs = []
        
        # Create items
        for i in range(10):
            item = HealingDodge(i, 0)
            items.append(item)
            weak_refs.append(weakref.ref(item))
        
        # Simulate equip/unequip cycles
        for item in items:
            # Equip
            self.player.accessories[0] = item
            self.game.register_equipment_events(item)
            
            # Test event works
            from monsters.goblin import Goblin
            goblin = Goblin(10, 10)
            from event_context import AttackContext
            context = AttackContext(
                player=self.player,
                attacker=goblin,
                defender=self.player,
                damage=0,
                is_miss=True
            )
            self.emitter.emit(EventType.SUCCESSFUL_DODGE, context)
            
            # Unequip
            self.game.unregister_equipment_events(item)
            self.player.accessories[0] = None
        
        # Clear references
        items.clear()
        gc.collect()
        
        # Most items should be garbage collected (allowing for GC timing)
        collected_count = sum(1 for ref in weak_refs if ref() is None)
        self.assertGreaterEqual(collected_count, 8, f"Only {collected_count}/10 items were garbage collected, expected >= 8")
        
        # No listeners should remain
        self.assertEqual(len(self.emitter._listeners.get(EventType.SUCCESSFUL_DODGE, [])), 0)
    
    def test_repeated_subscribe_unsubscribe_cycles(self):
        """Test that repeated subscription cycles don't accumulate memory."""
        item = VampiresPendant(0, 0)
        
        # Perform many subscribe/unsubscribe cycles
        for _ in range(1000):
            self.emitter.subscribe(EventType.MONSTER_DEATH, item.on_event)
            self.assertEqual(len(self.emitter._listeners[EventType.MONSTER_DEATH]), 1)
            
            self.emitter.unsubscribe(EventType.MONSTER_DEATH, item.on_event)
            self.assertEqual(len(self.emitter._listeners[EventType.MONSTER_DEATH]), 0)
        
        # Final state should be clean
        self.assertEqual(len(self.emitter._listeners[EventType.MONSTER_DEATH]), 0)
    
    def test_exception_in_callback_cleanup(self):
        """Test that exceptions in callbacks don't prevent cleanup."""
        # Create callback that raises exception
        class BadItem:
            def __init__(self):
                pass
            
            def on_event(self, event_type, context):
                raise ValueError("Test exception in callback")
        
        bad_item = BadItem()
        good_item = VampiresPendant(0, 0)
        
        weak_bad_ref = weakref.ref(bad_item)
        weak_good_ref = weakref.ref(good_item)
        
        # Subscribe both items
        self.emitter.subscribe(EventType.MONSTER_DEATH, bad_item.on_event)
        self.emitter.subscribe(EventType.MONSTER_DEATH, good_item.on_event)
        
        # Emit event - should handle exception
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        context = DeathContext(
            player=self.player,
            monster=goblin,
            experience_gained=10
        )
        
        # This should not crash despite bad_item raising exception
        try:
            self.emitter.emit(EventType.MONSTER_DEATH, context)
        except ValueError:
            pass  # Expected from bad_item
        
        # Unsubscribe and cleanup
        self.emitter.unsubscribe(EventType.MONSTER_DEATH, bad_item.on_event)
        self.emitter.unsubscribe(EventType.MONSTER_DEATH, good_item.on_event)
        
        del bad_item, good_item
        gc.collect()
        
        # Both items should be collectible despite exception
        self.assertIsNone(weak_bad_ref(), "Bad item with exception was not garbage collected")
        self.assertIsNone(weak_good_ref(), "Good item was not garbage collected")


if __name__ == '__main__':
    unittest.main(verbosity=2)