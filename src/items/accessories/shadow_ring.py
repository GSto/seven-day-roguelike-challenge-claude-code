"""
ShadowRing - Ring that enhances evasion.
"""
from .ring import Ring


class ShadowRing(Ring):
    """Ring that enhances evasion."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Shadow Ring", evade_bonus=0.10, description="A ring that bends light around you")