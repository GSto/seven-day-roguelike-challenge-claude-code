"""
Feu-Glace weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class FeuGlace(Weapon):
    """Late game weapon. 10 dmg. Deals fire, ice, and mystic damage"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Feu-Glace", ')', 10, 
                        "Late game weapon. 10 dmg. Deals fire, ice, and mystic damage",
                        attack_traits=[Trait.FIRE, Trait.ICE, Trait.MYSTIC])