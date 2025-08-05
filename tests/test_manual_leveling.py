"""
Tests for the new manual leveling system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from game import Game


def test_manual_leveling_basic():
    """Test basic manual leveling functionality."""
    player = Player(5, 5)
    
    # Check initial state
    assert player.level == 1
    assert player.xp == 0
    assert player.xp_to_next == 50
    assert not player.can_level_up()
    
    # Give enough XP to level up
    player.gain_xp(50)
    
    # Should not auto-level
    assert player.level == 1
    assert player.xp == 50
    assert player.can_level_up()
    
    # Manual level up should work
    result = player.attempt_level_up()
    assert result == True
    assert player.level == 2
    assert player.xp == 0  # XP spent
    assert player.xp_to_next == 75  # Increased by 1.5x
    
    print("✓ Manual leveling basic functionality works")


def test_insufficient_xp_leveling():
    """Test that leveling fails with insufficient XP."""
    player = Player(5, 5)
    
    # Give some XP but not enough
    player.gain_xp(25)
    
    assert not player.can_level_up()
    
    # Attempt level up should fail
    result = player.attempt_level_up()
    assert result == False
    assert player.level == 1  # Still level 1
    assert player.xp == 25   # XP unchanged
    
    print("✓ Insufficient XP leveling properly fails")


def test_multiple_level_ups():
    """Test multiple level ups require multiple manual actions."""
    player = Player(5, 5)
    
    # Give enough XP for multiple levels (50 + 75 = 125 XP)
    player.gain_xp(125)
    
    # Should still be level 1 (no auto-leveling)
    assert player.level == 1
    assert player.can_level_up()
    
    # First manual level up
    result = player.attempt_level_up()
    assert result == True
    assert player.level == 2
    assert player.xp == 75  # 125 - 50 = 75 remaining
    
    # Should be able to level up again
    assert player.can_level_up()
    
    # Second manual level up
    result = player.attempt_level_up()
    assert result == True
    assert player.level == 3
    assert player.xp == 0  # 75 - 75 = 0 remaining
    
    print("✓ Multiple level ups work correctly")


def test_level_up_stat_increases():
    """Test that manual level up increases stats correctly."""
    player = Player(5, 5)
    
    # Record initial stats
    initial_hp = player.hp
    initial_max_hp = player.max_hp
    initial_attack = player.attack
    initial_defense = player.defense
    
    # Give XP and level up
    player.gain_xp(50)
    player.attempt_level_up()
    
    # Check stat increases
    assert player.max_hp == initial_max_hp + 20
    assert player.hp == player.max_hp  # Should heal to full
    assert player.attack == initial_attack + 3
    assert player.defense == initial_defense + 1
    
    print("✓ Level up stat increases work correctly")


def test_game_integration():
    """Test manual leveling integration with game system."""
    game = Game()
    player = game.player
    
    # Give player XP
    player.gain_xp(50)
    
    # Should be able to level up
    assert player.can_level_up()
    
    # Test the game's manual level up handler
    game.handle_manual_level_up()
    
    # Should have leveled up
    assert player.level == 2
    assert not player.can_level_up()
    
    print("✓ Game integration works correctly")


def test_xp_display_format():
    """Test that XP is displayed as a single value."""
    player = Player(5, 5)
    
    # Give some XP
    player.gain_xp(25)
    
    # Check that XP values are accessible for UI display
    assert player.xp == 25
    assert player.xp_to_next == 50
    assert player.level == 1
    
    # Test can_level_up method for UI highlighting
    assert not player.can_level_up()
    
    player.gain_xp(25)  # Total 50 XP
    assert player.can_level_up()
    
    print("✓ XP display format values work correctly")


if __name__ == "__main__":
    test_manual_leveling_basic()
    test_insufficient_xp_leveling()
    test_multiple_level_ups()
    test_level_up_stat_increases()
    test_game_integration()
    test_xp_display_format()
    print("✅ All manual leveling tests passed!")