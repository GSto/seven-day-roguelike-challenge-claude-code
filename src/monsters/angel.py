"""
Angel monster - angelic creature with flight abilities.
"""

from .base import Monster
from constants import COLOR_WHITE
from traits import Trait


class Angel(Monster):
    """Angelic monster"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Angel",
            char='A',
            color=COLOR_WHITE,
            hp=200,
            attack=13,
            defense=2,
            xp_value=65,
            evade=0.20,  # Flying Creatures Evade More
            crit=0.05,  
            crit_multiplier=1.5,
            weaknesses=[Trait.DARK, Trait.MYSTIC],
            attack_traits=[Trait.HOLY]
        )