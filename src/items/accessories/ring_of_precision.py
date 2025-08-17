"""
RingOfPrecision - Ring that enhances critical strikes.
"""
from .ring import Ring


class RingOfPrecision(Ring):
    """Ring that enhances critical strikes."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Precision", crit_bonus=0.12, description="A ring that guides your strikes")