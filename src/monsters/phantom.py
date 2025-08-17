"""
Phantom monster - hard to hit, ephemeral creature.
"""

from .base import Monster
from constants import COLOR_WHITE
from traits import Trait


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
            resistances=[Trait.ICE, Trait.SLASH, Trait.STRIKE],
            attack_traits=[Trait.MYSTIC]
        )