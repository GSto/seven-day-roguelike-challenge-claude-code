"""
Applies a random enchantment to equipped weapon or armor.
"""

import random
from constants import COLOR_GREEN
from .boon import Boon
from enchantments import EnchantmentType, get_weapon_enchantment_by_type


class JokersBoon(Boon):
    """Applies a random enchantment to equipped weapon or armor"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Joker's Boon",
            char='*',
            color=COLOR_GREEN,
            description="Applies a random enchantment to equipped weapon or armor",
            effect_value=1
        )
    
    def use(self, player):
        """Apply a random enchantment with equipment choice"""
        # Get all possible enchantment types
        all_enchantments = [e for e in EnchantmentType]
        random_enchantment_type = random.choice(all_enchantments)
        
        # Store the selected enchantment type for later use
        self.selected_enchantment_type = random_enchantment_type
        
        # Use the choice logic with the random enchantment type
        return self.apply_enchantment_with_choice(player, random_enchantment_type)
    
    def apply_to_weapon(self, player, enchantment_type):
        """Override to provide custom message for Joker's Boon."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} is enchanted with {enchantment.name} power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")
    
    def apply_to_armor(self, player, enchantment_type):
        """Override to provide custom message for Joker's Boon."""
        from enchantments import get_armor_enchantment_by_type
        enchantment = get_armor_enchantment_by_type(enchantment_type)
        if player.armor.add_enchantment(enchantment):
            return (True, f"Your {player.armor.name} is enchanted with {enchantment.name} power!")
        else:
            return (False, f"Your {player.armor.name} cannot be further enhanced!")