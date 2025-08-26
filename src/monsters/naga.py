"""
Naga poisonous snake monster
"""

from .base import Monster
from constants import COLOR_GREEN
from traits import Trait


class Naga(Monster):
    """Poisonous Snake Person"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Naga",
            char='N',
            color=COLOR_GREEN,
            hp=80,
            attack=9,
            defense=3,
            xp_value=65,
            evade=0.08,  # Slightly higher evade
            crit=0.05,  # Nerfed crit abilities - Horrors are dangerous enough in current state
            crit_multiplier=1.5,
            attack_traits=[Trait.POISON]
        )