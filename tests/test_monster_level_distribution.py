"""
Test monster distribution across levels to ensure correct spawning.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from monster import create_monster_for_level, Skeleton, Orc, Troll, Dragon


def test_level_9_no_dragons():
    """Test that level 9 never spawns dragons."""
    # Test many iterations to ensure no dragons spawn on level 9
    dragon_count = 0
    total_tests = 100
    
    for _ in range(total_tests):
        monster_class = create_monster_for_level(9)
        if monster_class == Dragon:
            dragon_count += 1
    
    # Level 9 should NEVER spawn dragons
    assert dragon_count == 0, f"Level 9 spawned {dragon_count} dragons out of {total_tests} attempts"
    
    print("✓ Level 9 never spawns dragons")


def test_level_10_only_dragons():
    """Test that level 10 always spawns dragons."""
    dragon_count = 0
    total_tests = 100
    
    for _ in range(total_tests):
        monster_class = create_monster_for_level(10)
        if monster_class == Dragon:
            dragon_count += 1
    
    # Level 10 should ALWAYS spawn dragons
    assert dragon_count == total_tests, f"Level 10 spawned {dragon_count} dragons out of {total_tests} attempts"
    
    print("✓ Level 10 always spawns dragons")


def test_level_distribution():
    """Test monster distribution across all levels."""
    # Test each level's monster distribution
    for level in range(1, 11):
        monster_counts = {}
        total_tests = 100
        
        for _ in range(total_tests):
            monster_class = create_monster_for_level(level)
            monster_name = monster_class.__name__
            monster_counts[monster_name] = monster_counts.get(monster_name, 0) + 1
        
        print(f"Level {level}: {monster_counts}")
        
        # Verify level-specific rules
        if level <= 2:
            # Early levels: only Goblins and Orcs
            assert 'Dragon' not in monster_counts
            assert 'Troll' not in monster_counts
            assert 'Goblin' in monster_counts or 'Orc' in monster_counts
            
        elif level <= 5:
            # Mid levels: Goblins, Orcs, and Trolls
            assert 'Dragon' not in monster_counts
            
        elif level <= 9:
            # Later levels: Orcs and Trolls (NO DRAGONS)
            assert 'Dragon' not in monster_counts, f"Level {level} should not spawn dragons but got {monster_counts}"
            assert 'Orc' in monster_counts or 'Troll' in monster_counts
            
        elif level == 10:
            # Final level: only Dragons
            assert monster_counts.get('Dragon', 0) == total_tests
            assert len(monster_counts) == 1  # Only dragons
    
    print("✓ All levels have correct monster distribution")


def test_specific_level_checks():
    """Test specific level monster spawning rules."""
    # Test level 8 - should be Orcs and Trolls only
    level_8_monsters = set()
    for _ in range(50):
        monster_class = create_monster_for_level(8)
        level_8_monsters.add(monster_class.__name__)
    
    assert 'Dragon' not in level_8_monsters
    assert 'Orc' in level_8_monsters or 'Troll' in level_8_monsters
    print("✓ Level 8 spawns correct monsters (no dragons)")
    
    # Test level 9 - should be Orcs and Trolls only
    level_9_monsters = set()
    for _ in range(50):
        monster_class = create_monster_for_level(9)
        level_9_monsters.add(monster_class.__name__)
    
    assert 'Dragon' not in level_9_monsters
    assert 'Orc' in level_9_monsters or 'Troll' in level_9_monsters
    print("✓ Level 9 spawns correct monsters (no dragons)")
    
    # Test level 10 - should be Dragons only
    level_10_monsters = set()
    for _ in range(50):
        monster_class = create_monster_for_level(10)
        level_10_monsters.add(monster_class.__name__)
    
    assert level_10_monsters == {'Dragon'}
    print("✓ Level 10 spawns only dragons")


def run_all_tests():
    """Run all monster level distribution tests."""
    print("Running monster level distribution tests...")
    print()
    
    test_level_9_no_dragons()
    test_level_10_only_dragons()
    test_level_distribution()
    test_specific_level_checks()
    
    print()
    print("✅ All monster level distribution tests passed!")


if __name__ == "__main__":
    run_all_tests()