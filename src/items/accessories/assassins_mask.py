"""
AssassinsMask - Mask combining stealth and lethality.
"""
from .hat import Hat


class AssassinsMask(Hat):
    """Mask combining stealth and lethality."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Assassin's Mask", evade_bonus=0.08, crit_bonus=0.08, 
                        description="A mask that shrouds you in shadow and sharpens your focus")