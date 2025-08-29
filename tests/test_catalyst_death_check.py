"""
Test that using catalysts properly checks for player death.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items.consumables.power_catalyst import PowerCatalyst
from items.consumables.defense_catalyst import DefenseCatalyst


def test_catalyst_prevents_suicide():
    """Test that catalysts prevent using them if it would kill the player."""
    player = Player(10, 10)
    catalyst = PowerCatalyst(0, 0)
    
    # Set player HP to low value
    player.hp = 5
    player.catalyst_tax = 0.1  # 10% tax
    
    # Calculate expected cost
    hp_cost = int(player.max_hp * player.catalyst_tax)
    print(f"Player HP: {player.hp}, Catalyst cost: {hp_cost}")
    
    # Try to use catalyst when it would kill us
    success, message = catalyst.use(player)
    
    print(f"Success: {success}")
    print(f"Message: {message}")
    print(f"Player HP after: {player.hp}")
    
    # Should fail and player should still be alive
    assert not success, "Catalyst should prevent usage when it would kill player"
    assert player.hp > 0, "Player HP should remain positive"
    assert player.is_alive(), "Player should still be alive"
    
    print("✓ Catalyst correctly prevents suicide")


def test_catalyst_hp_never_negative():
    """Test that catalyst HP cost never makes HP negative."""
    player = Player(10, 10)
    catalyst = DefenseCatalyst(0, 0)
    
    # Set player HP to exact cost + 1
    player.catalyst_tax = 0.1  # 10% tax
    hp_cost = int(player.max_hp * player.catalyst_tax)
    player.hp = hp_cost + 1  # Just enough to use it
    
    print(f"Player HP before: {player.hp}, Catalyst cost: {hp_cost}")
    
    # Use catalyst
    success, message = catalyst.use(player)
    
    print(f"Success: {success}")
    print(f"Player HP after: {player.hp}")
    
    # Should succeed and leave player at 1 HP
    assert success, "Catalyst should work when player has just enough HP"
    assert player.hp >= 0, "Player HP should never be negative"
    assert player.hp == 1, f"Player should have 1 HP left, but has {player.hp}"
    assert player.is_alive(), "Player should still be alive at 1 HP"
    
    print("✓ Catalyst HP cost never makes HP negative")


def test_catalyst_tax_increases():
    """Test that catalyst tax increases after each use."""
    player = Player(10, 10)
    catalyst1 = PowerCatalyst(0, 0)
    catalyst2 = DefenseCatalyst(0, 0)
    
    # Give player plenty of HP
    player.hp = player.max_hp = 100
    initial_tax = player.catalyst_tax
    
    print(f"Initial catalyst tax: {initial_tax * 100}%")
    
    # Use first catalyst
    success1, _ = catalyst1.use(player)
    tax_after_first = player.catalyst_tax
    
    print(f"Tax after first use: {tax_after_first * 100}%")
    
    # Use second catalyst
    success2, _ = catalyst2.use(player)
    tax_after_second = player.catalyst_tax
    
    print(f"Tax after second use: {tax_after_second * 100}%")
    
    assert success1 and success2, "Both catalysts should work"
    assert tax_after_first > initial_tax, "Tax should increase after first use"
    assert tax_after_second > tax_after_first, "Tax should increase after second use"
    assert tax_after_second == initial_tax + 0.10, "Tax should increase by 5% each time"
    
    print("✓ Catalyst tax increases correctly")


def test_catalyst_with_exact_hp():
    """Test edge cases with exact HP values."""
    scenarios = [
        (10, 1, 0.1),   # 10 HP, cost 1, should work
        (20, 2, 0.1),   # 20 HP, cost 2, should work
        (50, 5, 0.1),   # 50 HP, cost 5, should work
        (100, 10, 0.1), # 100 HP, cost 10, should work
    ]
    
    for max_hp, expected_cost, tax in scenarios:
        player = Player(10, 10)
        catalyst = PowerCatalyst(0, 0)
        
        player.max_hp = max_hp
        player.hp = expected_cost + 1  # Just enough HP
        player.catalyst_tax = tax
        
        success, _ = catalyst.use(player)
        
        assert success, f"Should work with {expected_cost + 1} HP and cost {expected_cost}"
        assert player.hp == 1, f"Should have 1 HP left, but has {player.hp}"
        assert player.is_alive(), "Player should be alive"
        
        print(f"  ✓ Max HP {max_hp}, cost {expected_cost}: player survives with 1 HP")
    
    print("✓ All exact HP scenarios work correctly")


def run_all_tests():
    """Run all catalyst death check tests."""
    print("Testing catalyst death checks...")
    print()
    
    test_catalyst_prevents_suicide()
    test_catalyst_hp_never_negative()
    test_catalyst_tax_increases()
    test_catalyst_with_exact_hp()
    
    print()
    print("✅ All catalyst death check tests passed!")


if __name__ == "__main__":
    run_all_tests()