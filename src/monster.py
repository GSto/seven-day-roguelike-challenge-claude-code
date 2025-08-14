"""
Monster system - creatures that populate the dungeon levels.
"""

import random
from constants import COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_CRIMSON, COLOR_WHITE
from traits import Trait


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


# Traditionally, Rogue had 26 monsters, one for each letter of the alphabet 
# _BC_EF__IJKLMN__QR_TUVWXYZ
class Skeleton(Monster):
    """Weak but fast skeleton with higher evade."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Skeleton",
            char='S',
            color=COLOR_WHITE,
            hp=15,
            attack=4,
            defense=0,
            xp_value=10,
            evade=0.15,  # Higher evade - skeletons are nimble
            crit=0.05,
            crit_multiplier=2.0,
            weaknesses=[Trait.HOLY]
        )

class Zombie(Monster):
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Zombie",
            char='Z',
            color=COLOR_WHITE,
            hp=12,
            attack=5,
            defense=0,
            xp_value=10,
            evade=0, #Zombies slow
            crit=0,
            weaknesses=[Trait.HOLY, Trait.FIRE],
            resistances=[Trait.ICE]
        )


class Orc(Monster):
    """Medium strength orc warrior."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Orc",
            char='O',
            color=COLOR_RED,
            hp=25,
            attack=9,
            defense=2,
            xp_value=20,
            weaknesses=[Trait.STRIKE],
            resistances=[Trait.FIRE]
        )

class Phantom(Monster):
    """Hard to hit, ephemeral creature."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Phantom",
            char='P',
            color=COLOR_WHITE,
            hp=15,
            attack=9,
            defense=0,
            xp_value=25,
            evade=0.4,
            weaknesses=[Trait.HOLY, Trait.DARK],
            resistances=[Trait.ICE],
            attack_traits=[Trait.MYSTIC]
        )

class Goblin(Monster):
    """Sneaky goblin with higher crit chance."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Goblin",
            char='G',
            color=COLOR_GREEN,
            hp=35,
            attack=9,
            defense=1,
            xp_value=25,
            evade=0.1,  # Decent evade
            crit=0.15,  # Higher crit - goblins are sneaky
            crit_multiplier=2.0,
            attack_traits=[Trait.SLASH],
            weaknesses=[Trait.ICE, Trait.HOLY],
            resistances=[Trait.FIRE]
        )


class Troll(Monster):
    """Strong troll with high defense."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Troll",
            char='T',
            color=COLOR_YELLOW,
            hp=60,
            attack=8,
            defense=5,
            xp_value=45,
            evade=0.02, # Trolls are slow
            attack_traits=[Trait.STRIKE],
            weaknesses=[Trait.FIRE, Trait.SLASH]
        )

class Horror(Monster):
      """Aggressive abomination with devastating crits"""
      
      def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Horror",
            char='H',
            color=COLOR_CRIMSON,
            hp=100,
            attack=16,
            defense=3,
            xp_value=65,
            evade=0.08,  # Slightly higher evade
            crit=0.05,  # Nerfed crit abilities - Horrors are dangerous enough in current state
            crit_multiplier=1.5,
            weaknesses=[Trait.MYSTIC, Trait.ICE]
        )

class Angel(Monster):
      """Angelic monster"""
      
      def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Angel",
            char='A',
            color=COLOR_YELLOW,
            hp=100,
            attack=11,
            defense=2,
            xp_value=65,
            evade=0.20,  # Flying Creatures Evade More
            crit=0.05,  
            crit_multiplier=1.5,
            weaknesses=[Trait.DARK, Trait.MYSTIC],
            attack_traits=[Trait.HOLY]
        )
    


class Devil(Monster):
    """Powerful devil - final boss of the dungeon."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Ancient Devil",
            char='D',
            color=COLOR_RED,
            hp=666,      
            attack=20,   
            defense=6,   
            xp_value=666, # Massive XP reward
            evade=0.06,  
            crit=0.06,  
            crit_multiplier=2.06,
            attack_traits=[Trait.DARK, Trait.FIRE],
            weaknesses=[Trait.DEMONSLAYER]
        )
        # Mark this as the final boss
        self.is_final_boss = True


def create_monster_for_level(level_number):
    """Create an appropriate monster type for the given dungeon level."""
    # Scale monster difficulty with dungeon level
    rand = random.random()
    
    if level_number <= 2:
        if rand < 0.7:
            return Skeleton
        else:
            return Zombie
        
    elif level_number <=3:
        if rand < 0.7:
            return Skeleton
        elif rand < 0.9:
            return Zombie
        else:
            return Orc
        
        
    elif level_number <= 4: 
        if rand < 0.1:
          return Skeleton
        if rand < 0.2:
          return Zombie
        elif rand < 0.5:
          return Phantom
        elif rand < 0.8:
          return Orc
        else: 
          return Goblin
    
    elif level_number <= 5:
        # Mid levels: no more goblins, trolls start to appear
        if rand < 0.2: 
            return Phantom
        elif rand < 0.4:
            return Orc
        elif rand < 0.8:
            return Goblin
        else:
            return Troll
        
    elif level_number <= 7:
      # Upper-mid levels: 
      if rand < 0.2:
          return Orc
      elif rand < 0.5:
          return Goblin
      elif rand < 0.8:
          return Troll
      elif rand < 0.9:
          return Angel
      else:
          return Horror
    
    elif level_number <= 9:
        # Later levels: no more orcs, only harder enemies
        if rand < 0.3:
            return Goblin
        elif rand < 0.7:
            return Troll
        elif rand < 0.85: 
            return Angel
        else:
            return Horror
    
    else:
        # Final level (level 10): devil only
        return Devil