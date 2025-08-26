"""
Orc monster - medium strength warrior.
"""

from .base import Monster
from constants import COLOR_RED
from traits import Trait


class Orc(Monster):
    """Medium strength orc warrior."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Orc",
            char='O',
            color=COLOR_RED,
            hp=45,
            attack=9,
            defense=2,
            xp_value=20,
            weaknesses=[Trait.STRIKE],
            resistances=[Trait.FIRE]
        )