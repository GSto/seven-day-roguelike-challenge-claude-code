"""
Monster factory for creating monsters based on level difficulty.
"""

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