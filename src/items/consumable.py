"""
Consumable item class for the roguelike game.
"""

from .item import Item


class Consumable(Item):
    """Base class for consumable items like potions."""
    
    def __init__(self, x, y, name, char, color, description="", effect_value=0,
                 attack_multiplier_effect=0.0, defense_multiplier_effect=0.0, xp_multiplier_effect=0.0,
                 attack_traits=None, weaknesses=None, resistances=None, charges=None):
        super().__init__(x, y, name, char, color, description)
        self.effect_value = effect_value
        
        # Multiplier effects (additive to current multipliers)
        self.attack_multiplier_effect = attack_multiplier_effect
        self.defense_multiplier_effect = defense_multiplier_effect
        self.xp_multiplier_effect = xp_multiplier_effect
        
        # Traits system
        self.attack_traits = attack_traits or []
        self.weaknesses = weaknesses or []
        self.resistances = resistances or []
        
        # Charges system - if None, item is destroyed after use
        self.charges = charges
        self.max_charges = charges if charges is not None else None
    
    def use(self, player, **kwargs):
        """Use the consumable item. Returns (success, message, should_destroy)."""
        # Default implementation - override in subclasses
        # Returns whether use was successful, message, and whether item should be destroyed
        return False, "Cannot use this item", True
    
    def use_charge(self):
        """Use one charge and return whether item should be destroyed."""
        if self.charges is None:
            return True  # Item has no charges, should be destroyed
        
        self.charges -= 1
        return self.charges <= 0  # Destroy if no charges left
    
    def get_display_name(self):
        """Get display name including charges if applicable."""
        if self.charges is not None:
            return f"{self.name} ({self.charges}/{self.max_charges})"
        return self.name