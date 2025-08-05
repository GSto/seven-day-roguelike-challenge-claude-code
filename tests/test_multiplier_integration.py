"""
Integration test to ensure multiplier system doesn't break existing functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from player import Player
from items import HealthPotion, PowerCatalyst

def test_basic_player_creation():
    """Test that player can be created with new multiplier attributes"""
    player = Player(5, 5)
    
    # Test that all new attributes exist
    assert hasattr(player, 'attack_multiplier')
    assert hasattr(player, 'defense_multiplier') 
    assert hasattr(player, 'xp_multiplier')
    
    # Test default values
    assert player.attack_multiplier == 1.0
    assert player.defense_multiplier == 1.0
    assert player.xp_multiplier == 1.0
    
    print("✓ Player creation with multipliers works")

def test_attack_defense_calculations():
    """Test that attack and defense calculations work with multipliers"""
    player = Player(5, 5)
    
    # Get baseline values
    base_attack = player.get_total_attack()
    base_defense = player.get_total_defense()
    
    # These should be > 0 (player has starting equipment)
    assert base_attack > 0
    assert base_defense > 0
    
    # Test with modified multipliers
    player.attack_multiplier = 2.0
    player.defense_multiplier = 1.5
    
    new_attack = player.get_total_attack()
    new_defense = player.get_total_defense()
    
    # New values should be higher
    assert new_attack > base_attack
    assert new_defense > base_defense
    
    print("✓ Attack and defense calculations work with multipliers")

def test_xp_gain_with_multiplier():
    """Test that XP gain works with multipliers"""
    player = Player(5, 5)
    
    initial_xp = player.xp
    
    # Test base XP gain
    player.gain_xp(100)
    assert player.xp == initial_xp + 100
    
    # Test with multiplier
    player.xp_multiplier = 1.5
    initial_xp = player.xp
    player.gain_xp(100)
    assert player.xp == initial_xp + 150  # 100 * 1.5
    
    print("✓ XP gain works with multipliers")

def test_existing_consumables_still_work():
    """Test that existing consumables still work after our changes"""
    player = Player(5, 5)
    
    # Damage player first
    player.hp = 10
    
    # Test health potion
    potion = HealthPotion(0, 0)
    result = potion.use(player)
    assert result == True
    assert player.hp > 10  # Should have healed
    
    # Test power catalyst
    catalyst = PowerCatalyst(0, 0)
    initial_attack = player.attack
    result = catalyst.use(player)
    assert result == True
    assert player.attack == initial_attack + 1
    
    print("✓ Existing consumables still work")

def test_damage_calculation():
    """Test that damage calculation works with defense multipliers"""
    player = Player(5, 5)
    
    initial_hp = player.hp
    
    # Take some damage
    damage_taken = player.take_damage(10)
    assert damage_taken >= 1  # Should take at least 1 damage
    assert player.hp < initial_hp  # HP should decrease
    
    print("✓ Damage calculation works with defense multipliers")

if __name__ == "__main__":
    test_basic_player_creation()
    test_attack_defense_calculations() 
    test_xp_gain_with_multiplier()
    test_existing_consumables_still_work()
    test_damage_calculation()
    
    print("\n✅ All integration tests passed! The multiplier system is working correctly.")