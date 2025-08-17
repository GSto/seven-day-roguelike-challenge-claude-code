"""
GreaterPowerRing - Ring that greatly boosts attack.
"""
from .ring import Ring


class GreaterPowerRing(Ring):
    """Ring that greatly boosts attack."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Greater Ring of Power", attack_bonus=6, defense_bonus=0)