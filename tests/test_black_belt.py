"""
Unit tests for the Black Belt accessory.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import MagicMock
from items.accessories.black_belt import BlackBelt
from event_type import EventType
from event_context import AttackContext


class TestBlackBelt(unittest.TestCase):
    """Test suite for the Black Belt accessory."""
    
    def test_black_belt_initialization(self):
        """Test that Black Belt initializes with correct base stats."""
        belt = BlackBelt(5, 5)
        
        assert belt.name == "Black Belt"
        assert belt.crit_bonus == 0.0
        assert belt.evade_bonus == 0.0
        assert belt.dodge_count == 0
        assert belt.crit_count == 0
        assert EventType.SUCCESSFUL_DODGE in belt.event_subscriptions
        assert EventType.CRITICAL_HIT in belt.event_subscriptions
    
    def test_successful_dodge_increases_crit_bonus(self):
        """Test that successful dodges increase critical chance."""
        belt = BlackBelt(5, 5)
        
        # Create mock objects
        player = MagicMock()
        player.equipment_list = [belt]
        attacker = MagicMock()
        
        # Create attack context
        context = AttackContext(
            attacker=attacker,
            defender=player,
            player=player
        )
        
        # Simulate successful dodges
        belt.on_event(EventType.SUCCESSFUL_DODGE, context)
        assert belt.dodge_count == 1
        assert belt.crit_bonus == 0.01  # +1%
        
        belt.on_event(EventType.SUCCESSFUL_DODGE, context)
        assert belt.dodge_count == 2
        assert belt.crit_bonus == 0.02  # +2%
        
        belt.on_event(EventType.SUCCESSFUL_DODGE, context)
        assert belt.dodge_count == 3
        assert belt.crit_bonus == 0.03  # +3%
    
    def test_critical_hit_increases_evade_bonus(self):
        """Test that critical hits increase evade chance."""
        belt = BlackBelt(5, 5)
        
        # Create mock objects
        player = MagicMock()
        player.equipment_list = [belt]
        defender = MagicMock()
        
        # Create attack context
        context = AttackContext(
            attacker=player,
            defender=defender,
            player=player
        )
        
        # Simulate critical hits
        belt.on_event(EventType.CRITICAL_HIT, context)
        assert belt.crit_count == 1
        assert belt.evade_bonus == 0.01  # +1%
        
        belt.on_event(EventType.CRITICAL_HIT, context)
        assert belt.crit_count == 2
        assert belt.evade_bonus == 0.02  # +2%
        
        belt.on_event(EventType.CRITICAL_HIT, context)
        assert belt.crit_count == 3
        assert belt.evade_bonus == 0.03  # +3%
    
    def test_only_player_events_count(self):
        """Test that only the player's dodges and crits count."""
        belt = BlackBelt(5, 5)
        
        # Create mock objects
        player = MagicMock()
        player.equipment_list = [belt]
        enemy = MagicMock()
        enemy.equipment_list = []
        
        # Enemy dodges - should not count
        context = AttackContext(
            attacker=player,
            defender=enemy,
            player=player
        )
        belt.on_event(EventType.SUCCESSFUL_DODGE, context)
        assert belt.dodge_count == 0
        assert belt.crit_bonus == 0.0
        
        # Enemy critical hit - should not count
        context = AttackContext(
            attacker=enemy,
            defender=player,
            player=player
        )
        belt.on_event(EventType.CRITICAL_HIT, context)
        assert belt.crit_count == 0
        assert belt.evade_bonus == 0.0
    
    def test_belt_must_be_equipped(self):
        """Test that the belt must be equipped to gain bonuses."""
        belt = BlackBelt(5, 5)
        
        # Create mock objects
        player = MagicMock()
        player.equipment_list = []  # Belt not equipped
        attacker = MagicMock()
        
        # Create attack context
        context = AttackContext(
            attacker=attacker,
            defender=player,
            player=player
        )
        
        # Player dodges but belt is not equipped
        belt.on_event(EventType.SUCCESSFUL_DODGE, context)
        assert belt.dodge_count == 0
        assert belt.crit_bonus == 0.0
    
    def test_dynamic_description(self):
        """Test that the description updates with accumulated bonuses."""
        belt = BlackBelt(5, 5)
        
        # Initial description
        assert belt.description == "Gains +1% Critical chance per dodge, +1% EVD per critical hit"
        
        # Add some dodges and crits manually and update description
        belt.dodge_count = 5
        belt.crit_count = 3
        belt._update_description()
        
        # Check updated description
        expected = "Gains +1% Critical chance per dodge, +1% EVD per critical hit (Dodges: 5, Crits: 3)"
        assert belt.description == expected
    
    def test_combined_bonuses(self):
        """Test that both bonuses can accumulate independently."""
        belt = BlackBelt(5, 5)
        
        # Create mock objects
        player = MagicMock()
        player.equipment_list = [belt]
        enemy = MagicMock()
        
        # Player dodges
        dodge_context = AttackContext(
            attacker=enemy,
            defender=player,
            player=player
        )
        belt.on_event(EventType.SUCCESSFUL_DODGE, dodge_context)
        belt.on_event(EventType.SUCCESSFUL_DODGE, dodge_context)
        
        # Player scores critical hits
        crit_context = AttackContext(
            attacker=player,
            defender=enemy,
            player=player
        )
        belt.on_event(EventType.CRITICAL_HIT, crit_context)
        belt.on_event(EventType.CRITICAL_HIT, crit_context)
        belt.on_event(EventType.CRITICAL_HIT, crit_context)
        
        # Check both bonuses
        assert belt.dodge_count == 2
        assert belt.crit_count == 3
        assert belt.crit_bonus == 0.02  # +2% from dodges
        assert belt.evade_bonus == 0.03  # +3% from crits


if __name__ == "__main__":
    unittest.main()