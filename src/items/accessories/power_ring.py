"""
PowerRing - Ring that boosts attack.
"""
from .ring import Ring


class PowerRing(Ring):
    """Ring that boosts attack."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Power", attack_bonus=3, defense_bonus=0)