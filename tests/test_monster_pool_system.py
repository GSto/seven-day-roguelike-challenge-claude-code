"""
Tests for the new monster pool management system.
"""

import sys
import os

# Add src to path for imports  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from monsters.pool import MonsterPool, MonsterSpec, create_monster_for_level, get_monster_pool
from monsters.skeleton import Skeleton
from monsters.zombie import Zombie
from monsters.orc import Orc
from monsters.phantom import Phantom
from monsters.goblin import Goblin
from monsters.troll import Troll
from monsters.horror import Horror
from monsters.angel import Angel
from monsters.devil import Devil


class TestMonsterSpec:
    """Test the MonsterSpec dataclass."""
    
    def test_monster_spec_creation(self):
        """Test creating a MonsterSpec."""
        spec = MonsterSpec(Skeleton, 1.0, 1, 5, 0.8)
        assert spec.monster_class == Skeleton
        assert spec.difficulty_rating == 1.0
        assert spec.min_level == 1
        assert spec.max_level == 5
        assert spec.rarity == 0.8
        assert spec.boss_only == False
        
    def test_boss_monster_spec(self):
        """Test creating a boss MonsterSpec."""
        spec = MonsterSpec(Devil, 10.0, 10, 10, 1.0, boss_only=True)
        assert spec.boss_only == True


