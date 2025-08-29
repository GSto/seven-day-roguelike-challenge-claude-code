"""
Safety Vest armor for the roguelike game.
"""

from .base import Armor


class SafetyVest(Armor):
    """Light armor for early game."""

    def __init__(self, x, y):
        super().__init__(x, y, "Safety Vest", '[', 2, description="Bright orange, easy to see", fov_bonus=2)
        self.market_value = 25  # Early game common armor