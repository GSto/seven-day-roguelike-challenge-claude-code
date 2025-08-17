"""
Test monster distribution across levels to ensure correct spawning.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from monsters import create_monster_for_level, Skeleton, Orc, Troll, Devil


def test_level_9_no_devils():
    """Test that level 9 never spawns devils."""
    # Test many iterations to ensure no devils spawn on level 9
    devil_count = 0
    total_tests = 100
    
    for _ in range(total_tests):
        monster_class = create_monster_for_level(9)
        if monster_class == Devil:
            devil_count += 1
    
    # Level 9 should NEVER spawn devils
    assert devil_count == 0, f"Level 9 spawned {devil_count} devils out of {total_tests} attempts"
    
    print("✓ Level 9 never spawns devils")


def test_level_10_only_devils():
    """Test that level 10 always spawns devils."""
    devil_count = 0
    total_tests = 100
    
    for _ in range(total_tests):
        monster_class = create_monster_for_level(10)
        if monster_class == Devil:
            devil_count += 1
    
    # Level 10 should ALWAYS spawn devils
    assert devil_count == total_tests, f"Level 10 spawned {devil_count} devils out of {total_tests} attempts"
    
    print("✓ Level 10 always spawns devils")


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
            # Early levels: only Skeletons and Zombies
            assert 'Devil' not in monster_counts
            assert 'Troll' not in monster_counts
            assert 'Skeleton' in monster_counts or 'Zombie' in monster_counts
            
        elif level <= 5:
            # Mid levels: Orcs, Goblins, and Trolls
            assert 'Devil' not in monster_counts
            
        elif level <= 9:
            # Later levels: Goblins, Trolls, and Horrors (NO DEVILS)
            assert 'Devil' not in monster_counts, f"Level {level} should not spawn devils but got {monster_counts}"
            assert any(monster in monster_counts for monster in ['Goblin', 'Troll', 'Horror'])
            
        elif level == 10:
            # Final level: only Devils
            assert monster_counts.get('Devil', 0) == total_tests
            assert len(monster_counts) == 1  # Only devils
    
    print("✓ All levels have correct monster distribution")


def test_specific_level_checks():
    """Test specific level monster spawning rules."""
    # Test level 8 - should be Goblins, Trolls, and Horrors only
    level_8_monsters = set()
    for _ in range(50):
        monster_class = create_monster_for_level(8)
        level_8_monsters.add(monster_class.__name__)
    
    assert 'Devil' not in level_8_monsters
    assert any(monster in level_8_monsters for monster in ['Goblin', 'Troll', 'Horror'])
    print("✓ Level 8 spawns correct monsters (no devils)")
    
    # Test level 9 - should be Goblins, Trolls, and Horrors only
    level_9_monsters = set()
    for _ in range(50):
        monster_class = create_monster_for_level(9)
        level_9_monsters.add(monster_class.__name__)
    
    assert 'Devil' not in level_9_monsters
    assert any(monster in level_9_monsters for monster in ['Goblin', 'Troll', 'Horror'])
    print("✓ Level 9 spawns correct monsters (no devils)")
    
    # Test level 10 - should be Devils only
    level_10_monsters = set()
    for _ in range(50):
        monster_class = create_monster_for_level(10)
        level_10_monsters.add(monster_class.__name__)
    
    assert level_10_monsters == {'Devil'}
    print("✓ Level 10 spawns only devils")


def run_all_tests():
    """Run all monster level distribution tests."""
    print("Running monster level distribution tests...")
    print()
    
    test_level_9_no_devils()
    test_level_10_only_devils()
    test_level_distribution()
    test_specific_level_checks()
    
    print()
    print("✅ All monster level distribution tests passed!")


if __name__ == "__main__":
    run_all_tests()