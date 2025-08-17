"""
Zombie monster - slow but tough undead.
"""

from .base import Monster
from constants import COLOR_WHITE
from traits import Trait


class Zombie(Monster):
    """Slow but resilient zombie."""
    
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