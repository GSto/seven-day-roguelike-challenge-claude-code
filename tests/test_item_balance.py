"""
Balance tests for event-driven items to ensure they provide appropriate power levels.
Tests progression curves, synergies, and edge cases for game balance.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import patch
from event_emitter import EventEmitter
from event_type import EventType
from event_context import AttackContext, DeathContext, LevelUpContext, FloorContext, ConsumeContext
from player import Player

# Import all event-driven items for balance testing
from items.accessories import HealingDodge, VampiresPendant, WardensTome, TurtlesBlessing, ProtectiveLevel
from items.accessories.psychics_turban import PsychicsTurban
from items.armor.skin_suit import SkinSuit
from items.weapons import Defender, HolyAvenger, BackhandBlade


class TestItemBalance(unittest.TestCase):
    """Balance tests for event-driven items."""
    
    def setUp(self):
        # Reset singleton instance for each test
        EventEmitter._instance = None
        self.emitter = EventEmitter()
        self.player = Player(5, 5)
    
    def tearDown(self):
        # Clear all listeners after each test
        self.emitter.clear_all_listeners()
        EventEmitter._instance = None
    
    def test_healing_item_power_levels(self):
        """Test that healing items provide appropriate healing amounts."""
        healing_dodge = HealingDodge(0, 0)
        vampire_pendant = VampiresPendant(0, 0)
        
        # Subscribe items
        self.emitter.subscribe(EventType.SUCCESSFUL_DODGE, healing_dodge.on_event)
        self.emitter.subscribe(EventType.MONSTER_DEATH, vampire_pendant.on_event)
        
        # Test with different max HP values
        test_cases = [
            (50, 2),   # 50 max HP -> 2 heal (5%)
            (100, 5),  # 100 max HP -> 5 heal (5%)
            (20, 1),   # 20 max HP -> 1 heal (5%)
        ]
        
        for max_hp, expected_heal in test_cases:
            with self.subTest(max_hp=max_hp):
                # Set player max HP and current HP
                self.player.max_hp = max_hp
                self.player.hp = max_hp - 10  # Damage player
                initial_hp = self.player.hp
                
                # Test healing dodge
                from monsters.goblin import Goblin
                goblin = Goblin(10, 10)
                dodge_context = AttackContext(
                    player=self.player,
                    attacker=goblin,
                    defender=self.player,
                    damage=0,
                    is_miss=True
                )
                self.emitter.emit(EventType.SUCCESSFUL_DODGE, dodge_context)
                
                actual_heal = self.player.hp - initial_hp
                self.assertEqual(actual_heal, expected_heal, 
                    f"Healing Dodge: Expected {expected_heal} heal, got {actual_heal}")
                
                # Reset and test vampire pendant
                self.player.hp = initial_hp
                death_context = DeathContext(
                    player=self.player,
                    monster=goblin,
                    experience_gained=10
                )
                self.emitter.emit(EventType.MONSTER_DEATH, death_context)
                
                actual_heal = self.player.hp - initial_hp
                self.assertEqual(actual_heal, expected_heal,
                    f"Vampire Pendant: Expected {expected_heal} heal, got {actual_heal}")
    
    def test_defensive_item_progression(self):
        """Test that defensive items scale appropriately."""
        wardens_tome = WardensTome(0, 0)
        skin_suit = SkinSuit(0, 0)
        
        # Subscribe items
        self.emitter.subscribe(EventType.LEVEL_UP, wardens_tome.on_event)
        self.emitter.subscribe(EventType.MONSTER_DEATH, skin_suit.on_event)
        
        # Test Warden's Tome progression
        initial_defense = self.player.defense
        
        # Level up 5 times
        for level in range(2, 7):
            context = LevelUpContext(
                player=self.player,
                new_level=level,
                stat_increases={"attack": 1}
            )
            self.emitter.emit(EventType.LEVEL_UP, context)
        
        # Should gain 5 defense from 5 level ups
        expected_defense = initial_defense + 5
        self.assertEqual(self.player.defense, expected_defense,
            f"Warden's Tome should give +5 DEF after 5 level ups")
        
        # Test Skin Suit progression (every 4 kills = +1 DEF)
        initial_bonus = skin_suit.get_defense_bonus(self.player)
        
        # Kill 12 monsters (should give +3 defense)
        from monsters.goblin import Goblin
        for i in range(12):
            goblin = Goblin(10, 10)
            context = DeathContext(
                player=self.player,
                monster=goblin,
                experience_gained=10
            )
            self.emitter.emit(EventType.MONSTER_DEATH, context)
        
        final_bonus = skin_suit.get_defense_bonus(self.player)
        expected_bonus = initial_bonus + 3  # 12 kills / 4 = 3
        self.assertEqual(final_bonus, expected_bonus,
            f"Skin Suit should give +3 DEF after 12 kills")
    
    def test_shield_item_balance(self):
        """Test that shield-granting items provide reasonable protection."""
        turtle_blessing = TurtlesBlessing(0, 0)
        protective_level = ProtectiveLevel(0, 0)
        
        # Subscribe items
        self.emitter.subscribe(EventType.FLOOR_CHANGE, turtle_blessing.on_event)
        self.emitter.subscribe(EventType.LEVEL_UP, protective_level.on_event)
        
        initial_shields = self.player.status_effects.shields
        
        # Test floor changes (every floor should give 1 shield)
        for floor in range(2, 6):  # Floors 2-5
            context = FloorContext(
                player=self.player,
                floor_number=floor,
                previous_floor=floor - 1
            )
            self.emitter.emit(EventType.FLOOR_CHANGE, context)
        
        expected_shields_floor = initial_shields + 4  # 4 floor changes
        self.assertEqual(self.player.status_effects.shields, expected_shields_floor,
            "Turtle's Blessing should give 1 shield per floor change")
        
        # Test level ups (every level should give 1 shield)
        for level in range(2, 5):  # Levels 2-4
            context = LevelUpContext(
                player=self.player,
                new_level=level,
                stat_increases={"attack": 1}
            )
            self.emitter.emit(EventType.LEVEL_UP, context)
        
        expected_shields_total = expected_shields_floor + 3  # +3 from level ups
        self.assertEqual(self.player.status_effects.shields, expected_shields_total,
            "Protective Level should give 1 shield per level up")
    
    def test_weapon_balance_curves(self):
        """Test weapon balance and power progression."""
        defender = Defender(0, 0)
        
        # Set as player weapon and subscribe
        self.player.weapon = defender
        self.emitter.subscribe(EventType.MONSTER_DEATH, defender.on_event)
        
        # Track progression
        initial_attack = defender.attack_bonus
        initial_defense = self.player.defense
        
        # Kill monsters until weapon reaches minimum attack
        kills = 0
        from monsters.goblin import Goblin
        while defender.attack_bonus > 1 and kills < 20:  # Safety limit
            goblin = Goblin(10, 10)
            context = DeathContext(
                player=self.player,
                monster=goblin,
                experience_gained=10
            )
            self.emitter.emit(EventType.MONSTER_DEATH, context)
            kills += 1
        
        # Defender should trade attack for defense
        attack_lost = initial_attack - defender.attack_bonus
        defense_gained = self.player.defense - initial_defense
        
        self.assertEqual(attack_lost, defense_gained,
            "Defender should trade attack for defense 1:1")
        self.assertGreaterEqual(defender.attack_bonus, 1,
            "Defender attack should never go below 1")
        
        # Test that further kills don't reduce attack below 1
        for _ in range(5):
            goblin = Goblin(10, 10)
            context = DeathContext(
                player=self.player,
                monster=goblin,
                experience_gained=10
            )
            self.emitter.emit(EventType.MONSTER_DEATH, context)
        
        self.assertEqual(defender.attack_bonus, 1,
            "Defender attack should stay at 1 after reaching minimum")
    
    def test_counter_attack_balance(self):
        """Test that counter-attack items are reasonably powerful but not overpowered."""
        holy_avenger = HolyAvenger(0, 0)
        backhand_blade = BackhandBlade(0, 0)
        
        # Set weapons and subscribe
        self.emitter.subscribe(EventType.MONSTER_ATTACK_PLAYER, holy_avenger.on_event)
        self.emitter.subscribe(EventType.SUCCESSFUL_DODGE, backhand_blade.on_event)
        
        # Mock random for predictable testing
        with patch('random.random', return_value=0.05):  # 5% chance - should trigger Holy Avenger
            # Test Holy Avenger counter-attack (10% chance)
            from monsters.goblin import Goblin
            goblin = Goblin(10, 10)
            goblin_initial_hp = goblin.hp
            
            # Set holy avenger as equipped weapon
            self.player.weapon = holy_avenger
            
            # Mock take_damage_with_traits to track counter-attacks
            with patch.object(goblin, 'take_damage_with_traits', return_value=5) as mock_damage:
                context = AttackContext(
                    player=self.player,
                    attacker=goblin,
                    defender=self.player,
                    damage=10  # Player takes damage
                )
                self.emitter.emit(EventType.MONSTER_ATTACK_PLAYER, context)
                
                # Counter-attack should have been triggered
                mock_damage.assert_called_once()
        
        # Test Backhand Blade counter-attack (always on dodge)
        from monsters.orc import Orc
        orc = Orc(10, 10)
        
        # Set backhand blade as equipped weapon
        self.player.weapon = backhand_blade
        
        with patch.object(orc, 'take_damage_with_traits', return_value=3) as mock_damage:
            context = AttackContext(
                player=self.player,
                attacker=orc,
                defender=self.player,
                damage=0,  # Player dodged
                is_miss=True
            )
            self.emitter.emit(EventType.SUCCESSFUL_DODGE, context)
            
            # Counter-attack should always trigger on dodge
            mock_damage.assert_called_once()
    
    def test_consumable_tracking_balance(self):
        """Test that consumable tracking items scale reasonably."""
        turban = PsychicsTurban(0, 0)
        
        # Subscribe item
        self.emitter.subscribe(EventType.PLAYER_CONSUME_ITEM, turban.on_event)
        
        # Test progression with different consumable counts
        test_scenarios = [
            (5, 5),    # 5 consumables -> +5 attack
            (15, 15),  # 15 consumables -> +15 attack
            (50, 50),  # 50 consumables -> +50 attack (high-end scenario)
        ]
        
        for consumables_used, expected_bonus in test_scenarios:
            with self.subTest(consumables_used=consumables_used):
                # Reset counters
                self.player.consumable_count = 0
                turban.consumable_counter = 0
                
                # Simulate using consumables
                from items.consumables.health_potion import HealthPotion
                for _ in range(consumables_used):
                    potion = HealthPotion(0, 0)
                    context = ConsumeContext(
                        player=self.player,
                        item_type="HealthPotion",
                        item=potion
                    )
                    self.emitter.emit(EventType.PLAYER_CONSUME_ITEM, context)
                
                # Check attack bonus
                bonus = turban.get_attack_bonus(self.player)
                self.assertEqual(bonus, expected_bonus,
                    f"Psychic's Turban should give +{expected_bonus} attack after {consumables_used} consumables")
    
    def test_xp_cost_vs_power_balance(self):
        """Test that XP costs are appropriate for item power levels."""
        items_and_costs = [
            (HealingDodge(0, 0), 10),
            (VampiresPendant(0, 0), 15),
            (WardensTome(0, 0), 25),
            (TurtlesBlessing(0, 0), 15),
            (ProtectiveLevel(0, 0), 20),
            (Defender(0, 0), 20),
            (HolyAvenger(0, 0), 30),
            (BackhandBlade(0, 0), 25),
        ]
        
        for item, expected_cost in items_and_costs:
            with self.subTest(item=item.name):
                self.assertEqual(item.xp_cost, expected_cost,
                    f"{item.name} should cost {expected_cost} XP")
                
                # Ensure player can afford it at reasonable levels
                # Level 2 player should have ~30-40 XP available
                test_player = Player(5, 5)
                test_player.xp = 40
                
                if expected_cost <= 30:
                    self.assertTrue(item.can_equip(test_player),
                        f"{item.name} should be affordable by level 2 player")
    
    def test_item_synergy_balance(self):
        """Test that item combinations are powerful but not game-breaking."""
        # Test healing synergy
        healing_dodge = HealingDodge(0, 0)
        vampire_pendant = VampiresPendant(0, 0)
        
        self.player.accessories.append(healing_dodge)
        self.player.accessories.append(vampire_pendant)
        
        self.emitter.subscribe(EventType.SUCCESSFUL_DODGE, healing_dodge.on_event)
        self.emitter.subscribe(EventType.MONSTER_DEATH, vampire_pendant.on_event)
        
        # Simulate combat with both dodge and kill
        self.player.hp = 30
        initial_hp = self.player.hp
        
        from monsters.goblin import Goblin
        goblin = Goblin(10, 10)
        
        # Player dodges attack (heals from dodge)
        dodge_context = AttackContext(
            player=self.player,
            attacker=goblin,
            defender=self.player,
            damage=0,
            is_miss=True
        )
        self.emitter.emit(EventType.SUCCESSFUL_DODGE, dodge_context)
        
        # Player kills monster (heals from kill)
        death_context = DeathContext(
            player=self.player,
            monster=goblin,
            experience_gained=10
        )
        self.emitter.emit(EventType.MONSTER_DEATH, death_context)
        
        # Total healing should be 10% max HP (5% each, but rounded down individually)
        total_heal = self.player.hp - initial_hp
        expected_heal = int(self.player.max_hp * 0.05) * 2  # Two separate 5% heals
        self.assertEqual(total_heal, expected_heal,
            f"Healing synergy should provide {expected_heal} HP total (2x{int(self.player.max_hp * 0.05)})")
        
        # Ensure healing doesn't exceed max HP
        self.assertLessEqual(self.player.hp, self.player.max_hp,
            "Healing should not exceed max HP")
    
    def test_edge_case_balance(self):
        """Test edge cases to ensure items don't break game balance."""
        # Test very low HP healing
        healing_dodge = HealingDodge(0, 0)
        self.emitter.subscribe(EventType.SUCCESSFUL_DODGE, healing_dodge.on_event)
        
        # Test with minimum possible HP
        self.player.max_hp = 1
        self.player.hp = 0  # At death's door
        
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
        
        # Even with 1 max HP, should heal at least 0 (int(1 * 0.05) = 0)
        self.assertGreaterEqual(self.player.hp, 0,
            "Healing should never make HP negative")
        
        # Test shield stacking limits
        turtle_blessing = TurtlesBlessing(0, 0)
        self.emitter.subscribe(EventType.FLOOR_CHANGE, turtle_blessing.on_event)
        
        # Simulate many floor changes
        for floor in range(2, 102):  # 100 floor changes
            context = FloorContext(
                player=self.player,
                floor_number=floor,
                previous_floor=floor - 1
            )
            self.emitter.emit(EventType.FLOOR_CHANGE, context)
        
        # Shields should accumulate (no artificial limit in current design)
        self.assertEqual(self.player.status_effects.shields, 100,
            "Turtle's Blessing should accumulate shields without limit")


if __name__ == '__main__':
    unittest.main(verbosity=2)