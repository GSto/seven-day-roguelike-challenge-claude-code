"""
Base item classes for the roguelike game.
"""

from constants import COLOR_WHITE


class Item:
    """Base class for all items."""
    
    def __init__(self, x, y, name, char, color, description=""):
        """Initialize an item."""
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.description = description
    
    def render(self, console, fov):
        """Render the item on the console."""
        if fov[self.x, self.y]:
            console.print(self.x, self.y, self.char, fg=self.color)


class Consumable(Item):
    """Base class for consumable items like potions."""
    
    def __init__(self, x, y, name, char, color, description="", effect_value=0,
                 attack_multiplier_effect=0.0, defense_multiplier_effect=0.0, xp_multiplier_effect=0.0):
        super().__init__(x, y, name, char, color, description)
        self.effect_value = effect_value
        
        # Multiplier effects (additive to current multipliers)
        self.attack_multiplier_effect = attack_multiplier_effect
        self.defense_multiplier_effect = defense_multiplier_effect
        self.xp_multiplier_effect = xp_multiplier_effect
    
    def use(self, player):
        """Use the consumable item. Returns True if successfully used."""
        return False  # Override in subclasses


class Equipment(Item):
    """Base class for equippable items."""
    
    def __init__(self, x, y, name, char, color, description="", 
                 attack_bonus=0, defense_bonus=0, equipment_slot="", 
                 fov_bonus=0, health_aspect_bonus=0.0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0):
        super().__init__(x, y, name, char, color, description)
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.equipment_slot = equipment_slot  # "weapon", "armor", "accessory"
        self.fov_bonus = fov_bonus  # Bonus to field of view radius
        self.health_aspect_bonus = health_aspect_bonus  # Bonus to health potion effectiveness
        
        # Multiplier bonuses (additive to base multiplier of 1.0)
        self.attack_multiplier_bonus = attack_multiplier_bonus
        self.defense_multiplier_bonus = defense_multiplier_bonus
        self.xp_multiplier_bonus = xp_multiplier_bonus
    
    def can_equip(self, player):
        """Check if player can equip this item."""
        return True  # Basic check, can be overridden