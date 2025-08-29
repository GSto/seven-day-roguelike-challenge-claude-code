from .base import Monster
from constants import COLOR_GRAY
from traits import Trait


class Voidwalker(Monster):
    """Shadow being from nothingness"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Voidwalker",
            char='V',
            color=COLOR_GRAY,
            hp=210,
            attack=13,
            defense=3,
            xp_value=104,
            evade=0.12,  
            crit=0.08,  
            crit_multiplier=1.8,
            attack_traits=[Trait.FIRE, Trait.MYSTIC, Trait.POISON],
            resistances=[Trait.HOLY, Trait.DARK, Trait.MYSTIC]
        )