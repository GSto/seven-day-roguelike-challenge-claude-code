"""
GreaterProtectionRing - Ring that greatly boosts defense.
"""
from .ring import Ring


class GreaterProtectionRing(Ring):
    """Ring that greatly boosts attack."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Greater Ring of Protection", attack_bonus=0, defense_bonus=4)