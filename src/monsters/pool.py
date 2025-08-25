"""
Monster pool management system for creating monsters based on level difficulty.
"""

from dataclasses import dataclass
from typing import List, Type, Dict, Optional
import random

from .skeleton import Skeleton
from .zombie import Zombie
from .orc import Orc
from .phantom import Phantom
from .goblin import Goblin
from .troll import Troll
from .horror import Horror
from .angel import Angel
from .devil import Devil


@dataclass
class MonsterSpec:
    """Specification for a monster type including difficulty and spawn rules."""
    monster_class: Type
    difficulty_rating: float  # Relative difficulty (1.0 = baseline)
    min_level: int           # Earliest level this monster can appear
    max_level: Optional[int] # Latest level (None = no limit)
    rarity: float           # Base spawn weight (higher = more common)
    boss_only: bool = False # True if this is a boss monster


class MonsterPool:
    """Manages monster spawning with smooth difficulty curves."""
    
    def __init__(self):
        """Initialize the monster pool with all available monsters."""
        self.monsters: List[MonsterSpec] = [
            # Early game monsters (levels 1-3)
            MonsterSpec(Skeleton, 1.0, 1, 4, 1.0),
            MonsterSpec(Zombie, 1.2, 1, 5, 0.8),
            
            # Mid-early monsters (levels 2-6) 
            MonsterSpec(Orc, 1.8, 3, 7, 0.7),
            MonsterSpec(Phantom, 2.0, 4, 8, 0.6),
            MonsterSpec(Goblin, 2.2, 4, 9, 0.8),
            
            # Mid-late monsters (levels 5-9)
            MonsterSpec(Troll, 3.0, 5, None, 0.5),
            MonsterSpec(Angel, 3.5, 7, None, 0.4),
            MonsterSpec(Horror, 4.0, 7, None, 0.3),
            
            # Boss monster (level 10 only)
            MonsterSpec(Devil, 10.0, 10, 10, 1.0, boss_only=False),
        ]
        
        # Cache for performance
        self._level_pools: Dict[int, List[tuple]] = {}
    
    def clear_cache(self):
        """Clear the level pool cache."""
        self._level_pools.clear()
    
    def get_available_monsters(self, level: int, boss_encounter: bool = False) -> List[MonsterSpec]:
        """Get all monsters that can spawn on the given level."""
        available = []
        for monster in self.monsters:
            # Check level range
            if level < monster.min_level:
                continue
            if monster.max_level is not None and level > monster.max_level:
                continue
                
            # Check boss status
            if boss_encounter and not monster.boss_only:
                continue
            if not boss_encounter and monster.boss_only:
                continue
                
            available.append(monster)
        
        return available
    
    def calculate_spawn_weight(self, monster: MonsterSpec, level: int, target_difficulty: float) -> float:
        """Calculate the spawn weight for a monster based on level and target difficulty."""
        # Base weight from rarity
        weight = monster.rarity
        
        # Special case for level 10 boss encounters
        if level >= 10 and monster.difficulty_rating >= 10.0:
            # Massively boost weight for boss-level monsters on boss levels
            return weight * 10000.0
        
        # Difficulty scaling factor - prefer monsters closer to target difficulty
        difficulty_diff = abs(monster.difficulty_rating - target_difficulty)
        
        # More aggressive difficulty matching for high-level content
        if target_difficulty >= 8.0:
            # For late game, strongly prefer monsters that match difficulty
            if difficulty_diff < 0.5:
                difficulty_factor = 2.0  # Strong preference for exact matches
            elif difficulty_diff < 1.0:
                difficulty_factor = 1.0
            else:
                difficulty_factor = max(0.1, 1.0 - (difficulty_diff / 2.0))
        else:
            # Early/mid game can have more variety
            difficulty_factor = max(0.1, 1.0 - (difficulty_diff / 2.0))
            
        weight *= difficulty_factor
        
        # Level transition smoothing - gradually phase out monsters as they become too easy
        if monster.max_level is not None:
            levels_from_max = monster.max_level - level
            if levels_from_max <= 2 and levels_from_max >= 0:
                # Gradually reduce weight in final levels
                transition_factor = levels_from_max / 2.0
                weight *= max(0.1, transition_factor)
        
        # Phase in new monsters gradually
        levels_from_min = level - monster.min_level
        if levels_from_min <= 1:
            # Gradually increase weight in first few levels
            phase_in_factor = min(1.0, (levels_from_min + 1) / 2.0)
            weight *= phase_in_factor
            
        return max(0.01, weight)  # Ensure minimum weight
    
    def get_target_difficulty(self, level: int) -> float:
        """Calculate the target difficulty for a given level."""
        # Smooth exponential curve from 1.0 to 4.0 over levels 1-9
        if level >= 10:
            return 10.0  # Boss level
        
        # Exponential growth: difficulty = 1.0 * (growth_rate ^ (level - 1))
        growth_rate = (4.0 / 1.0) ** (1.0 / 8.0)  # 8 levels of growth (2-9)
        return 1.0 * (growth_rate ** (level - 1))
    
    def create_monster_for_level(self, level: int, x: int, y: int, boss_encounter: bool = False):
        """Create an appropriate monster for the given level."""
        # Use cached pool if available
        cache_key = level if not boss_encounter else f"boss_{level}"
        
        if cache_key not in self._level_pools:
            available_monsters = self.get_available_monsters(level, boss_encounter)
            
            if not available_monsters:
                # Fallback to skeleton if no monsters available (shouldn't happen)
                return Skeleton(x, y)
            
            target_difficulty = self.get_target_difficulty(level)
            
            # Calculate weighted list
            weighted_monsters = []
            for monster in available_monsters:
                weight = self.calculate_spawn_weight(monster, level, target_difficulty)
                weighted_monsters.append((monster.monster_class, weight))
            
            self._level_pools[cache_key] = weighted_monsters
        
        # Select monster using weighted random choice
        weighted_monsters = self._level_pools[cache_key]
        total_weight = sum(weight for _, weight in weighted_monsters)
        
        if total_weight <= 0:
            # Fallback
            return Skeleton(x, y)
        
        random_value = random.random() * total_weight
        current_weight = 0
        
        for monster_class, weight in weighted_monsters:
            current_weight += weight
            if random_value <= current_weight:
                return monster_class(x, y)
        
        # Fallback to last monster
        return weighted_monsters[-1][0](x, y)
    
    def get_level_monster_distribution(self, level: int) -> Dict[str, float]:
        """Get the probability distribution of monsters for a level (for debugging/testing)."""
        available_monsters = self.get_available_monsters(level, boss_encounter=False)
        target_difficulty = self.get_target_difficulty(level)
        
        distribution = {}
        total_weight = 0
        
        for monster in available_monsters:
            weight = self.calculate_spawn_weight(monster, level, target_difficulty)
            distribution[monster.monster_class.__name__] = weight
            total_weight += weight
        
        # Normalize to probabilities
        if total_weight > 0:
            for name in distribution:
                distribution[name] /= total_weight
        
        return distribution


# Global monster pool instance
_monster_pool = MonsterPool()


def create_monster_for_level(level_number: int, x: int = 0, y: int = 0, boss_encounter: bool = False):
    """Create an appropriate monster for the given level using the monster pool system."""
    return _monster_pool.create_monster_for_level(level_number, x, y, boss_encounter)


def get_monster_pool() -> MonsterPool:
    """Get the global monster pool instance."""
    return _monster_pool