"""
Accessory items like rings and amulets.
"""

from constants import COLOR_WHITE
from .base import Equipment


class Accessory(Equipment):
    """Accessory equipment (rings, amulets, etc.)."""
    
    def __init__(self, x, y, name, char, attack_bonus=0, defense_bonus=0, 
                 description="", fov_bonus=0, health_aspect_bonus=0.0, attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0):
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
            health_aspect_bonus=health_aspect_bonus,
            attack_multiplier_bonus=attack_multiplier_bonus,
            defense_multiplier_bonus=defense_multiplier_bonus,
            xp_multiplier_bonus=xp_multiplier_bonus
        )

# Base Classes
class Ring(Accessory):
    """Base class for rings."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0, 
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0, description="A magical ring"):
        super().__init__(x, y, name, '=', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                         attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus)

class Card(Accessory):
    """Base class for cards."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0, description="An enchanted card"):
        super().__init__(x, y, name, '🂡', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                         attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus)


class Necklace(Accessory):
    """Base class for necklaces."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0, description="A magical necklace"):
        super().__init__(x, y, name, 'v', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                         attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus)

class Hat(Accessory):
    """Base class for hats."""
    
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0, fov_bonus=0, health_aspect_bonus=0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0, description="A cool hat"):
        super().__init__(x, y, name, '^', attack_bonus, defense_bonus, description, fov_bonus, health_aspect_bonus,
                         attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus)


class PowerRing(Ring):
    """Ring that boosts attack."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Power", attack_bonus=4, defense_bonus=0)


class ProtectionRing(Ring):
    """Ring that provides strong defense."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Protection", defense_bonus=3)

class Rosary(Necklace):
    """Necklace that increases health aspect."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Rosary", attack_bonus=0, defense_bonus=1, fov_bonus=0, health_aspect_bonus=0.1, description="A healer's necklace")

class HeadLamp(Hat):
    """Hat that increases FOV"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "HeadLamp", attack_bonus=0, defense_bonus=1, fov_bonus=1, health_aspect_bonus=0, description="lamp on your head")

class BaronsCrown(Hat):
    """Hat with attack multiplier."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Baron's Crown", attack_multiplier_bonus=1.25, description="Crown of a Jester King")

class JewelersCap(Hat):
    """Hat with XP multiplier."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Jeweler's Cap", xp_multiplier_bonus=1.1, description="A greedy man's gift")

# Later Game Accessories

class GreaterPowerRing(Ring):
    """Ring that greatly boosts attack."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Greater Ring of Power", attack_bonus=9, defense_bonus=0)


class GreaterProtectionRing(Ring):
    """Ring that greatly boosts attack."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Greater Ring of Protection", attack_bonus=0, defense_bonus=7)


class AceOfSpades(Card):
    """Legendary ring with high attack multiplier."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ace of Spades", attack_multiplier_bonus=2.0, defense_multiplier_bonus=0.1, description="Are you a gambling man? doubles attack, decimates defense")