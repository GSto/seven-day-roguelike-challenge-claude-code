"""
Tests for the three bug fixes:
1. FOV bonus of headlamp affecting display (equipment FOV update)
2. Spiked armor attack bonus 
3. Dragons only spawning on level 10
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items.accessories import HeadLamp
from items.armor import SpikedArmor
from monsters import create_monster_for_level, Devil
from game import Game


def test_headlamp_fov_calculation():
    """Test that HeadLamp FOV bonus is calculated correctly."""
    player = Player(5, 5)
    headlamp = HeadLamp(0, 0)
    
    base_fov = player.get_total_fov()
    assert base_fov == 10, f"Expected base FOV 10, got {base_fov}"
    
    player.accessories.append(headlamp)
    fov_with_headlamp = player.get_total_fov()
    
    assert fov_with_headlamp == 15, f"Expected FOV 15 with headlamp, got {fov_with_headlamp}"
    print("✓ HeadLamp FOV bonus calculated correctly")


def test_spiked_armor_stats():
    """Test that Spiked Armor provides both defense and attack bonuses."""
    player = Player(5, 5)
    spiked_armor = SpikedArmor(0, 0)
    
    # Check armor attributes
    assert spiked_armor.defense_bonus == 1, f"Expected defense bonus 1, got {spiked_armor.defense_bonus}"
    assert spiked_armor.attack_bonus == 2, f"Expected attack bonus 2, got {spiked_armor.attack_bonus}"
    
    # Test when equipped
    base_attack = player.attack  # Raw attack without equipment
    base_defense = player.defense  # Raw defense without equipment
    
    player.armor = spiked_armor
    
    total_attack = player.get_total_attack()
    total_defense = player.get_total_defense()
    
    # Account for starting weapon (+1 attack)
    expected_attack = base_attack + 1 + 2  # base + starting weapon + spiked armor
    expected_defense = base_defense + 1  # base + spiked armor
    
    assert total_attack == expected_attack, f"Expected total attack {expected_attack}, got {total_attack}"
    assert total_defense == expected_defense, f"Expected total defense {expected_defense}, got {total_defense}"
    print("✓ Spiked Armor provides +1 defense and +2 attack")


def test_devil_spawning_levels():
    """Test that devils only spawn on level 10, not level 9."""
    # Test level 9 - should NOT spawn dragons
    level_9_monsters = set()
    for _ in range(100):  # Test many spawns
        monster_class = create_monster_for_level(9)
        level_9_monsters.add(monster_class.__name__)
    
    assert 'Devil' not in level_9_monsters, f"Devils found on level 9: {level_9_monsters}"
    print(f"Level 9 monsters: {level_9_monsters}")
    
    # Test level 10 - should ONLY spawn dragons
    level_10_monsters = set()
    for _ in range(50):  # Test many spawns
        monster_class = create_monster_for_level(10)
        level_10_monsters.add(monster_class.__name__)
    
    assert level_10_monsters == {'Devil'}, f"Expected only Devils on level 10, got: {level_10_monsters}"
    print(f"Level 10 monsters: {level_10_monsters}")
    
    print("✓ Devils only spawn on level 10")


def test_level_progression_monsters():
    """Test monster progression across all levels."""
    for level in range(1, 11):
        monsters = set()
        for _ in range(20):
            monster_class = create_monster_for_level(level)
            monsters.add(monster_class.__name__)
        
        print(f"Level {level}: {sorted(monsters)}")
        
        # Verify no devils appear before level 10
        if level < 10:
            assert 'Devil' not in monsters, f"Devil found on level {level}"
        else:
            assert monsters == {'Devil'}, f"Expected only Devils on level 10, got {monsters}"
    
    print("✓ Monster progression works correctly across all levels")


def test_game_integration_fov_update():
    """Test that FOV updates work in game context (integration test)."""
    game = Game()
    player = game.player
    
    # Create headlamp and add to inventory
    headlamp = HeadLamp(player.x, player.y)
    player.add_item(headlamp)
    
    # Initial FOV should be base value
    initial_fov = player.get_total_fov()
    assert initial_fov == 10, f"Expected initial FOV 10, got {initial_fov}"
    
    # Equip headlamp directly to accessories (the new system works correctly)
    player.accessories.append(headlamp)
    player.remove_item(headlamp)
    
    # FOV should now include bonus
    final_fov = player.get_total_fov()
    assert final_fov == 15, f"Expected FOV 15 after equipping headlamp, got {final_fov}"
    
    print("✓ Game integration FOV update works correctly")


if __name__ == "__main__":
    test_headlamp_fov_calculation()
    test_spiked_armor_stats()
    test_devil_spawning_levels()
    test_level_progression_monsters()
    test_game_integration_fov_update()
    print("✅ All bug fix tests passed!")