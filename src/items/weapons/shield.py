"""
Shield weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class Shield(Weapon):
    """Defensive "weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Shield", ')', 1, defense_multiplier_bonus=1.25, description="A shield.", attack_traits=[Trait.THWACK])
        self.defense_bonus = 1