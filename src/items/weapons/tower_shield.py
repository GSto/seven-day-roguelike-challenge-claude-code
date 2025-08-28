"""
Tower Shield weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class TowerShield(Weapon):
    """Defensive "weapon."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Tower Shield", ')', 1, defense_multiplier_bonus=1.5, description="A large powerful shield", attack_traits=[Trait.THWACK])
        self.defense_bonus = 4