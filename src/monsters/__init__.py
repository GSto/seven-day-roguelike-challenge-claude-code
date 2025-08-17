"""
Monster system - creatures that populate the dungeon levels.
"""

from .base import Monster
from .skeleton import Skeleton
from .zombie import Zombie
from .orc import Orc
from .phantom import Phantom
from .goblin import Goblin
from .troll import Troll
from .horror import Horror
from .angel import Angel
from .devil import Devil
from .factory import create_monster_for_level

__all__ = [
    'Monster',
    'Skeleton',
    'Zombie', 
    'Orc',
    'Phantom',
    'Goblin',
    'Troll',
    'Horror',
    'Angel',
    'Devil',
    'create_monster_for_level'
]