class TestMonsterPool:
    """Test the MonsterPool class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pool = MonsterPool()
    
    def test_monster_pool_initialization(self):
        """Test that the monster pool initializes correctly."""
        pool = MonsterPool()
        
        # Should have all monster types
        monster_classes = [spec.monster_class for spec in pool.monsters]
        expected_classes = [Skeleton, Zombie, Orc, Phantom, Goblin, Troll, Horror, Angel, Devil]
        
        for expected_class in expected_classes:
            assert expected_class in monster_classes, f"{expected_class.__name__} not found in monster pool"
    
    def test_get_available_monsters_early_level(self):
        """Test getting available monsters for early levels."""
        pool = MonsterPool()
        
        # Level 1 should only have Skeleton and Zombie
        available = pool.get_available_monsters(1)
        available_classes = [spec.monster_class for spec in available]
        
        assert Skeleton in available_classes
        assert Zombie in available_classes
        assert Orc not in available_classes
        assert Devil not in available_classes
    
    def test_get_available_monsters_mid_level(self):
        """Test getting available monsters for mid levels."""
        pool = MonsterPool()
        
        # Level 5 should have more variety
        available = pool.get_available_monsters(5)
        available_classes = [spec.monster_class for spec in available]
        
        assert len(available_classes) >= 5  # Should have multiple options
        assert Troll in available_classes  # Should have mid-tier monsters
        assert Devil not in available_classes  # But not boss
    
    def test_get_available_monsters_boss_level(self):
        """Test getting available monsters for level 10."""
        pool = MonsterPool()
        
        # Level 10 should have Devil as primary option
        available = pool.get_available_monsters(10, boss_encounter=False)
        available_classes = [spec.monster_class for spec in available]
        
        assert Devil in available_classes
        # Should have other high-level monsters too, but Devil will dominate via weighting
    
    def test_target_difficulty_scaling(self):
        """Test that target difficulty scales appropriately."""
        pool = MonsterPool()
        
        # Difficulty should increase with level
        diff_1 = pool.get_target_difficulty(1)
        diff_5 = pool.get_target_difficulty(5)
        diff_9 = pool.get_target_difficulty(9)
        diff_10 = pool.get_target_difficulty(10)
        
        assert diff_1 < diff_5 < diff_9 < diff_10
        assert diff_1 == 1.0  # Should start at 1.0
        assert diff_10 == 10.0  # Boss level should be 10.0
    
    def test_spawn_weight_calculation(self):
        """Test spawn weight calculations."""
        pool = MonsterPool()
        skeleton_spec = next(spec for spec in pool.monsters if spec.monster_class == Skeleton)
        
        # At level 1, skeleton should have good weight
        weight_1 = pool.calculate_spawn_weight(skeleton_spec, 1, 1.0)
        
        # At level 8, skeleton should have much lower weight
        weight_8 = pool.calculate_spawn_weight(skeleton_spec, 8, 4.0)
        
        assert weight_1 > weight_8, "Skeleton should be less likely at higher levels"
        assert weight_8 > 0, "Weight should never be zero"
    
    def test_monster_creation_consistency(self):
        """Test that monster creation is consistent and appropriate."""
        pool = MonsterPool()
        
        # Test multiple levels
        for level in range(1, 11):
            monster = pool.create_monster_for_level(level, 0, 0)
            
            # Should always return a valid monster
            assert monster is not None
            assert hasattr(monster, 'name')
            assert hasattr(monster, 'x')
            assert hasattr(monster, 'y')
            assert monster.x == 0
            assert monster.y == 0
    
    def test_level_10_creation(self):
        """Test level 10 monster creation."""
        pool = MonsterPool()
        
        # Level 10 should predominantly spawn Devils
        devils = 0
        for _ in range(10):
            monster = pool.create_monster_for_level(10, 5, 5, boss_encounter=False)
            if isinstance(monster, Devil):
                devils += 1
            assert monster.x == 5
            assert monster.y == 5
        
        # Should spawn mostly devils (at least 80% due to very high weighting)
        assert devils >= 8
    
    def test_level_monster_distribution(self):
        """Test getting monster distribution for levels."""
        pool = MonsterPool()
        
        # Level 1 distribution
        dist_1 = pool.get_level_monster_distribution(1)
        assert "Skeleton" in dist_1
        assert "Zombie" in dist_1
        assert "Devil" not in dist_1
        
        # Probabilities should sum to ~1.0
        total_prob = sum(dist_1.values())
        assert abs(total_prob - 1.0) < 0.001
        
        # Level 6 should have more variety
        dist_6 = pool.get_level_monster_distribution(6)
        assert len(dist_6) >= 4  # Should have multiple monster types


class TestMonsterFactoryCompatibility:
    """Test the factory interface for backward compatibility."""
    
    def test_create_monster_for_level_function(self):
        """Test the main factory function."""
        # Should work with just level
        monster = create_monster_for_level(1)
        assert monster is not None
        assert monster.x == 0  # Default position
        assert monster.y == 0
        
        # Should work with coordinates
        monster = create_monster_for_level(5, 10, 20)
        assert monster.x == 10
        assert monster.y == 20
    
    def test_global_pool_access(self):
        """Test that the global pool is accessible."""
        pool = get_monster_pool()
        assert isinstance(pool, MonsterPool)
        assert len(pool.monsters) > 0
    
    def test_level_progression(self):
        """Test that monster types change appropriately with level."""
        # Sample monsters from different levels
        level_1_monsters = set()
        level_5_monsters = set()
        level_9_monsters = set()
        
        # Generate multiple monsters to see variety
        for _ in range(50):
            level_1_monsters.add(type(create_monster_for_level(1)).__name__)
            level_5_monsters.add(type(create_monster_for_level(5)).__name__)
            level_9_monsters.add(type(create_monster_for_level(9)).__name__)
        
        # Early levels should have basic monsters
        assert "Skeleton" in level_1_monsters or "Zombie" in level_1_monsters
        
        # Mid levels should have more variety
        assert len(level_5_monsters) >= 2
        
        # Later levels should have advanced monsters
        assert any(monster in level_9_monsters for monster in ["Troll", "Angel", "Horror"])
        
        # Level 9 should not have early game monsters as primary spawns
        # (They might still appear due to transition smoothing, but should be rare)
    
    def test_boss_level_spawning(self):
        """Test that level 10 spawns appropriate monsters."""
        # Level 10 should predominantly spawn Devils
        devils = 0
        for _ in range(20):
            monster = create_monster_for_level(10, 0, 0)
            if isinstance(monster, Devil):
                devils += 1
        
        # Should spawn mostly devils (at least 90% due to very high weighting)
        assert devils >= 18, f"Expected at least 18 devils, got {devils}"


def run_all_tests():
    """Run all tests manually."""
    print("Running Monster Pool System Tests...")
    
    # Test MonsterSpec
    print("\n=== Testing MonsterSpec ===")
    test_spec = TestMonsterSpec()
    test_spec.test_monster_spec_creation()
    test_spec.test_boss_monster_spec()
    print("MonsterSpec tests passed!")
    
    # Test MonsterPool  
    print("\n=== Testing MonsterPool ===")
    test_pool = TestMonsterPool()
    test_pool.test_monster_pool_initialization()
    test_pool.test_get_available_monsters_early_level()
    test_pool.test_get_available_monsters_mid_level()
    test_pool.test_get_available_monsters_boss_level()
    test_pool.test_target_difficulty_scaling()
    test_pool.test_spawn_weight_calculation()
    test_pool.test_monster_creation_consistency()
    test_pool.test_level_10_creation()
    test_pool.test_level_monster_distribution()
    print("MonsterPool tests passed!")
    
    # Test Factory Compatibility
    print("\n=== Testing Factory Compatibility ===")
    test_factory = TestMonsterFactoryCompatibility()
    test_factory.test_create_monster_for_level_function()
    test_factory.test_global_pool_access()
    test_factory.test_level_progression()
    test_factory.test_boss_level_spawning()
    print("Factory compatibility tests passed!")
    
    print("\n🎉 All tests passed!")


if __name__ == "__main__":
    run_all_tests()