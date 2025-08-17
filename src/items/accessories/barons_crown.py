"""
BaronsCrown - Hat with attack multiplier.
"""
from .hat import Hat


class BaronsCrown(Hat):
    """Hat with attack multiplier."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Baron's Crown", attack_multiplier_bonus=1.25, description="Crown of a Jester King")