"""
Spiked Armor for the roguelike game.
"""

from .base import Armor


class SpikedArmor(Armor):
    """Aggressive armor with spikes for extra protection and offense."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Spiked Armor", '[', 1, description="Menacing armor covered in spikes", attack_bonus=2)