"""
Base Monster class for all creatures in the dungeon.
"""

import random
from status_effects import StatusEffects
from entity import Entity
from stats import Stats, StatType


class Monster(Entity):
    """Base class for all monsters."""
    
    def __init__(self, x, y, name, char, color, hp, attack, defense, xp_value,
                 evade=0.05, crit=0.05, crit_multiplier=2.0, attack_traits=None, weaknesses=None, resistances=None):
        """Initialize a monster."""
        # Create stats for the monster
        monster_stats = Stats(
            max_hp=hp,
            hp=hp,
            attack=attack,
            defense=defense,
            evade=evade,
            crit=crit,
            crit_multiplier=crit_multiplier,
            attack_multiplier=1.0,
            defense_multiplier=1.0
        )
        
        # Initialize base Entity attributes
        super().__init__(
            x=x,
            y=y,
            character=char,
            color=color,
            stats=monster_stats,
            attack_traits=attack_traits or [],
            weaknesses=weaknesses or [],
            resistances=resistances or []
        )
        
        # Monster-specific attributes
        self.name = name
        self.xp_value = xp_value
        
        # AI state
        self.target_x = None
        self.target_y = None
        self.has_seen_player = False
        self.turns_since_seen_player = 0
    
    def distance_to(self, x, y):
        """Calculate distance to given coordinates."""
        return ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
    
    def can_see_player(self, player_x, player_y, level_fov):
        """Check if monster can see the player using FOV."""
        # Monster can see player if player is in its FOV and close enough
        if level_fov[self.x, self.y] and level_fov[player_x, player_y]:
            distance = self.distance_to(player_x, player_y)
            return distance <= 8  # Monster sight range
        return False
