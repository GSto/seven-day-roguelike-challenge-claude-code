"""
Accessory items like rings and amulets.
"""

from constants import COLOR_WHITE
from .base import Equipment


class Accessory(Equipment):
    """Accessory equipment (rings, amulets, etc.)."""
    
    def __init__(self, x, y, name, char, attack_bonus=0, defense_bonus=0, description=""):
        super().__init__(
            x=x, y=y,
            name=name,
            char=char,
            color=COLOR_WHITE,
            description=description,
            attack_bonus=attack_bonus,
            defense_bonus=defense_bonus,
            equipment_slot="accessory"
        )


class Ring(Accessory):
    """Base class for rings."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0):
        super().__init__(x, y, name, '=', attack_bonus, defense_bonus, f"A magical ring")


class PowerRing(Ring):
    """Ring that boosts attack and defense."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Power", attack_bonus=3, defense_bonus=1)


class ProtectionRing(Ring):
    """Ring that provides strong defense."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Protection", defense_bonus=3)