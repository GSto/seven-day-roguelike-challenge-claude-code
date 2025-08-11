"""
Tests for the new items implemented from plans/new_items.md
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items.consumables import PowerCatalyst, DefenseCatalyst, D6
from items.weapons import BrightSword, ClericsStaff
from items.armor import SpikedArmor


def test_power_catalyst():
    """Test that Power Catalyst permanently increases attack."""
    player = Player(5, 5)
    catalyst = PowerCatalyst(0, 0)
    
    initial_attack = player.attack
    result, msg = catalyst.use(player)
    
    assert result == True
    assert player.attack == initial_attack + 1, f"Expected attack {initial_attack + 1}, got {player.attack}"
    print("✓ Power Catalyst increases attack by 1")


def test_defense_catalyst():
    """Test that Defense Catalyst permanently increases defense."""
    player = Player(5, 5)
    catalyst = DefenseCatalyst(0, 0)
    
    initial_defense = player.defense
    result, msg = catalyst.use(player)
    
    assert result == True
    assert player.defense == initial_defense + 1, f"Expected defense {initial_defense + 1}, got {player.defense}"
    print("✓ Defense Catalyst increases defense by 1")


def test_d6_effects():
    """Test that D6 provides one of the expected random effects."""
    import random
    
    # Test multiple rolls to see different effects
    effects_seen = set()
    for i in range(50):  # Run enough tests to likely see all effects
        player = Player(5, 5)
        d6 = D6(0, 0)
        
        # Store initial values
        initial_attack = player.attack
        initial_defense = player.defense
        initial_max_hp = player.max_hp
        initial_fov = player.fov
        initial_hp = player.hp
        
        result, msg = d6.use(player)
        assert result == True
        
        # Check which effect occurred
        if player.attack > initial_attack:
            effects_seen.add("attack_boost")
        elif player.defense > initial_defense:
            effects_seen.add("defense_boost")
        elif player.max_hp > initial_max_hp:
            effects_seen.add("hp_boost")
            # Should also heal when max HP increases
            assert player.hp > initial_hp, "HP should increase when max HP increases"
        elif player.fov > initial_fov:
            effects_seen.add("fov_boost")
        elif player.max_hp < initial_max_hp:
            effects_seen.add("hp_penalty")
            # HP should be capped to max HP
            assert player.hp <= player.max_hp, "HP should not exceed max HP"
    
    # We should see at least some different effects over 50 rolls
    assert len(effects_seen) >= 3, f"Expected to see multiple effects, only saw: {effects_seen}"
    print("✓ D6 provides various random effects")

def test_d6_hp_penalty_safety():
    """Test that D6's HP penalty doesn't kill the player."""
    player = Player(5, 5)
    player.max_hp = 25  # Set to minimum safe threshold
    player.hp = 25
    
    d6 = D6(0, 0)
    
    # Force the HP penalty effect (this is a bit hacky but ensures we test the safety)
    import random
    original_randint = random.randint
    
    def mock_randint(a, b):
        return 5  # Force the HP penalty effect
    
    random.randint = mock_randint
    
    try:
        result, msg = d6.use(player)
        # With max_hp = 25, the HP penalty should not trigger
        assert player.max_hp == 25, "HP penalty should not trigger when max_hp <= 25"
        assert result == True
    finally:
        random.randint = original_randint
    
    print("✓ D6 HP penalty has safety mechanism")


if __name__ == "__main__":
    test_power_catalyst()
    test_defense_catalyst() 
    test_d6_effects()
    test_d6_hp_penalty_safety()
    print("✅ All new item tests passed!")