"""
Integration tests for complex event chains and scenarios.
Tests multiple items responding to same events, event cascades, and equipment lifecycle.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import MagicMock, patch
from event_emitter import EventEmitter
from event_type import EventType
from event_context import AttackContext, DeathContext, LevelUpContext, FloorContext, ConsumeContext
from player import Player
from game import Game

# Import event-driven items
from items.accessories import HealingDodge, VampiresPendant, WardensTome, TurtlesBlessing, ProtectiveLevel
from items.accessories.psychics_turban import PsychicsTurban
from items.armor.skin_suit import SkinSuit
from items.weapons import Defender, HolyAvenger, BackhandBlade


class TestEventIntegration(unittest.TestCase):
    """Integration tests for complex event scenarios."""
    
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
    
    def test_multiple_items_respond_to_same_event(self):
        """Test that multiple items can respond to the same event simultaneously."""
        # Equip multiple items that respond to MONSTER_DEATH
        vampire_pendant = VampiresPendant(0, 0)
        defender = Defender(0, 0)
        skin_suit = SkinSuit(0, 0)
        
        # Simulate equipping all items
        self.player.accessories.append(vampire_pendant)
        self.player.weapon = defender
        self.player.armor = skin_suit
        
        # Register all event listeners
        self.emitter.subscribe(EventType.MONSTER_DEATH, vampire_pendant.on_event)
        self.emitter.subscribe(EventType.MONSTER_DEATH, defender.on_event)
        self.emitter.subscribe(EventType.MONSTER_DEATH, skin_suit.on_event)
        
        # Set up initial state
        self.player.hp = 30  # Reduced for healing test
        initial_hp = self.player.hp
        initial_attack = defender.attack_bonus
        initial_defense = self.player.defense
        initial_skin_count = skin_suit.death_counter
        
        # Create monster death event
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        context = DeathContext(
            player=self.player,
            monster=goblin,
            experience_gained=25
        )
        
        # Emit event - all three items should respond
        self.emitter.emit(EventType.MONSTER_DEATH, context)
        
        # Verify all items responded
        self.assertGreater(self.player.hp, initial_hp)  # Vampire pendant healed
        if initial_attack > 1:
            self.assertEqual(defender.attack_bonus, initial_attack - 1)  # Defender lost attack
            self.assertEqual(self.player.defense, initial_defense + 1)  # Defender gave defense
        self.assertEqual(skin_suit.death_counter, initial_skin_count + 1)  # Skin suit counted
    
    def test_equipment_registration_lifecycle(self):
        """Test that equipment properly registers/unregisters when equipped/unequipped."""
        healing_dodge = HealingDodge(0, 0)
        
        # Verify no listeners initially
        self.assertEqual(len(self.emitter._listeners.get(EventType.SUCCESSFUL_DODGE, [])), 0)
        
        # Directly equip and register events
        self.player.accessories[0] = healing_dodge
        self.game.register_equipment_events(healing_dodge)
        
        # Verify listener was registered
        self.assertEqual(len(self.emitter._listeners.get(EventType.SUCCESSFUL_DODGE, [])), 1)
        self.assertIn(healing_dodge.on_event, self.emitter._listeners[EventType.SUCCESSFUL_DODGE])
        
        # Test that item responds to events
        self.player.hp = 30
        initial_hp = self.player.hp
        
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        context = AttackContext(
            player=self.player,
            attacker=goblin,
            defender=self.player,
            damage=0,
            is_miss=True
        )
        
        self.emitter.emit(EventType.SUCCESSFUL_DODGE, context)
        self.assertGreater(self.player.hp, initial_hp)
        
        # Unequip item manually since there's no direct unequip_item method
        self.game.unregister_equipment_events(healing_dodge)
        self.player.accessories[0] = None
        self.player.add_item(healing_dodge)
        
        # Verify listener was unregistered
        self.assertEqual(len(self.emitter._listeners.get(EventType.SUCCESSFUL_DODGE, [])), 0)
    
    def test_level_up_cascade_effects(self):
        """Test cascading effects when multiple items respond to level up."""
        # Equip items that respond to LEVEL_UP
        wardens_tome = WardensTome(0, 0)
        protective_level = ProtectiveLevel(0, 0)
        
        self.player.accessories.append(wardens_tome)
        self.player.accessories.append(protective_level)
        
        # Register listeners
        self.emitter.subscribe(EventType.LEVEL_UP, wardens_tome.on_event)
        self.emitter.subscribe(EventType.LEVEL_UP, protective_level.on_event)
        
        # Record initial state
        initial_defense = self.player.defense
        initial_shields = self.player.status_effects.shields
        
        # Create level up event
        context = LevelUpContext(
            player=self.player,
            new_level=2,
            stat_increases={"attack": 1, "max_hp": 10}
        )
        
        # Emit level up event
        self.emitter.emit(EventType.LEVEL_UP, context)
        
        # Verify both items responded
        self.assertEqual(self.player.defense, initial_defense + 1)  # Warden's tome effect
        self.assertEqual(self.player.status_effects.shields, initial_shields + 1)  # Protective level effect
    
    def test_dodge_counter_attack_chain(self):
        """Test complex chain: dodge -> heal + counter-attack."""
        # Equip items that respond to dodge
        healing_dodge = HealingDodge(0, 0)
        backhand_blade = BackhandBlade(0, 0)
        
        self.player.accessories.append(healing_dodge)
        self.player.weapon = backhand_blade
        
        # Register listeners
        self.emitter.subscribe(EventType.SUCCESSFUL_DODGE, healing_dodge.on_event)
        self.emitter.subscribe(EventType.SUCCESSFUL_DODGE, backhand_blade.on_event)
        
        # Set up scenario
        self.player.hp = 30
        initial_hp = self.player.hp
        
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        initial_goblin_hp = goblin.hp
        
        # Mock the counter-attack to track if it was called
        with patch.object(goblin, 'take_damage_with_traits', return_value=5) as mock_damage:
            context = AttackContext(
                player=self.player,
                attacker=goblin,
                defender=self.player,
                damage=0,
                is_miss=True
            )
            
            # Emit dodge event
            self.emitter.emit(EventType.SUCCESSFUL_DODGE, context)
            
            # Verify healing occurred
            self.assertGreater(self.player.hp, initial_hp)
            
            # Verify counter-attack was triggered
            mock_damage.assert_called_once()
    
    def test_historical_vs_event_counters(self):
        """Test that items properly combine historical and event-driven counters."""
        # Set up player with some historical activity
        self.player.consumable_count = 5
        self.player.body_count = 8
        
        # Equip items
        turban = PsychicsTurban(0, 0)
        skin_suit = SkinSuit(0, 0)
        
        self.player.accessories.append(turban)
        self.player.armor = skin_suit
        
        # Register listeners
        self.emitter.subscribe(EventType.PLAYER_CONSUME_ITEM, turban.on_event)
        self.emitter.subscribe(EventType.MONSTER_DEATH, skin_suit.on_event)
        
        # Check initial bonuses include historical counts
        turban_bonus = turban.get_attack_bonus(self.player)
        skin_bonus = skin_suit.get_defense_bonus(self.player)
        
        self.assertEqual(turban_bonus, 5)  # Historical consumables
        self.assertEqual(skin_bonus, 2)  # 8 historical kills / 4 = 2
        
        # Trigger events
        from items.consumables.health_potion import HealthPotion
        potion = HealthPotion(0, 0)
        consume_context = ConsumeContext(
            player=self.player,
            item_type="HealthPotion",
            item=potion
        )
        self.emitter.emit(EventType.PLAYER_CONSUME_ITEM, consume_context)
        
        from monsters.goblin import Goblin
        for _ in range(4):  # Kill 4 more monsters
            goblin = Goblin(10, 10)
            death_context = DeathContext(
                player=self.player,
                monster=goblin,
                experience_gained=10
            )
            self.emitter.emit(EventType.MONSTER_DEATH, death_context)
        
        # Check bonuses now include event-driven counts
        new_turban_bonus = turban.get_attack_bonus(self.player)
        new_skin_bonus = skin_suit.get_defense_bonus(self.player)
        
        self.assertEqual(new_turban_bonus, 6)  # 5 historical + 1 event
        self.assertEqual(new_skin_bonus, 3)  # (8 historical + 4 events) / 4 = 3
    
    def test_event_order_independence(self):
        """Test that event handling is order-independent for simultaneous events."""
        # Create multiple items responding to same event
        items = [VampiresPendant(0, 0) for _ in range(3)]
        
        for item in items:
            self.player.accessories.append(item)
            self.emitter.subscribe(EventType.MONSTER_DEATH, item.on_event)
        
        # Damage player to see healing
        self.player.hp = 20
        initial_hp = self.player.hp
        
        # Emit event multiple times
        from monsters.goblin import Goblin
        for _ in range(5):
            goblin = Goblin(10, 10)
            context = DeathContext(
                player=self.player,
                monster=goblin,
                experience_gained=10
            )
            self.emitter.emit(EventType.MONSTER_DEATH, context)
        
        # Each event should trigger all 3 pendants (15% healing each)
        # Total healing should be significant regardless of order
        self.assertGreater(self.player.hp, initial_hp + 10)
    
    def test_no_duplicate_subscriptions(self):
        """Test that items don't get duplicate subscriptions when re-equipped."""
        healing_dodge = HealingDodge(0, 0)
        
        # Directly equip and register
        self.player.accessories[0] = healing_dodge  
        self.game.register_equipment_events(healing_dodge)
        # Unequip
        self.game.unregister_equipment_events(healing_dodge)
        self.player.accessories[0] = None
        # Re-equip
        self.player.accessories[0] = healing_dodge
        self.game.register_equipment_events(healing_dodge)
        
        # Should only have one listener
        listeners = self.emitter._listeners.get(EventType.SUCCESSFUL_DODGE, [])
        self.assertEqual(len(listeners), 1)
        
        # Should still work correctly
        self.player.hp = 30
        initial_hp = self.player.hp
        
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        context = AttackContext(
            player=self.player,
            attacker=goblin,
            defender=self.player,
            damage=0,
            is_miss=True
        )
        
        self.emitter.emit(EventType.SUCCESSFUL_DODGE, context)
        expected_heal = int(self.player.max_hp * 0.05)
        self.assertEqual(self.player.hp, initial_hp + expected_heal)


if __name__ == '__main__':
    unittest.main()