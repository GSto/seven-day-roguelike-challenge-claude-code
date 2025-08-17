"""
Rosary - Necklace that increases health aspect.
"""
from .necklace import Necklace
from traits import Trait


class Rosary(Necklace):
    """Necklace that increases health aspect."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Rosary", defense_bonus=1, health_aspect_bonus=0.1, description="A healer's necklace")
        self.weaknesses = [Trait.HOLY]
        self.resistances = [Trait.DARK]