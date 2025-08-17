"""
Morning Star weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class MorningStar(Weapon):
    """Powerful two-handed weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Morning Star", ')', 9, "A two-handed club", attack_traits=[Trait.STRIKE])