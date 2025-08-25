"""
Performance tests for the event system with multiple listeners.
Tests event emission overhead and memory usage patterns.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import time
import tracemalloc
from unittest.mock import MagicMock
from event_emitter import EventEmitter
from event_type import EventType
from event_context import AttackContext, DeathContext, LevelUpContext, FloorContext
from player import Player

# Import event-driven items for stress testing
from items.accessories import HealingDodge, VampiresPendant, WardensTome, TurtlesBlessing, ProtectiveLevel
from items.weapons import Defender, HolyAvenger, BackhandBlade


class TestEventPerformance(unittest.TestCase):
    """Performance tests for event system scalability."""
    
    def setUp(self):
        # Reset singleton instance for each test
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
    
    def tearDown(self):
        # Clear all listeners after each test
        self.emitter.clear_all_listeners()
        EventEmitter._instance = None
    
    def test_single_event_emission_performance(self):
        """Test baseline performance for single event emission."""
        # Create a simple callback
        callback_count = 0
        def simple_callback(event_type, context):
            nonlocal callback_count
            callback_count += 1
        
        # Subscribe single listener
        self.emitter.subscribe(EventType.MONSTER_DEATH, simple_callback)
        
        # Create context
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        context = DeathContext(
            player=self.player,
            monster=goblin,
            experience_gained=10
        )
        
        # Time multiple emissions
        iterations = 1000
        start_time = time.perf_counter()
        
        for _ in range(iterations):
            self.emitter.emit(EventType.MONSTER_DEATH, context)
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        avg_time = (total_time / iterations) * 1000000  # Convert to microseconds
        
        # Performance assertion - should be very fast
        self.assertLess(avg_time, 100, f"Average event emission took {avg_time:.2f}μs, expected < 100μs")
        self.assertEqual(callback_count, iterations)
        
        print(f"Single event emission: {avg_time:.2f}μs average over {iterations} iterations")
    
    def test_multiple_listeners_performance(self):
        """Test performance with many listeners for the same event."""
        # Create multiple callback functions
        callback_counts = []
        callbacks = []
        
        num_listeners = 50
        for i in range(num_listeners):
            count = [0]  # Use list to make it mutable
            callback_counts.append(count)
            
            def make_callback(counter):
                def callback(event_type, context):
                    counter[0] += 1
                return callback
            
            callbacks.append(make_callback(count))
        
        # Subscribe all listeners to the same event
        for callback in callbacks:
            self.emitter.subscribe(EventType.MONSTER_DEATH, callback)
        
        # Create context
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        context = DeathContext(
            player=self.player,
            monster=goblin,
            experience_gained=10
        )
        
        # Time event emission with multiple listeners
        iterations = 100
        start_time = time.perf_counter()
        
        for _ in range(iterations):
            self.emitter.emit(EventType.MONSTER_DEATH, context)
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        avg_time = (total_time / iterations) * 1000000  # Convert to microseconds
        
        # Performance assertion - should scale reasonably
        self.assertLess(avg_time, 1000, f"Average event emission with {num_listeners} listeners took {avg_time:.2f}μs, expected < 1000μs")
        
        # Verify all callbacks were called
        for count in callback_counts:
            self.assertEqual(count[0], iterations)
        
        print(f"Event emission with {num_listeners} listeners: {avg_time:.2f}μs average over {iterations} iterations")
    
    def test_real_items_performance(self):
        """Test performance with actual event-driven items as listeners."""
        # Create multiple real items that respond to MONSTER_DEATH
        items = [
            VampiresPendant(0, 0),
            VampiresPendant(1, 0), 
            VampiresPendant(2, 0),
            Defender(0, 0),
            Defender(1, 0),
        ]
        
        # Set up player state for items
        self.player.hp = 30  # For healing items
        self.player.weapon = items[3]  # Set defender as weapon
        
        # Subscribe all items
        for item in items:
            self.emitter.subscribe(EventType.MONSTER_DEATH, item.on_event)
        
        # Create context
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        context = DeathContext(
            player=self.player,
            monster=goblin,
            experience_gained=10
        )
        
        # Time realistic event usage
        iterations = 500
        start_time = time.perf_counter()
        
        for _ in range(iterations):
            self.emitter.emit(EventType.MONSTER_DEATH, context)
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        avg_time = (total_time / iterations) * 1000000  # Convert to microseconds
        
        # Performance assertion for realistic usage
        self.assertLess(avg_time, 500, f"Average event emission with real items took {avg_time:.2f}μs, expected < 500μs")
        
        # Verify effects occurred
        self.assertGreater(self.player.hp, 30)  # Should have healed from pendants
        
        print(f"Event emission with {len(items)} real items: {avg_time:.2f}μs average over {iterations} iterations")
    
    def test_memory_usage_with_many_listeners(self):
        """Test memory usage patterns with many event listeners."""
        # Start memory monitoring
        tracemalloc.start()
        
        # Create many items and subscribe them
        num_items = 100
        items = []
        
        for i in range(num_items):
            if i % 3 == 0:
                item = VampiresPendant(i, 0)
                event_type = EventType.MONSTER_DEATH
            elif i % 3 == 1:
                item = HealingDodge(i, 0)
                event_type = EventType.SUCCESSFUL_DODGE
            else:
                item = WardensTome(i, 0)
                event_type = EventType.LEVEL_UP
            
            items.append((item, event_type))
            self.emitter.subscribe(event_type, item.on_event)
        
        # Take snapshot after subscription
        snapshot_after = tracemalloc.take_snapshot()
        
        # Emit many events
        from monsters.goblin import Goblin
        for _ in range(50):
            goblin = Goblin(10, 10)
            self.emitter.emit(EventType.MONSTER_DEATH, DeathContext(
                player=self.player, monster=goblin, experience_gained=10
            ))
            self.emitter.emit(EventType.SUCCESSFUL_DODGE, AttackContext(
                player=self.player, attacker=goblin, defender=self.player, damage=0, is_miss=True
            ))
            self.emitter.emit(EventType.LEVEL_UP, LevelUpContext(
                player=self.player, new_level=2, stat_increases={"attack": 1}
            ))
        
        # Take final snapshot
        snapshot_final = tracemalloc.take_snapshot()
        
        # Analyze memory usage
        top_stats = snapshot_final.compare_to(snapshot_after, 'lineno')
        total_size_diff = sum(stat.size_diff for stat in top_stats)
        
        # Memory growth should be minimal (allowing for some overhead)
        self.assertLess(total_size_diff, 1024 * 100, f"Memory grew by {total_size_diff} bytes, expected < 100KB")
        
        print(f"Memory usage with {num_items} listeners: {total_size_diff} bytes growth")
        
        # Clean up
        tracemalloc.stop()
    
    def test_subscription_unsubscription_performance(self):
        """Test performance of subscribing and unsubscribing many listeners."""
        num_items = 100
        items = []
        
        # Create items
        for i in range(num_items):
            item = VampiresPendant(i, 0)
            items.append(item)
        
        # Time subscription
        start_time = time.perf_counter()
        for item in items:
            self.emitter.subscribe(EventType.MONSTER_DEATH, item.on_event)
        subscription_time = time.perf_counter() - start_time
        
        # Time unsubscription
        start_time = time.perf_counter()
        for item in items:
            self.emitter.unsubscribe(EventType.MONSTER_DEATH, item.on_event)
        unsubscription_time = time.perf_counter() - start_time
        
        # Performance assertions
        avg_subscribe_time = (subscription_time / num_items) * 1000000  # microseconds
        avg_unsubscribe_time = (unsubscription_time / num_items) * 1000000  # microseconds
        
        self.assertLess(avg_subscribe_time, 100, f"Average subscription took {avg_subscribe_time:.2f}μs, expected < 100μs")
        self.assertLess(avg_unsubscribe_time, 100, f"Average unsubscription took {avg_unsubscribe_time:.2f}μs, expected < 100μs")
        
        print(f"Subscription performance: {avg_subscribe_time:.2f}μs average over {num_items} items")
        print(f"Unsubscription performance: {avg_unsubscribe_time:.2f}μs average over {num_items} items")
    
    def test_concurrent_event_types_performance(self):
        """Test performance when many different event types are being emitted."""
        # Subscribe listeners to different event types
        monster_items = [VampiresPendant(i, 0) for i in range(10)]
        dodge_items = [HealingDodge(i, 0) for i in range(10)]  
        level_items = [WardensTome(i, 0) for i in range(10)]
        
        for item in monster_items:
            self.emitter.subscribe(EventType.MONSTER_DEATH, item.on_event)
        for item in dodge_items:
            self.emitter.subscribe(EventType.SUCCESSFUL_DODGE, item.on_event)
        for item in level_items:
            self.emitter.subscribe(EventType.LEVEL_UP, item.on_event)
        
        # Create contexts
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        contexts = [
            (EventType.MONSTER_DEATH, DeathContext(player=self.player, monster=goblin, experience_gained=10)),
            (EventType.SUCCESSFUL_DODGE, AttackContext(player=self.player, attacker=goblin, defender=self.player, damage=0, is_miss=True)),
            (EventType.LEVEL_UP, LevelUpContext(player=self.player, new_level=2, stat_increases={"attack": 1}))
        ]
        
        # Set up player for healing
        self.player.hp = 30
        
        # Time emission of mixed event types
        iterations = 300
        start_time = time.perf_counter()
        
        for i in range(iterations):
            event_type, context = contexts[i % len(contexts)]
            self.emitter.emit(event_type, context)
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        avg_time = (total_time / iterations) * 1000000  # Convert to microseconds
        
        # Performance assertion for mixed events
        self.assertLess(avg_time, 200, f"Average mixed event emission took {avg_time:.2f}μs, expected < 200μs")
        
        print(f"Mixed event types performance: {avg_time:.2f}μs average over {iterations} events")


if __name__ == '__main__':
    # Run with more verbose output for performance numbers
    unittest.main(verbosity=2)