"""
Unit tests for event-driven items (accessories and weapons that respond to events).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import MagicMock
from event_emitter import EventEmitter
from event_type import EventType
from event_context import AttackContext, DeathContext, LevelUpContext, FloorContext
from player import Player

# Import new event-driven items
from items.accessories import HealingDodge, VampiresPendant, WardensTome, TurtlesBlessing, ProtectiveLevel
from items.weapons import Defender, HolyAvenger, BackhandBlade

class TestEventDrivenAccessories(unittest.TestCase):
    
    def setUp(self):
        # Reset singleton instance for each test
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
    
    def tearDown(self):
        # Clear all listeners after each test
        self.emitter.clear_all_listeners()
        EventEmitter._instance = None
    
    def test_healing_dodge_creation(self):
        """Test HealingDodge accessory creation and event subscription."""
        healing_dodge = HealingDodge(0, 0)
        
        self.assertEqual(healing_dodge.name, "Healing Dodge")
        self.assertIn(EventType.SUCCESSFUL_DODGE, healing_dodge.get_subscribed_events())
        self.assertEqual(healing_dodge.xp_cost, 10)
    
    def test_healing_dodge_event_response(self):
        """Test that HealingDodge heals when player successfully dodges."""
        healing_dodge = HealingDodge(0, 0)
        
        # Simulate equipment registration
        self.emitter.subscribe(EventType.SUCCESSFUL_DODGE, healing_dodge.on_event)
        
        # Damage player first so healing has visible effect
        self.player.hp = 30
        initial_hp = self.player.hp
        
        # Create dodge context
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        context = AttackContext(
            player=self.player,
            attacker=goblin,
            defender=self.player,
            damage=0,
            is_miss=True
        )
        
        # Emit dodge event
        self.emitter.emit(EventType.SUCCESSFUL_DODGE, context)
        
        # Check that player healed (5% of 50 max HP = 2.5, rounded down to 2)
        expected_heal = int(self.player.max_hp * 0.05)
        self.assertGreater(self.player.hp, initial_hp)
    
    def test_vampires_pendant_creation(self):
        """Test VampiresPendant accessory creation and event subscription."""
        pendant = VampiresPendant(0, 0)
        
        self.assertEqual(pendant.name, "Vampire's Pendant")
        self.assertIn(EventType.MONSTER_DEATH, pendant.get_subscribed_events())
        self.assertEqual(pendant.xp_cost, 15)
    
    def test_vampires_pendant_event_response(self):
        """Test that VampiresPendant heals when monster dies."""
        pendant = VampiresPendant(0, 0)
        
        # Simulate equipment registration
        self.emitter.subscribe(EventType.MONSTER_DEATH, pendant.on_event)
        
        # Damage player first
        self.player.hp = 30
        initial_hp = self.player.hp
        
        # Create death context
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        context = DeathContext(
            player=self.player,
            monster=goblin,
            experience_gained=25
        )
        
        # Emit death event
        self.emitter.emit(EventType.MONSTER_DEATH, context)
        
        # Check that player healed
        self.assertGreater(self.player.hp, initial_hp)
    
    def test_wardens_tome_creation(self):
        """Test WardensTome accessory creation and event subscription."""
        tome = WardensTome(0, 0)
        
        self.assertEqual(tome.name, "Warden's Tome")
        self.assertIn(EventType.LEVEL_UP, tome.get_subscribed_events())
        self.assertEqual(tome.xp_cost, 25)
    
    def test_wardens_tome_event_response(self):
        """Test that WardensTome permanently increases defense when leveling up."""
        tome = WardensTome(0, 0)
        
        # Simulate equipment registration
        self.emitter.subscribe(EventType.LEVEL_UP, tome.on_event)
        
        initial_defense = self.player.defense
        
        # Create level up context
        context = LevelUpContext(
            player=self.player,
            new_level=2,
            stat_increases={"attack": 1, "max_hp": 10}
        )
        
        # Emit level up event
        self.emitter.emit(EventType.LEVEL_UP, context)
        
        # Check that defense increased
        self.assertEqual(self.player.defense, initial_defense + 1)
    
    def test_turtles_blessing_creation(self):
        """Test TurtlesBlessing accessory creation and event subscription."""
        blessing = TurtlesBlessing(0, 0)
        
        self.assertEqual(blessing.name, "Turtle's Blessing")
        self.assertIn(EventType.FLOOR_CHANGE, blessing.get_subscribed_events())
        self.assertEqual(blessing.xp_cost, 15)
    
    def test_turtles_blessing_event_response(self):
        """Test that TurtlesBlessing gives shield when changing floors."""
        blessing = TurtlesBlessing(0, 0)
        
        # Simulate equipment registration
        self.emitter.subscribe(EventType.FLOOR_CHANGE, blessing.on_event)
        
        initial_shields = self.player.status_effects.shields
        
        # Create floor change context
        context = FloorContext(
            player=self.player,
            floor_number=2,
            previous_floor=1
        )
        
        # Emit floor change event
        self.emitter.emit(EventType.FLOOR_CHANGE, context)
        
        # Check that shield was added
        self.assertEqual(self.player.status_effects.shields, initial_shields + 1)
    
    def test_protective_level_creation(self):
        """Test ProtectiveLevel accessory creation and event subscription."""
        protective = ProtectiveLevel(0, 0)
        
        self.assertEqual(protective.name, "Protective Level")
        self.assertIn(EventType.LEVEL_UP, protective.get_subscribed_events())
        self.assertEqual(protective.xp_cost, 20)
    
    def test_protective_level_event_response(self):
        """Test that ProtectiveLevel gives shield when leveling up."""
        protective = ProtectiveLevel(0, 0)
        
        # Simulate equipment registration
        self.emitter.subscribe(EventType.LEVEL_UP, protective.on_event)
        
        initial_shields = self.player.status_effects.shields
        
        # Create level up context
        context = LevelUpContext(
            player=self.player,
            new_level=2,
            stat_increases={"attack": 1}
        )
        
        # Emit level up event
        self.emitter.emit(EventType.LEVEL_UP, context)
        
        # Check that shield was added
        self.assertEqual(self.player.status_effects.shields, initial_shields + 1)


class TestEventDrivenWeapons(unittest.TestCase):
    
    def setUp(self):
        # Reset singleton instance for each test
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
    
    def tearDown(self):
        # Clear all listeners after each test
        self.emitter.clear_all_listeners()
        EventEmitter._instance = None
    
    def test_defender_creation(self):
        """Test Defender weapon creation and event subscription."""
        defender = Defender(0, 0)
        
        self.assertEqual(defender.name, "Defender")
        self.assertIn(EventType.MONSTER_DEATH, defender.get_subscribed_events())
        self.assertEqual(defender.attack_bonus, 7)
        self.assertEqual(defender.xp_cost, 20)
    
    def test_defender_event_response(self):
        """Test that Defender trades attack for defense when monsters die."""
        defender = Defender(0, 0)
        
        # Simulate equipment registration and equipping
        self.player.weapon = defender
        self.emitter.subscribe(EventType.MONSTER_DEATH, defender.on_event)
        
        initial_attack = defender.attack_bonus
        initial_defense = self.player.defense
        
        # Create death context
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        context = DeathContext(
            player=self.player,
            monster=goblin,
            experience_gained=25
        )
        
        # Emit death event
        self.emitter.emit(EventType.MONSTER_DEATH, context)
        
        # Check that attack decreased and defense increased (only if attack > 1)
        if initial_attack > 1:
            self.assertEqual(defender.attack_bonus, initial_attack - 1)
            self.assertEqual(self.player.defense, initial_defense + 1)
        else:
            # If attack was already 1, shouldn't change
            self.assertEqual(defender.attack_bonus, 1)
    
    def test_holy_avenger_creation(self):
        """Test HolyAvenger weapon creation and event subscription."""
        avenger = HolyAvenger(0, 0)
        
        self.assertEqual(avenger.name, "Holy Avenger")
        self.assertIn(EventType.MONSTER_ATTACK_PLAYER, avenger.get_subscribed_events())
        self.assertEqual(avenger.attack_bonus, 8)
        self.assertEqual(avenger.xp_cost, 30)
        # Check for Holy trait
        from traits import Trait
        self.assertIn(Trait.HOLY, avenger.attack_traits)
    
    def test_backhand_blade_creation(self):
        """Test BackhandBlade weapon creation and event subscription."""
        blade = BackhandBlade(0, 0)
        
        self.assertEqual(blade.name, "Backhand Blade")
        self.assertIn(EventType.SUCCESSFUL_DODGE, blade.get_subscribed_events())
        self.assertEqual(blade.attack_bonus, 3)
        self.assertEqual(blade.evade_bonus, 0.05)
        self.assertEqual(blade.xp_cost, 25)
        # Check for Dark trait
        from traits import Trait
        self.assertIn(Trait.DARK, blade.attack_traits)


if __name__ == '__main__':
    unittest.main()