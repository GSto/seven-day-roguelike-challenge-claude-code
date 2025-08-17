"""
ElementalMayhem - Grants a +3 attack bonus for every unique elemental trait among attack traits, and resistance traits.
"""
from .accessory import Accessory


class ElementalMayhem(Accessory):
    """Grants a +3 attack bonus for every unique elemental trait among attack traits, and resistance traits"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Elemental Mayhem", '=',
                        description="Grants a +3 attack bonus for every unique elemental trait among attack traits and resistance traits")
    
    def get_attack_bonus(self, player):
        """Get attack bonus based on unique elemental traits."""
        base_bonus = super().get_attack_bonus(player)
        
        # Get all attack traits from player
        attack_traits = player.get_total_attack_traits()
        resistance_traits = player.get_total_resistances()
        
        # Combine and count unique elemental traits
        all_traits = set(attack_traits + resistance_traits)
        elemental_traits = {trait for trait in all_traits if trait.is_elemental}
        
        return base_bonus + (len(elemental_traits) * 3)