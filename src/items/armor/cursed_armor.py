"""
Cursed Armor - High defense armor with elemental weaknesses.
"""

from .base import Armor
from traits import Trait


class CursedArmor(Armor):
    """Cursed Armor - Strong defense but vulnerable to multiple damage types."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Cursed Armor",
            char="[",
            defense_bonus=9,
            description="Powerful armor bearing an ancient curse. +9 DEF but weakness to Fire, Ice, Holy, and Dark damage.",
            market_value=55,
            weaknesses=[Trait.FIRE, Trait.ICE, Trait.HOLY, Trait.DARK]
        )