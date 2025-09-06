import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from player import Player
from event_emitter import EventEmitter
from event_type import EventType
from event_context import AttackContext
from items.accessories.brutality_expertise import BrutalityExpertise


class TestBrutalityExpertise(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
        self.brutality_expertise = BrutalityExpertise(0, 0)

    def tearDown(self):
        """Clean up after tests."""
        self.emitter.clear_all_listeners()

    def test_creation(self):
        """Test that BrutalityExpertise is created correctly."""
        item = BrutalityExpertise(1, 2)
        
        self.assertEqual(item.x, 1)
        self.assertEqual(item.y, 2)
        self.assertEqual(item.name, "Brutality Expertise")
        self.assertEqual(item.char, "⚔")
        self.assertEqual(item.color, (255, 255, 255))  # COLOR_WHITE from accessory base
        self.assertEqual(item.market_value, 75)
        self.assertEqual(item.crit_count, 0)
        self.assertIn(EventType.CRITICAL_HIT, item.event_subscriptions)

    def test_initial_bonuses(self):
        """Test initial stat bonuses are zero."""
        self.assertEqual(self.brutality_expertise.get_crit_multiplier_bonus(self.player), 0.0)

    def test_critical_hit_tracking(self):
        """Test that critical hits are tracked correctly."""
        # Simulate a critical hit by the player
        context = AttackContext(
            attacker=self.player,
            defender=None,  # Mock monster
            damage=10,
            player=self.player
        )
        
        self.brutality_expertise.on_event(EventType.CRITICAL_HIT, context)
        
        self.assertEqual(self.brutality_expertise.crit_count, 1)
        self.assertEqual(self.brutality_expertise.get_crit_multiplier_bonus(self.player), 0.05)

    def test_multiple_critical_hits(self):
        """Test that multiple critical hits stack correctly."""
        context = AttackContext(
            attacker=self.player,
            defender=None,
            damage=10,
            player=self.player
        )
        
        # Simulate 5 critical hits
        for i in range(5):
            self.brutality_expertise.on_event(EventType.CRITICAL_HIT, context)
            expected_bonus = (i + 1) * 0.05
            self.assertEqual(self.brutality_expertise.get_crit_multiplier_bonus(self.player), expected_bonus)
        
        self.assertEqual(self.brutality_expertise.crit_count, 5)
        self.assertEqual(self.brutality_expertise.get_crit_multiplier_bonus(self.player), 0.25)

    def test_monster_critical_hits_ignored(self):
        """Test that monster critical hits don't increase the counter."""
        # Create mock monster
        class MockMonster:
            pass
        
        monster = MockMonster()
        
        # Monster attacking player - should be ignored
        context = AttackContext(
            attacker=monster,
            defender=self.player,
            damage=10,
            player=self.player
        )
        
        self.brutality_expertise.on_event(EventType.CRITICAL_HIT, context)
        
        self.assertEqual(self.brutality_expertise.crit_count, 0)
        self.assertEqual(self.brutality_expertise.get_crit_multiplier_bonus(self.player), 0.0)

    def test_non_critical_events_ignored(self):
        """Test that non-critical hit events are ignored."""
        context = AttackContext(
            attacker=self.player,
            defender=None,
            damage=10,
            player=self.player
        )
        
        # Try other event types
        self.brutality_expertise.on_event(EventType.SUCCESSFUL_DODGE, context)
        self.brutality_expertise.on_event(EventType.PLAYER_HEAL, context)
        self.brutality_expertise.on_event(EventType.MONSTER_DEATH, context)
        
        self.assertEqual(self.brutality_expertise.crit_count, 0)
        self.assertEqual(self.brutality_expertise.get_crit_multiplier_bonus(self.player), 0.0)

    def test_wrong_context_type_ignored(self):
        """Test that events with wrong context types are ignored."""
        # Try with wrong context type
        self.brutality_expertise.on_event(EventType.CRITICAL_HIT, "not an attack context")
        
        self.assertEqual(self.brutality_expertise.crit_count, 0)
        self.assertEqual(self.brutality_expertise.get_crit_multiplier_bonus(self.player), 0.0)

    def test_crit_count_persistence(self):
        """Test that critical hit counter persists across multiple events."""
        # Build up some critical hits
        context = AttackContext(
            attacker=self.player,
            defender=None,
            damage=10,
            player=self.player
        )
        
        for _ in range(3):
            self.brutality_expertise.on_event(EventType.CRITICAL_HIT, context)
        
        self.assertEqual(self.brutality_expertise.crit_count, 3)
        self.assertAlmostEqual(self.brutality_expertise.get_crit_multiplier_bonus(self.player), 0.15, places=6)

    def test_equipment_integration(self):
        """Test that the item works when equipped by the player."""
        # Add to an accessory slot manually (simulating equipment)
        self.player.accessories[0] = self.brutality_expertise
        
        # Verify it's in the accessory list
        equipped_accessories = list(self.player.equipped_accessories())
        self.assertIn(self.brutality_expertise, equipped_accessories)
        
        # Simulate critical hit
        context = AttackContext(
            attacker=self.player,
            defender=None,
            damage=10,
            player=self.player
        )
        
        self.brutality_expertise.on_event(EventType.CRITICAL_HIT, context)
        
        # Verify the item has tracked the critical hit
        self.assertEqual(self.brutality_expertise.crit_count, 1)
        self.assertAlmostEqual(self.brutality_expertise.get_crit_multiplier_bonus(self.player), 0.05, places=6)

    def test_high_crit_count_scaling(self):
        """Test scaling with very high critical hit counts."""
        context = AttackContext(
            attacker=self.player,
            defender=None,
            damage=10,
            player=self.player
        )
        
        # Simulate 20 critical hits
        for i in range(20):
            self.brutality_expertise.on_event(EventType.CRITICAL_HIT, context)
        
        self.assertEqual(self.brutality_expertise.crit_count, 20)
        self.assertEqual(self.brutality_expertise.get_crit_multiplier_bonus(self.player), 1.0)  # 100% bonus


if __name__ == '__main__':
    unittest.main()