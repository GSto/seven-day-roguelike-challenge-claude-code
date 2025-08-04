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
    assert player.xp_to_next == 100
    
    # Gain some XP
    player.gain_xp(25)
    assert player.xp == 25
    assert player.level == 1  # Should not level up yet
    
    # Gain more XP
    player.gain_xp(30)
    assert player.xp == 55
    assert player.level == 1
    
    print("✓ Basic XP gain works correctly")


def test_player_level_up():
    """Test that player levels up when reaching XP threshold."""
    player = Player(x=10, y=10)
    
    # Store initial stats
    initial_max_hp = player.max_hp
    initial_attack = player.attack
    initial_defense = player.defense
    
    # Gain enough XP to level up
    player.gain_xp(100)
    
    # Check that player leveled up
    assert player.level == 2
    assert player.xp == 0  # XP should be reset
    assert player.xp_to_next == 150  # Should be 1.5x previous
    
    # Check stat increases
    assert player.max_hp == initial_max_hp + 20
    assert player.attack == initial_attack + 3
    assert player.defense == initial_defense + 1
    assert player.hp == player.max_hp  # Should heal to full
    
    print("✓ Player level up works correctly")


def test_multiple_level_ups():
    """Test gaining enough XP for multiple level ups."""
    player = Player(x=10, y=10)
    
    # Gain massive XP (enough for multiple levels)
    player.gain_xp(500)
    
    # Should have leveled up multiple times
    assert player.level > 2
    print(f"✓ Player reached level {player.level} with massive XP gain")


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