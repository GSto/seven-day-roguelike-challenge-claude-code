"""
Armor items for defense.
"""

from constants import COLOR_GREEN
from .base import Equipment


class Armor(Equipment):
    """Armor equipment."""
    
    def __init__(self, x, y, name, char, defense_bonus, description=""):
        super().__init__(
            x=x, y=y,
            name=name,
            char=char,
            color=COLOR_GREEN,
            description=description,
            defense_bonus=defense_bonus,
            equipment_slot="armor"
        )


# Specific armor types
class WhiteTShirt(Armor):
    """Basic starting armor."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "White T-Shirt", '[', 0, "A plain white T-shirt")


class LeatherArmor(Armor):
    """Light armor for early game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Leather Armor", '[', 2, "Basic leather protection")


class ChainMail(Armor):
    """Medium armor for mid-game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Chain Mail", '[', 4, "Flexible chain mail armor")


class PlateArmor(Armor):
    """Heavy armor for late game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Plate Armor", '[', 6, "Heavy plate armor")


class DragonScale(Armor):
    """Legendary armor from dragon materials."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Dragon Scale Armor", '[', 10, "Legendary dragon scale armor")