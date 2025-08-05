"""
Unit tests for the XP system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from monster import Goblin, Orc
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
    assert player.xp_to_next == 75  # Should be 1.5x previous (50 * 1.5)
    
    # Check stat increases
    assert player.max_hp == initial_max_hp + 20
    assert player.attack == initial_attack + 3
    assert player.defense == initial_defense + 1
    assert player.hp == player.max_hp  # Should heal to full
    
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
    player.attempt_level_up()
    assert player.level == 3
    assert player.xp == 0  # 75 - 75 = 0
    assert not player.can_level_up()  # Can't level up again
    
    print(f"✓ Multiple manual level ups work correctly - reached level {player.level}")


def test_monster_xp_values():
    """Test that monsters have correct XP values."""
    goblin = Goblin(5, 5)
    orc = Orc(5, 5)
    
    assert goblin.xp_value == 10
    assert orc.xp_value == 20
    
    print("✓ Monsters have correct XP values")


def test_combat_xp_integration():
    """Test XP gain through combat simulation."""
    # Create game components
    player = Player(x=10, y=10)
    goblin = Goblin(x=11, y=10)
    
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
    test_monster_xp_values()
    test_combat_xp_integration()
    
    print()
    print("✅ All XP system tests passed!")


if __name__ == "__main__":
    run_all_tests()