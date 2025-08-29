"""
Test for the specific bug where player can hit 0 HP and not die.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from monsters import Skeleton


def test_player_dies_at_exactly_zero_hp():
    """Test that player dies when HP reaches exactly 0."""
    player = Player(10, 10)
    
    # Set HP to exactly 0
    player.hp = 0
    print(f"Player HP: {player.hp}")
    print(f"Player is_alive(): {player.is_alive()}")
    assert not player.is_alive(), "Player should be dead at 0 HP!"
    
    print("✓ Player correctly dies at exactly 0 HP")


def test_player_dies_when_damage_brings_hp_to_zero():
    """Test that player dies when damage brings HP to exactly 0."""
    player = Player(10, 10)
    
    # Set HP to a known value
    player.hp = 10
    player.defense = 0  # Remove defense for predictable damage
    
    # Take exactly 10 damage
    actual_damage = player.take_damage(10)
    print(f"Damage taken: {actual_damage}")
    print(f"Player HP after damage: {player.hp}")
    print(f"Player is_alive(): {player.is_alive()}")
    
    assert player.hp == 0, f"HP should be exactly 0, but is {player.hp}"
    assert not player.is_alive(), "Player should be dead when damage brings HP to 0!"
    
    print("✓ Player correctly dies when damage brings HP to exactly 0")


def test_player_dies_with_trait_damage():
    """Test that player dies when trait damage brings HP to 0."""
    player = Player(10, 10)
    from traits import Trait
    
    # Set HP to a known value
    player.hp = 10
    player.defense = 0  # Remove defense for predictable damage
    player.weaknesses = [Trait.FIRE]  # Add weakness for extra damage
    
    # Take damage with fire trait (should be doubled due to weakness)
    actual_damage = player.take_damage_with_traits(5, [Trait.FIRE])
    print(f"Damage taken with trait: {actual_damage}")
    print(f"Player HP after trait damage: {player.hp}")
    print(f"Player is_alive(): {player.is_alive()}")
    
    assert player.hp == 0, f"HP should be 0, but is {player.hp}"
    assert not player.is_alive(), "Player should be dead when trait damage brings HP to 0!"
    
    print("✓ Player correctly dies when trait damage brings HP to 0")


def test_minimum_damage_can_kill():
    """Test that minimum damage (1) can kill a player at 1 HP."""
    player = Player(10, 10)
    
    # Set HP to 1
    player.hp = 1
    player.defense = 100  # High defense to trigger minimum damage
    
    # Take damage (should deal minimum 1 damage)
    actual_damage = player.take_damage(50)
    print(f"Minimum damage taken: {actual_damage}")
    print(f"Player HP after minimum damage: {player.hp}")
    print(f"Player is_alive(): {player.is_alive()}")
    
    assert actual_damage == 1, f"Should deal minimum 1 damage, but dealt {actual_damage}"
    assert player.hp == 0, f"HP should be 0, but is {player.hp}"
    assert not player.is_alive(), "Player should be dead when minimum damage brings HP to 0!"
    
    print("✓ Player correctly dies from minimum damage at 1 HP")


def test_hp_cannot_go_negative():
    """Test that HP is clamped at 0 and doesn't go negative."""
    player = Player(10, 10)
    
    # Set HP to low value
    player.hp = 5
    player.defense = 0
    
    # Take massive damage
    actual_damage = player.take_damage(1000)
    print(f"Massive damage taken: {actual_damage}")
    print(f"Player HP after massive damage: {player.hp}")
    
    assert player.hp == 0, f"HP should be clamped at 0, but is {player.hp}"
    assert player.hp >= 0, "HP should never be negative!"
    assert not player.is_alive(), "Player should be dead after massive damage!"
    
    print("✓ HP correctly clamped at 0 and doesn't go negative")


def test_exact_lethal_damage():
    """Test various scenarios of exact lethal damage."""
    scenarios = [
        (50, 50, 0),  # Full HP to 0
        (25, 25, 0),  # Half HP to 0
        (1, 1, 0),     # 1 HP to 0
        (100, 100, 0), # High HP to 0
    ]
    
    for initial_hp, damage, expected_hp in scenarios:
        player = Player(10, 10)
        player.hp = initial_hp
        player.max_hp = max(initial_hp, player.max_hp)
        player.defense = 0
        
        player.take_damage(damage)
        
        assert player.hp == expected_hp, f"Expected HP {expected_hp}, got {player.hp} (initial: {initial_hp}, damage: {damage})"
        assert not player.is_alive(), f"Player should be dead (HP: {player.hp})"
        print(f"  ✓ {initial_hp} HP - {damage} damage = {player.hp} HP (dead: {not player.is_alive()})")
    
    print("✓ All exact lethal damage scenarios work correctly")


def run_all_tests():
    """Run all zero HP death bug tests."""
    print("Testing zero HP death bug...")
    print()
    
    test_player_dies_at_exactly_zero_hp()
    test_player_dies_when_damage_brings_hp_to_zero()
    test_player_dies_with_trait_damage()
    test_minimum_damage_can_kill()
    test_hp_cannot_go_negative()
    test_exact_lethal_damage()
    
    print()
    print("✅ All zero HP death tests passed!")


if __name__ == "__main__":
    run_all_tests()