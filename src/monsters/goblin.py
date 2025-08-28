"""
Goblin monster - sneaky with higher crit chance.
"""

from .base import Monster
from constants import COLOR_GREEN
from traits import Trait


class Goblin(Monster):
    """Sneaky goblin with higher crit chance."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Goblin",
            char='G',
            color=COLOR_GREEN,
            hp=55,
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