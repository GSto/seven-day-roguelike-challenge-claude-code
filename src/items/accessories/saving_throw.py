"""
SavingThrow - If an attack would set your HP to 0 and your starting HP was not 1, your HP becomes 1.
"""
from .accessory import Accessory


class SavingThrow(Accessory):
    """If an attack would set your HP to 0 and your starting HP was not 1, your HP becomes 1"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Saving Throw", '=',
                        description="If an attack would set your HP to 0 and your starting HP was not 1, your HP becomes 1")
    
    def prevents_death(self, player, starting_hp):
        """Check if this accessory prevents death."""
        return starting_hp > 1