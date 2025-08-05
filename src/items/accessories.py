"""
Accessory items like rings and amulets.
"""

from constants import COLOR_WHITE
from .base import Equipment


class Accessory(Equipment):
    """Accessory equipment (rings, amulets, etc.)."""
    
    def __init__(self, x, y, name, char, attack_bonus=0, defense_bonus=0, 
                 description="", fov_bonus=0, health_aspect_bonus=0.0):
        super().__init__(
            x=x, y=y,
            name=name,
            char=char,
            color=COLOR_WHITE,
            description=description,
            attack_bonus=attack_bonus,
            defense_bonus=defense_bonus,
            equipment_slot="accessory",
            fov_bonus=fov_bonus,
            health_aspect_bonus=health_aspect_bonus
        )


class Ring(Accessory):
    """Base class for rings."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0):
        super().__init__(x, y, name, '=', attack_bonus, defense_bonus, f"A magical ring")


class PowerRing(Ring):
    """Ring that boosts attack."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Power", attack_bonus=4, defense_bonus=0)


class ProtectionRing(Ring):
    """Ring that provides strong defense."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Protection", defense_bonus=3)


class GreaterPowerRing(Ring):
    """Ring that greatly boosts attack."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Greater Ring of Power", attack_bonus=9, defense_bonus=0)


class GreaterProtectionRing(Ring):
    """Ring that greatly boosts attack."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Greater Ring of Protection", attack_bonus=0, defense_bonus=7)


  