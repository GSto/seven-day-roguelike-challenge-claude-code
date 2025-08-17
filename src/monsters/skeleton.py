"""
Skeleton monster - weak but fast with higher evade.
"""

from .base import Monster
from constants import COLOR_WHITE
from traits import Trait


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