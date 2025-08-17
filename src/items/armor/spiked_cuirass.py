"""
Spiked Cuirass armor for the roguelike game.
"""

from .base import Armor


class SpikedCuirass(Armor):
    """Mid-game+ armor. +4 DEF, +2 ATK"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Spiked Cuirass", '[', 4, 
                        description="Mid-game+ armor. +4 DEF, +2 ATK",
                        attack_bonus=2)