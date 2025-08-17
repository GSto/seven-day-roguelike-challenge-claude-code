"""
Longsword weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class Longsword(Weapon):
    """Powerful two-handed weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Longsword", ')', 8, "A two-handed longsword", attack_traits=[Trait.SLASH])