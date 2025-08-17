"""
Base Monster class for all creatures in the dungeon.
"""

import random
from status_effects import StatusEffects


class Monster:
    """Base class for all monsters."""
    
    def __init__(self, x, y, name, char, color, hp, attack, defense, xp_value,
                 evade=0.05, crit=0.05, crit_multiplier=2.0, attack_traits=None, weaknesses=None, resistances=None):
        """Initialize a monster."""
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        
        # Combat stats
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.xp_value = xp_value
        
        # Combat modifiers
        self.evade = evade  # Base 5% evade chance
        self.crit = crit  # Base 5% crit chance
        self.crit_multiplier = crit_multiplier  # 2x damage on critical hit
        
        # AI state
        self.target_x = None
        self.target_y = None
        self.has_seen_player = False
        self.turns_since_seen_player = 0
        
        # Traits system
        self.attack_traits = attack_traits or []
        self.weaknesses = weaknesses or []
        self.resistances = resistances or []
        
        # Status effects system
        self.status_effects = StatusEffects()
    
    def take_damage(self, damage):
        """Take damage, accounting for defense."""
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def take_damage_with_traits(self, damage, attack_traits=None):
        """Take damage with trait consideration for resistances/weaknesses."""
        if attack_traits is None:
            attack_traits = []
        
        # Check for trait interactions
        final_damage = damage
        
        for trait in attack_traits:
            if trait in self.resistances:
                final_damage = int(final_damage * 0.5)  # 50% damage if resistant
            elif trait in self.weaknesses:
                final_damage = int(final_damage * 2.0)  # 200% damage if weak
        
        # Apply normal damage calculation
        actual_damage = max(1, final_damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def is_alive(self):
        """Check if the monster is alive."""
        return self.hp > 0
    
    def move(self, dx, dy):
        """Move the monster by dx, dy."""
        self.x += dx
        self.y += dy
    
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
    
    def render(self, console, fov):
        """Render the monster on the console."""
        if fov[self.x, self.y]:
            console.print(self.x, self.y, self.char, fg=self.color)