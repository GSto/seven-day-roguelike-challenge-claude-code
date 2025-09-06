"""
Tests for new pickup items: Nickel, Penny, and Shell Token.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from items.pickups import Nickel, Penny, ShellToken
from player import Player


def test_nickel_initialization():
    """Test Nickel pickup initialization."""
    nickel = Nickel(10, 10)
    assert nickel.x == 10
    assert nickel.y == 10
    assert nickel.name == "Nickel"
    assert nickel.char == "¢"
    assert nickel.xp_amount == 5
    assert nickel.market_value == 0


def test_nickel_grants_xp():
    """Test that Nickel grants 5 XP when picked up."""
    player = Player(0, 0)
    initial_xp = player.xp
    
    nickel = Nickel(0, 0)
    success, message = nickel.on_pickup(player)
    
    assert success == True
    assert player.xp == initial_xp + 5
    assert "5 XP" in message
    assert "Nickel" in message


def test_nickel_with_xp_multiplier():
    """Test that Nickel respects XP multipliers."""
    player = Player(0, 0)
    player.xp_multiplier = 2.0  # 2x XP multiplier
    initial_xp = player.xp
    
    nickel = Nickel(0, 0)
    success, message = nickel.on_pickup(player)
    
    assert success == True
    assert player.xp == initial_xp + 10  # 5 * 2.0 multiplier
    assert "10 XP" in message  # Should show the multiplied amount


def test_penny_initialization():
    """Test Penny pickup initialization."""
    penny = Penny(5, 5)
    assert penny.x == 5
    assert penny.y == 5
    assert penny.name == "Penny"
    assert penny.char == "¢"
    assert penny.xp_amount == 1
    assert penny.market_value == 0


def test_penny_grants_xp():
    """Test that Penny grants 1 XP when picked up."""
    player = Player(0, 0)
    initial_xp = player.xp
    
    penny = Penny(0, 0)
    success, message = penny.on_pickup(player)
    
    assert success == True
    assert player.xp == initial_xp + 1
    assert "1 XP" in message
    assert "Penny" in message


def test_shell_token_initialization():
    """Test Shell Token pickup initialization."""
    shell_token = ShellToken(3, 7)
    assert shell_token.x == 3
    assert shell_token.y == 7
    assert shell_token.name == "Shell Token"
    assert shell_token.char == "○"
    assert shell_token.defense_amount == 1
    assert shell_token.market_value == 0


def test_shell_token_grants_defense():
    """Test that Shell Token grants +1 Defense when picked up."""
    player = Player(0, 0)
    initial_defense = player.stats.defense
    
    shell_token = ShellToken(0, 0)
    success, message = shell_token.on_pickup(player)
    
    assert success == True
    assert player.stats.defense == initial_defense + 1
    assert "Defense by 1" in message
    assert "Shell Token" in message


def test_shell_token_permanent_defense():
    """Test that Shell Token defense boost is permanent."""
    player = Player(0, 0)
    initial_defense = player.stats.defense
    
    # Pick up first Shell Token
    shell_token1 = ShellToken(0, 0)
    shell_token1.on_pickup(player)
    mid_defense = player.stats.defense
    
    # Pick up second Shell Token
    shell_token2 = ShellToken(1, 1)
    shell_token2.on_pickup(player)
    final_defense = player.stats.defense
    
    assert mid_defense == initial_defense + 1
    assert final_defense == initial_defense + 2
    # Defense should stack from multiple Shell Tokens


def test_xp_pickup_level_up():
    """Test that XP pickups can trigger level up."""
    player = Player(0, 0)
    # Set player close to leveling up
    player.xp = 48  # Needs 2 more XP to level up (xp_to_next = 50)
    initial_level = player.level
    
    # Pick up a Nickel (5 XP) - should cause level up
    nickel = Nickel(0, 0)
    success, message = nickel.on_pickup(player)
    
    print(f"Level up test message: '{message}'")
    assert success == True
    assert "level up" in message
    # Player should be able to level up after gaining XP


def test_different_pickup_types():
    """Test that pickups have different characteristics."""
    snackie_char = "Snackie"  # From previous implementation
    nickel = Nickel(0, 0)
    penny = Penny(0, 0)
    shell_token = ShellToken(0, 0)
    
    # All should have different names
    names = {nickel.name, penny.name, shell_token.name}
    assert len(names) == 3  # All unique
    
    # All should have same char (¢) except Shell Token
    assert nickel.char == penny.char == "¢"
    assert shell_token.char == "○"
    
    # All should have different colors
    colors = {nickel.color, penny.color, shell_token.color}
    assert len(colors) == 3  # All unique colors


if __name__ == "__main__":
    test_nickel_initialization()
    test_nickel_grants_xp()
    test_nickel_with_xp_multiplier()
    test_penny_initialization()
    test_penny_grants_xp()
    test_shell_token_initialization()
    test_shell_token_grants_defense()
    test_shell_token_permanent_defense()
    test_xp_pickup_level_up()
    test_different_pickup_types()
    print("All new pickup tests passed!")