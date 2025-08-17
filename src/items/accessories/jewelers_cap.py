"""
JewelersCap - Hat with XP multiplier.
"""
from .hat import Hat


class JewelersCap(Hat):
    """Hat with XP multiplier."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Jeweler's Cap", xp_multiplier_bonus=1.1, description="A greedy man's gift")