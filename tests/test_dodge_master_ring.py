"""
Test module for Dodge Master Ring accessory.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from player import Player
from event_emitter import EventEmitter
from event_type import EventType
from event_context import AttackContext
from items.accessories.dodge_master_ring import DodgeMasterRing
from monsters.base import Monster
from traits import Trait

class TestDodgeMasterRing(unittest.TestCase):
    """Test cases for Dodge Master Ring accessory."""
    
    def setUp(self):
        """Set up test fixtures."""
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
        self.ring = DodgeMasterRing(0, 0)
        
    def tearDown(self):
        """Clean up after tests."""
        self.emitter.clear_all_listeners()
        
    def test_creation(self):
        """Test ring creation with correct attributes."""
        ring = DodgeMasterRing(3, 4)
        self.assertEqual(ring.x, 3)
        self.assertEqual(ring.y, 4)
        self.assertEqual(ring.name, "Dodge Master Ring")
        self.assertEqual(ring.char, "o")
        self.assertEqual(ring.description, "Gains +1% CRT bonus for each successful dodge")
        self.assertEqual(ring.market_value, 45)
        self.assertEqual(ring.equipment_slot, "accessory")
        self.assertIn(EventType.SUCCESSFUL_DODGE, ring.event_subscriptions)
        
    def test_initial_crit_bonus(self):
        """Test initial critical hit bonus is zero."""
        self.assertEqual(self.ring.get_crit_bonus(self.player), 0)
        self.assertEqual(self.ring.dodge_count, 0)
        
    def test_dodge_count_increments_on_player_dodge(self):
        """Test dodge count increases when player successfully dodges."""
        # Equip the ring
        self.player.accessories[0] = self.ring
        self.emitter.subscribe(EventType.SUCCESSFUL_DODGE, self.ring.on_event)
        
        # Create a mock monster attacker
        monster = Monster(10, 10, "Monster", 'M', (255, 255, 255), 10, 2, 1, 10)
        
        # Simulate player dodging
        context = AttackContext(
            attacker=monster,
            defender=self.player,
            player=self.player,
            damage=0
        )
        
        # Emit dodge event
        self.emitter.emit(EventType.SUCCESSFUL_DODGE, context)
        
        # Check dodge count increased
        self.assertEqual(self.ring.dodge_count, 1)
        self.assertEqual(self.ring.get_crit_bonus(self.player), 0.01)
        
    def test_multiple_dodges_stack_bonus(self):
        """Test multiple dodges increase critical hit bonus."""
        # Equip the ring
        self.player.accessories[0] = self.ring
        self.emitter.subscribe(EventType.SUCCESSFUL_DODGE, self.ring.on_event)
        
        # Create a mock monster attacker
        monster = Monster(10, 10, "Monster", 'M', (255, 255, 255), 10, 2, 1, 10)
        
        # Simulate multiple player dodges
        for i in range(5):
            context = AttackContext(
                attacker=monster,
                defender=self.player,
                player=self.player,
                damage=0
            )
            self.emitter.emit(EventType.SUCCESSFUL_DODGE, context)
        
        # Check cumulative bonus
        self.assertEqual(self.ring.dodge_count, 5)
        self.assertEqual(self.ring.get_crit_bonus(self.player), 0.05)  # 5% bonus
        
    def test_monster_dodge_does_not_count(self):
        """Test that monster dodges don't increase the bonus."""
        # Equip the ring
        self.player.accessories[0] = self.ring
        self.emitter.subscribe(EventType.SUCCESSFUL_DODGE, self.ring.on_event)
        
        # Create a mock monster defender
        monster = Monster(10, 10, "Monster", 'M', (255, 255, 255), 10, 2, 1, 10)
        
        # Simulate monster dodging (player attacks, monster dodges)
        context = AttackContext(
            attacker=self.player,
            defender=monster,
            player=self.player,
            damage=0
        )
        
        # Emit dodge event
        self.emitter.emit(EventType.SUCCESSFUL_DODGE, context)
        
        # Check dodge count did not increase
        self.assertEqual(self.ring.dodge_count, 0)
        self.assertEqual(self.ring.get_crit_bonus(self.player), 0)
        
    def test_high_dodge_count_bonus(self):
        """Test bonus calculation with high dodge count."""
        # Simulate many dodges
        self.ring.dodge_count = 20
        
        # Check 20% critical hit bonus
        self.assertEqual(self.ring.get_crit_bonus(self.player), 0.20)
        
        # Simulate extreme case
        self.ring.dodge_count = 100
        self.assertEqual(self.ring.get_crit_bonus(self.player), 1.00)  # 100% crit bonus

if __name__ == '__main__':
    unittest.main()