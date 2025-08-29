from .base import Monster
from constants import COLOR_GRAY
from traits import Trait


class Umbral(Monster):
    """Shadow being touched by light and dark"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Umbral",
            char='U',
            color=COLOR_GRAY,
            hp=110,
            attack=10,
            defense=3,
            xp_value=52,
            evade=0.12,  
            crit=0.08,  
            crit_multiplier=1.8,
            attack_traits=[Trait.HOLY, Trait.DARK],
            resistances=[Trait.HOLY, Trait.DARK]
        )