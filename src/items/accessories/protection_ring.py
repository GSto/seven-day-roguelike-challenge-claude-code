"""
ProtectionRing - Ring that provides strong defense.
"""
from .ring import Ring


class ProtectionRing(Ring):
    """Ring that provides strong defense."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Protection", defense_bonus=2)