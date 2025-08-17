"""
Troll monster - strong with high defense.
"""

from .base import Monster
from constants import COLOR_YELLOW
from traits import Trait


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
            defense=7,
            xp_value=45,
            evade=0.02, # Trolls are slow
            attack_traits=[Trait.STRIKE],
            weaknesses=[Trait.FIRE, Trait.SLASH]
        )