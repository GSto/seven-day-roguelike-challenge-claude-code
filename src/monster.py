"""
Monster system - creatures that populate the dungeon levels.
"""

import random
from constants import COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_WHITE


class Monster:
    """Base class for all monsters."""
    
    def __init__(self, x, y, name, char, color, hp, attack, defense, xp_value):
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
        
        # AI state
        self.target_x = None
        self.target_y = None
        self.has_seen_player = False
        self.turns_since_seen_player = 0
    
    def take_damage(self, damage):
        """Take damage, accounting for defense."""
        actual_damage = max(1, damage - self.defense)
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


class Goblin(Monster):
    """Weak but fast goblin."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Goblin",
            char='g',
            color=COLOR_GREEN,
            hp=15,
            attack=4,
            defense=0,
            xp_value=10
        )


class Orc(Monster):
    """Medium strength orc warrior."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Orc",
            char='o',
            color=COLOR_RED,
            hp=25,
            attack=7,
            defense=1,
            xp_value=20
        )


class Troll(Monster):
    """Strong troll with high defense."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Troll",
            char='T',
            color=COLOR_YELLOW,
            hp=40,
            attack=10,
            defense=3,
            xp_value=35
        )


class Dragon(Monster):
    """Powerful dragon - final boss of the dungeon."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Ancient Dragon",
            char='D',
            color=COLOR_RED,
            hp=150,      # Increased HP for final boss
            attack=25,   # Higher attack
            defense=8,   # Strong defense
            xp_value=200 # Massive XP reward
        )
        # Mark this as the final boss
        self.is_final_boss = True


def create_monster_for_level(level_number):
    """Create an appropriate monster type for the given dungeon level."""
    # Scale monster difficulty with dungeon level
    rand = random.random()
    
    if level_number <= 2:
        # Early levels: mostly goblins
        if rand < 0.8:
            return Goblin
        else:
            return Orc
    
    elif level_number <= 5:
        # Mid levels: goblins and orcs
        if rand < 0.4:
            return Goblin
        elif rand < 0.8:
            return Orc
        else:
            return Troll
    
    elif level_number <= 8:
        # Later levels: orcs and trolls
        if rand < 0.3:
            return Orc
        else:
            return Troll
    
    elif level_number == 10:
        # Final level: dragons only
        return Dragon
    
    else:
        # Level 9: mix with some dragons
        if rand < 0.7:
            return Troll
        else:
            return Dragon