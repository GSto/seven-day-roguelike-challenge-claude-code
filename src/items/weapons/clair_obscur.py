"""
Clair Obscur weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class ClairObscur(Weapon):
    """Late game weapon. 10 dmg. Deals light, dark, and mystic damage"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Clair Obscur", ')', 10, 
                        "Late game weapon. 10 dmg. Deals light, dark, and mystic damage",
                        attack_traits=[Trait.HOLY, Trait.DARK, Trait.MYSTIC])