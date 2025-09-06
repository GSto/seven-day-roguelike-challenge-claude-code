"""
Test cases for Black Belt accessory functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from event_emitter import EventEmitter
from event_type import EventType
from event_context import AttackContext
from player import Player
from items.accessories.black_belt import BlackBelt

class TestBlackBelt(unittest.TestCase):
    """Test cases for the BlackBelt accessory."""
    
    def setUp(self):
        # Reset singleton instance for each test
        EventEmitter._instance = None
        self.emitter = EventEmitter()
    
    def tearDown(self):
        # Clear all listeners after each test
        self.emitter.clear_all_listeners()
    
    def test_black_belt_creation(self):
        """Test that BlackBelt can be created with correct properties."""
        belt = BlackBelt(5, 5)
        self.assertEqual(belt.name, "Black Belt")
        self.assertEqual(belt.char, "=")
        self.assertEqual(belt.description, "Gains +1% CRT bonus per dodge, +1% EVD bonus per critical hit")
        self.assertEqual(belt.market_value, 25)  # Common rarity
        self.assertEqual(belt.dodge_count, 0)
        self.assertEqual(belt.crit_count, 0)
        self.assertIn(EventType.SUCCESSFUL_DODGE, belt.event_subscriptions)
        self.assertIn(EventType.CRITICAL_HIT, belt.event_subscriptions)
    
    def test_dodge_increases_crit_bonus(self):
        """Test that successful dodge increases crit bonus."""
        belt = BlackBelt(0, 0)
        player = Player(5, 5)
        
        # Create mock attack context for dodge event
        context = AttackContext(
            attacker=None,  # Monster attacking player
            defender=player,
            player=player,
            damage=10
        )
        
        # Initial crit bonus should be 0
        self.assertEqual(belt.get_crit_bonus(player), 0.0)
        
        # Trigger dodge event
        belt.on_event(EventType.SUCCESSFUL_DODGE, context)
        
        # Crit bonus should increase by 1%
        self.assertEqual(belt.get_crit_bonus(player), 0.01)
        self.assertEqual(belt.dodge_count, 1)
        
        # Trigger another dodge
        belt.on_event(EventType.SUCCESSFUL_DODGE, context)
        
        # Crit bonus should increase to 2%
        self.assertEqual(belt.get_crit_bonus(player), 0.02)
        self.assertEqual(belt.dodge_count, 2)
    
    def test_crit_increases_evade_bonus(self):
        """Test that critical hit increases evade bonus."""
        belt = BlackBelt(0, 0)
        player = Player(5, 5)
        
        # Create mock attack context for crit event (player attacking)
        context = AttackContext(
            attacker=player,
            defender=None,  # Player attacking monster
            player=player,
            damage=20
        )
        
        # Initial evade bonus should be 0
        self.assertEqual(belt.get_evade_bonus(player), 0.0)
        
        # Trigger critical hit event
        belt.on_event(EventType.CRITICAL_HIT, context)
        
        # Evade bonus should increase by 1%
        self.assertEqual(belt.get_evade_bonus(player), 0.01)
        self.assertEqual(belt.crit_count, 1)
        
        # Trigger another critical hit
        belt.on_event(EventType.CRITICAL_HIT, context)
        
        # Evade bonus should increase to 2%
        self.assertEqual(belt.get_evade_bonus(player), 0.02)
        self.assertEqual(belt.crit_count, 2)
    
    def test_dodge_only_counts_when_player_is_defender(self):
        """Test that dodge only counts when player is the one dodging."""
        belt = BlackBelt(0, 0)
        player = Player(5, 5)
        other_defender = Player(10, 10)
        
        # Create context where someone else is the defender
        context = AttackContext(
            attacker=None,
            defender=other_defender,  # Not the player
            player=player,
            damage=10
        )
        
        # Trigger dodge event
        belt.on_event(EventType.SUCCESSFUL_DODGE, context)
        
        # Dodge count should not increase
        self.assertEqual(belt.dodge_count, 0)
        self.assertEqual(belt.get_crit_bonus(player), 0.0)
    
    def test_crit_only_counts_when_player_is_attacker(self):
        """Test that crit only counts when player is the one getting the critical hit."""
        belt = BlackBelt(0, 0)
        player = Player(5, 5)
        other_attacker = Player(10, 10)
        
        # Create context where someone else is the attacker
        context = AttackContext(
            attacker=other_attacker,  # Not the player
            defender=None,
            player=player,
            damage=20
        )
        
        # Trigger critical hit event
        belt.on_event(EventType.CRITICAL_HIT, context)
        
        # Crit count should not increase
        self.assertEqual(belt.crit_count, 0)
        self.assertEqual(belt.get_evade_bonus(player), 0.0)
    
    def test_combined_bonuses(self):
        """Test that both dodge and crit bonuses accumulate independently."""
        belt = BlackBelt(0, 0)
        player = Player(5, 5)
        
        # Create contexts for both events
        dodge_context = AttackContext(
            attacker=None,
            defender=player,
            player=player,
            damage=10
        )
        
        crit_context = AttackContext(
            attacker=player,
            defender=None,
            player=player,
            damage=20
        )
        
        # Trigger multiple dodge events
        belt.on_event(EventType.SUCCESSFUL_DODGE, dodge_context)
        belt.on_event(EventType.SUCCESSFUL_DODGE, dodge_context)
        belt.on_event(EventType.SUCCESSFUL_DODGE, dodge_context)  # 3 dodges
        
        # Trigger multiple crit events  
        belt.on_event(EventType.CRITICAL_HIT, crit_context)
        belt.on_event(EventType.CRITICAL_HIT, crit_context)  # 2 crits
        
        # Check that both bonuses accumulated independently
        self.assertEqual(belt.dodge_count, 3)
        self.assertEqual(belt.crit_count, 2)
        self.assertEqual(belt.get_crit_bonus(player), 0.03)  # 3% from dodges
        self.assertEqual(belt.get_evade_bonus(player), 0.02)  # 2% from crits
    
    def test_non_attack_context_ignored(self):
        """Test that non-AttackContext events are ignored."""
        belt = BlackBelt(0, 0)
        player = Player(5, 5)
        
        # Trigger events with non-AttackContext
        belt.on_event(EventType.SUCCESSFUL_DODGE, "not_an_attack_context")
        belt.on_event(EventType.CRITICAL_HIT, "not_an_attack_context")
        
        # Counts should remain zero
        self.assertEqual(belt.dodge_count, 0)
        self.assertEqual(belt.crit_count, 0)
        self.assertEqual(belt.get_crit_bonus(player), 0.0)
        self.assertEqual(belt.get_evade_bonus(player), 0.0)
    
    def test_equipment_slot(self):
        """Test that Black Belt is properly categorized as accessory."""
        belt = BlackBelt(0, 0)
        self.assertEqual(belt.equipment_slot, "accessory")


if __name__ == '__main__':
    unittest.main()