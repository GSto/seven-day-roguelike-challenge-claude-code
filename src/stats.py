"""
Stats system for managing entity attributes.
"""

from enum import Enum
from dataclasses import dataclass


class StatType(Enum):
    """Enumeration of all stat types."""
    MAX_HP = "max_hp"
    HP = "hp"
    ATTACK = "attack"
    DEFENSE = "defense"
    EVADE = "evade"
    CRIT = "crit"
    CRIT_MULTIPLIER = "crit_multiplier"
    ATTACK_MULTIPLIER = "attack_multiplier"
    DEFENSE_MULTIPLIER = "defense_multiplier"
    XP_MULTIPLIER = "xp_multiplier"
    XP = "xp"
    HEALTH_ASPECT = "health_aspect"


@dataclass
class Stats:
    """Container for all entity statistics."""
    
    # Core combat stats
    max_hp: int
    hp: int
    attack: int
    defense: int
    
    # Combat modifiers
    evade: float = 0.05
    crit: float = 0.05
    crit_multiplier: float = 2.0
    attack_multiplier: float = 1.0
    defense_multiplier: float = 1.0
    
    # Player-specific stats (will be 0/default for monsters)
    xp_multiplier: float = 1.0
    xp: int = 0
    health_aspect: float = 0.0
    
    def get_stat(self, stat_type: StatType):
        """Get a stat value by its type."""
        if stat_type == StatType.MAX_HP:
            return self.max_hp
        elif stat_type == StatType.HP:
            return self.hp
        elif stat_type == StatType.ATTACK:
            return self.attack
        elif stat_type == StatType.DEFENSE:
            return self.defense
        elif stat_type == StatType.EVADE:
            return self.evade
        elif stat_type == StatType.CRIT:
            return self.crit
        elif stat_type == StatType.CRIT_MULTIPLIER:
            return self.crit_multiplier
        elif stat_type == StatType.ATTACK_MULTIPLIER:
            return self.attack_multiplier
        elif stat_type == StatType.DEFENSE_MULTIPLIER:
            return self.defense_multiplier
        elif stat_type == StatType.XP_MULTIPLIER:
            return self.xp_multiplier
        elif stat_type == StatType.XP:
            return self.xp
        elif stat_type == StatType.HEALTH_ASPECT:
            return self.health_aspect
        else:
            raise ValueError(f"Unknown stat type: {stat_type}")
    
    def set_stat(self, stat_type: StatType, value):
        """Set a stat value by its type."""
        if stat_type == StatType.MAX_HP:
            self.max_hp = value
        elif stat_type == StatType.HP:
            self.hp = value
        elif stat_type == StatType.ATTACK:
            self.attack = value
        elif stat_type == StatType.DEFENSE:
            self.defense = value
        elif stat_type == StatType.EVADE:
            self.evade = value
        elif stat_type == StatType.CRIT:
            self.crit = value
        elif stat_type == StatType.CRIT_MULTIPLIER:
            self.crit_multiplier = value
        elif stat_type == StatType.ATTACK_MULTIPLIER:
            self.attack_multiplier = value
        elif stat_type == StatType.DEFENSE_MULTIPLIER:
            self.defense_multiplier = value
        elif stat_type == StatType.XP_MULTIPLIER:
            self.xp_multiplier = value
        elif stat_type == StatType.XP:
            self.xp = value
        elif stat_type == StatType.HEALTH_ASPECT:
            self.health_aspect = value
        else:
            raise ValueError(f"Unknown stat type: {stat_type}")