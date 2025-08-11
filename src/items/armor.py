"""
Armor items for defense.
"""

from constants import COLOR_GREEN, COLOR_ORANGE
from .base import Equipment


class Armor(Equipment):
    """Armor equipment."""
    
    def __init__(self, x, y, name, char, defense_bonus, description="", 
                 attack_bonus=0, fov_bonus=0, health_aspect_bonus=0.0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 xp_cost=5):
        super().__init__(
            x=x, y=y,
            name=name,
            char=char,
            color=COLOR_GREEN,
            description=description,
            attack_bonus=attack_bonus,
            defense_bonus=defense_bonus,
            equipment_slot="armor",
            fov_bonus=fov_bonus,
            health_aspect_bonus=health_aspect_bonus,
            attack_multiplier_bonus=attack_multiplier_bonus,
            defense_multiplier_bonus=defense_multiplier_bonus,
            xp_multiplier_bonus=xp_multiplier_bonus,
            xp_cost=xp_cost
        )


# Specific armor types
class WhiteTShirt(Armor):
    """Basic starting armor."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "White T-Shirt", '[', 0, "A plain white T-shirt", xp_cost=0)


class LeatherArmor(Armor):
    """Light armor for early game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Leather Armor", '[', 1, description="Basic leather protection. Free to equip", xp_cost=0)

class SafetyVest(Armor):
    """Light armor for early game."""

    def __init__(self, x, y):
        super().__init__(x, y, "Safety Vest", '[', 2, description="Bright orange, easy to see", fov_bonus=2)

class ChainMail(Armor):
    """Medium armor for mid-game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Chain Mail", '[', 2, description="Flexible chain mail armor")


class PlateArmor(Armor):
    """Heavy armor for late game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Plate Armor", '[', 3, description="Heavy plate armor")


class DragonScale(Armor):
    """Legendary armor from dragon materials."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Dragon Scale Armor", '[', 5, description="Legendary dragon scale armor")


class SpikedArmor(Armor):
    """Aggressive armor with spikes for extra protection and offense."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Spiked Armor", '[', 1, description="Menacing armor covered in spikes", attack_bonus=2)