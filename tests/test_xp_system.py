"""
Unit tests for the XP system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from monster import Skeleton, Orc
from game import Game
from level import Level


def test_player_gain_xp():
    """Test that player gains XP correctly."""
    player = Player(x=10, y=10)
    
    # Check initial XP
    assert player.xp == 0
    assert player.level == 1
    assert player.xp_to_next == 50
    
    # Gain some XP
    player.gain_xp(25)
    assert player.xp == 25
    assert player.level == 1  # Should not level up yet
    
    # Gain more XP (but still shouldn't auto-level with manual leveling)
    player.gain_xp(30)  # Total 55 XP, more than 50 needed
    assert player.xp == 55
    assert player.level == 1  # Should not auto-level up
    assert player.can_level_up()  # But should be able to level up manually
    
    print("✓ Basic XP gain works correctly")


def test_player_level_up():
    """Test that player levels up manually when reaching XP threshold."""
    player = Player(x=10, y=10)
    
    # Store initial stats
    initial_max_hp = player.max_hp
    initial_attack = player.attack
    initial_defense = player.defense
    initial_hp = player.hp
    
    # Gain enough XP to level up
    player.gain_xp(50)
    
    # Should not auto-level up
    assert player.level == 1
    assert player.xp == 50
    assert player.can_level_up()
    
    # Manual level up
    result = player.attempt_level_up()
    assert result == True
    
    # Check that player leveled up
    assert player.level == 2
    assert player.xp == 0  # XP should be reset
    assert player.xp_to_next == 70  # Should be 1.3x previous (50 * 1.3)
    
    # Check stat increases - level 2 is even, so attack should increase
    hp_gained = int(initial_max_hp * 1.2) - initial_max_hp
    assert player.max_hp == int(initial_max_hp * 1.2)
    assert player.attack == initial_attack + 1  # Even level increases attack
    assert player.defense == initial_defense  # Defense unchanged at even level
    
    # Should heal for HP gained without going over max HP
    hp_gained = int(initial_max_hp * 1.2) - initial_max_hp
    expected_hp = min(initial_hp + hp_gained, player.max_hp)
    assert player.hp == expected_hp
    
    print("✓ Player manual level up works correctly")


def test_multiple_level_ups():
    """Test gaining enough XP for multiple level ups requires multiple manual level ups."""
    player = Player(x=10, y=10)
    
    # Gain massive XP (enough for multiple levels: 50 + 75 = 125)
    player.gain_xp(125)
    
    # Should not auto-level up
    assert player.level == 1
    assert player.can_level_up()
    
    # Manual level up to level 2
    player.attempt_level_up()
    assert player.level == 2
    assert player.xp == 75  # 125 - 50 = 75
    assert player.can_level_up()  # Can level up again
    
    # Manual level up to level 3
    xp_needed_for_level_3 = player.xp_to_next
    player.attempt_level_up()
    assert player.level == 3
    expected_xp = 75 - xp_needed_for_level_3  # Remaining XP after level up
    assert player.xp == expected_xp
    assert player.xp < player.xp_to_next  # Should not be able to level up again
    
    print(f"✓ Multiple manual level ups work correctly - reached level {player.level}")


def test_alternating_power_defense():
    """Test that level ups alternate between increasing attack and defense."""
    player = Player(x=10, y=10)
    
    initial_attack = player.attack
    initial_defense = player.defense
    
    # Level up to 2 (even) - should increase attack
    player.gain_xp(50)
    player.attempt_level_up()
    assert player.level == 2
    assert player.attack == initial_attack + 1
    assert player.defense == initial_defense
    
    # Level up to 3 (odd) - should increase defense
    player.gain_xp(player.xp_to_next)
    player.attempt_level_up()
    assert player.level == 3
    assert player.attack == initial_attack + 1  # Still same as level 2
    assert player.defense == initial_defense + 1
    
    # Level up to 4 (even) - should increase attack again
    player.gain_xp(player.xp_to_next)
    player.attempt_level_up()
    assert player.level == 4
    assert player.attack == initial_attack + 2  # +1 from level 2, +1 from level 4
    assert player.defense == initial_defense + 1  # Still same as level 3
    
    print("✓ Alternating power/defense increases work correctly")


def test_level_up_healing():
    """Test that level up heals for HP gained without exceeding max HP."""
    player = Player(x=10, y=10)
    
    # Damage the player first
    initial_max_hp = player.max_hp
    player.take_damage(30)  # Reduce HP
    damaged_hp = player.hp
    
    # Level up
    player.gain_xp(50)
    player.attempt_level_up()
    
    # Calculate expected healing based on HP gained
    new_max_hp = player.max_hp
    hp_gained = new_max_hp - initial_max_hp
    expected_hp = min(damaged_hp + hp_gained, new_max_hp)
    
    assert player.hp == expected_hp
    assert player.hp <= player.max_hp  # Should never exceed max HP
    
    print("✓ Level up healing works correctly without exceeding max HP")


def test_monster_xp_values():
    """Test that monsters have correct XP values."""
    goblin = Skeleton(5, 5)
    orc = Orc(5, 5)
    
    assert goblin.xp_value == 10
    assert orc.xp_value == 20
    
    print("✓ Monsters have correct XP values")


def test_combat_xp_integration():
    """Test XP gain through combat simulation."""
    # Create game components
    player = Player(x=10, y=10)
    goblin = Skeleton(x=11, y=10)
    
    # Simulate combat - goblin should die (player has 10 attack, goblin has 15 HP, 0 defense)
    initial_xp = player.xp
    
    # Attack goblin until it dies
    attacks_needed = (goblin.hp + player.get_total_attack() - 1) // player.get_total_attack()  # Ceiling division
    
    for _ in range(attacks_needed):
        damage = player.get_total_attack()
        goblin.take_damage(damage)
        
        if not goblin.is_alive():
            # Monster died, player should gain XP
            player.gain_xp(goblin.xp_value)
            break
    
    # Check that player gained XP
    assert player.xp == initial_xp + goblin.xp_value
    assert not goblin.is_alive()
    
    print(f"✓ Combat XP integration works - gained {goblin.xp_value} XP")


def run_all_tests():
    """Run all XP system tests."""
    print("Running XP system tests...")
    print()
    
    test_player_gain_xp()
    test_player_level_up()
    test_multiple_level_ups()
    test_alternating_power_defense()
    test_level_up_healing()
    test_monster_xp_values()
    test_combat_xp_integration()
    
    print()
    print("✅ All XP system tests passed!")


if __name__ == "__main__":
    run_all_tests()