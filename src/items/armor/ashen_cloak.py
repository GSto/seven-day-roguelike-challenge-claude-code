"""
Ashen Cloak - Evasive armor with elemental resistances.
"""

from .base import Armor
from traits import Trait


class AshenCloak(Armor):
    """Ashen Cloak - Made from enchanted ash, providing evasion and elemental protection."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Ashen Cloak",
            char="[",
            defense_bonus=0,
            evade_bonus=0.16,
            description="A cloak woven from enchanted ash. +16% EVD and resistance to Fire, Ice, and Poison damage.",
            market_value=75,
            resistances=[Trait.FIRE, Trait.ICE, Trait.POISON]
        )