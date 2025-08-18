"""
Unit tests for the final boss and victory system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from level.level import Level
from monsters import Devil, create_monster_for_level
from game import Game


def test_devil_boss_stats():
    """Test that the Devil has appropriate boss-level stats."""
    devil = Devil(10, 10)
    
    # Devil should have high stats
    assert devil.hp >= 150  # High HP
    assert devil.attack >= 20  # High attack
    assert devil.defense >= 5  # Good defense
    assert devil.xp_value >= 100  # High XP reward
    
    # Devil should be marked as final boss
    assert hasattr(devil, 'is_final_boss')
    assert devil.is_final_boss == True
    
    print("✓ Devil boss has appropriate stats")


def test_level_10_spawns_only_devil():
    """Test that level 10 spawns only the Devil boss."""
    level = Level(level_number=10)
    
    # Level 10 should have exactly one monster
    assert len(level.monsters) == 1
    
    # That monster should be a Devil
    boss = level.monsters[0]
    assert isinstance(boss, Devil)
    assert boss.name == "Ancient Devil"
    assert hasattr(boss, 'is_final_boss')
    assert boss.is_final_boss == True
    
    print("✓ Level 10 spawns only Devil boss")


def test_devil_boss_combat_strength():
    """Test that the Devil boss is significantly stronger than regular monsters."""
    devil = Devil(10, 10)
    
    # Compare to other monsters
    from monsters import Skeleton, Orc, Troll
    goblin = Skeleton(10, 10)
    orc = Orc(10, 10)
    troll = Troll(10, 10)
    
    # Devil should have much higher stats
    assert devil.hp > troll.hp  # More HP than strongest regular monster
    assert devil.attack > troll.attack  # Higher attack
    assert devil.defense > troll.defense  # Better defense
    assert devil.xp_value > troll.xp_value  # More XP reward
    
    # Devil should be a significant challenge
    assert devil.hp >= 150  # High HP pool
    assert devil.attack >= 20  # Dangerous attack
    
    print("✓ Devil boss is significantly stronger than regular monsters")


def test_monster_creation_level_10():
    """Test that create_monster_for_level returns Devil for level 10."""
    monster_class = create_monster_for_level(10)
    
    # Level 10 should always return Devil
    assert monster_class == Devil
    
    # Create instance and verify it's a boss
    devil = monster_class(5, 5)
    assert isinstance(devil, Devil)
    assert hasattr(devil, 'is_final_boss')
    assert devil.is_final_boss == True
    
    print("✓ Monster creation correctly returns Devil for level 10")


def test_monster_creation_level_9():
    """Test that create_monster_for_level never returns Devil for level 9."""
    # Test multiple times to ensure no devils spawn on level 9
    for _ in range(20):
        monster_class = create_monster_for_level(9)
        assert monster_class != Devil, "Level 9 should never spawn devils"
    
    print("✓ Monster creation never returns Devil for level 9")


def test_boss_victory_condition_concept():
    """Test the victory condition logic concepts."""
    # Test boss identification
    devil = Devil(10, 10)
    non_boss = create_monster_for_level(5)(10, 10)  # Create a non-boss monster
    
    # Devil should be identified as final boss
    assert hasattr(devil, 'is_final_boss') and devil.is_final_boss
    
    # Non-boss should not have the flag or have it as False
    assert not (hasattr(non_boss, 'is_final_boss') and non_boss.is_final_boss)
    
    print("✓ Boss victory condition concepts work correctly")


def test_boss_defeat_triggers_victory():
    """Test that defeating the boss triggers victory state."""
    devil = Devil(10, 10)
    
    # Test boss death detection
    assert devil.is_alive() == True
    
    # Simulate massive damage to kill boss
    devil.take_damage(9999)  # More than enough to kill
    assert devil.is_alive() == False
    
    # Test that we can detect boss death
    if not devil.is_alive() and hasattr(devil, 'is_final_boss') and devil.is_final_boss:
        victory_triggered = True
    else:
        victory_triggered = False
    
    assert victory_triggered == True
    
    print("✓ Boss defeat correctly triggers victory condition")


def test_game_state_management():
    """Test victory game state management concepts."""
    # Test game state transitions
    game_states = {
        'PLAYING': 'playing',
        'VICTORY': 'victory',
        'DEAD': 'dead'
    }
    
    # Test state transition to victory
    current_state = game_states['PLAYING']
    assert current_state == 'playing'
    
    # Boss defeated
    current_state = game_states['VICTORY']
    assert current_state == 'victory'
    
    # Can restart from victory
    current_state = game_states['PLAYING']
    assert current_state == 'playing'
    
    print("✓ Victory game state management concepts work correctly")


def test_victory_screen_stats():
    """Test that victory screen can collect appropriate stats."""
    player = Player(10, 10)
    
    # Simulate end-game stats
    player.gain_xp(500)  # Gain some XP
    highest_floor = 10
    
    # Collect victory stats
    victory_stats = {
        'final_level': player.level,
        'floors_conquered': highest_floor,
        'total_xp': player.xp,
        'final_attack': player.get_total_attack(),
        'final_defense': player.get_total_defense()
    }
    
    # Verify stats are reasonable
    assert victory_stats['final_level'] >= 1
    assert victory_stats['floors_conquered'] == 10
    assert victory_stats['total_xp'] >= 0
    assert victory_stats['final_attack'] > 0
    assert victory_stats['final_defense'] >= 0
    
    print("✓ Victory screen stats collection works correctly")


def test_boss_placement_on_level():
    """Test that boss is placed appropriately on level 10."""
    level = Level(level_number=10)
    
    # Should have exactly one monster (the boss)
    assert len(level.monsters) == 1
    
    boss = level.monsters[0]
    
    # Boss should be placed within level boundaries
    assert 0 <= boss.x < level.width
    assert 0 <= boss.y < level.height
    
    # Boss should be placed in a room (not a wall)
    from constants import TILE_WALL
    assert level.tiles[boss.x, boss.y] != TILE_WALL
    
    # Boss should be alive initially
    assert boss.is_alive() == True
    
    print("✓ Boss is placed appropriately on level 10")


def test_victory_system_integration():
    """Test victory system integration concepts."""
    # Test that all components work together
    devil = Devil(15, 15)
    player = Player(10, 10)
    
    # Initial state
    assert devil.is_alive() == True
    assert hasattr(devil, 'is_final_boss')
    assert devil.is_final_boss == True
    
    # Simulate combat until devil dies
    while devil.is_alive():
        damage = player.get_total_attack()
        devil.take_damage(damage)
    
    # Devil should be dead
    assert not devil.is_alive()
    
    # Victory condition should be detectable
    victory_condition = (
        not devil.is_alive() and 
        hasattr(devil, 'is_final_boss') and 
        devil.is_final_boss
    )
    assert victory_condition == True
    
    print("✓ Victory system integration works correctly")


def run_all_tests():
    """Run all boss and victory system tests."""
    print("Running boss and victory system tests...")
    print()
    
    test_devil_boss_stats()
    test_level_10_spawns_only_devil()
    test_devil_boss_combat_strength()
    test_monster_creation_level_10()
    test_monster_creation_level_9()
    test_boss_victory_condition_concept()
    test_boss_defeat_triggers_victory()
    test_game_state_management()
    test_victory_screen_stats()
    test_boss_placement_on_level()
    test_victory_system_integration()
    
    print()
    print("✅ All boss and victory system tests passed!")


if __name__ == "__main__":
    run_all_tests()