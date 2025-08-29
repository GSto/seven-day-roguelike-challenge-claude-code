"""
Horror monster - aggressive abomination with devastating crits.
"""

from .base import Monster
from constants import COLOR_CRIMSON
from traits import Trait


class Horror(Monster):
    """Aggressive abomination with devastating crits"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Horror",
            char='H',
            color=COLOR_CRIMSON,
            hp=200,
            attack=16,
            defense=3,
            xp_value=67,
            evade=0.08,  # Slightly higher evade
            crit=0.05,  # Nerfed crit abilities - Horrors are dangerous enough in current state
            crit_multiplier=1.5,
            weaknesses=[Trait.MYSTIC, Trait.ICE]
        )