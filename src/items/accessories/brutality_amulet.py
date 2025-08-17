"""
BrutalityAmulet - Necklace that enhances critical damage.
"""
from .necklace import Necklace


class BrutalityAmulet(Necklace):
    """Necklace that enhances critical damage."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Amulet of Brutality", crit_multiplier_bonus=0.5, description="An amulet that amplifies your fury")