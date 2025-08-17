"""
Base class for boons that apply enchantments to equipment.
"""

from constants import COLOR_WHITE
from ..consumable import Consumable
from enchantments import EnchantmentType, get_weapon_enchantment_by_type


class Boon(Consumable):
    """Base class for boons that apply enchantments to equipment."""
    
    def __init__(self, x, y, name, char='*', color=COLOR_WHITE, description="", effect_value=1, enchantment_type=None):
        super().__init__(
            x=x, y=y,
            name=name,
            char=char,
            color=color,
            description=description,
            effect_value=effect_value
        )
        self.enchantment_type = enchantment_type
    
    def use(self, player):
        """Default use method that applies enchantment with choice logic."""
        if self.enchantment_type is None:
            return (False, "This boon has no enchantment type specified!")
        return self.apply_enchantment_with_choice(player, self.enchantment_type)
    
    def apply_enchantment_with_choice(self, player, enchantment_type):
        """Apply enchantment with weapon/armor choice logic."""
        # Check eligibility
        weapon_eligible = self.can_enchant_weapon(player, enchantment_type)
        armor_eligible = self.can_enchant_armor(player, enchantment_type)
        
        if not weapon_eligible and not armor_eligible:
            return (False, "You need equipped items that can be further enhanced!")
        
        # If only one option available, use it automatically
        if weapon_eligible and not armor_eligible:
            return self.apply_to_weapon(player, enchantment_type)
        elif armor_eligible and not weapon_eligible:
            return self.apply_to_armor(player, enchantment_type)
        
        # Both are eligible - player needs to choose
        # Return a special state indicating choice is needed
        # This will be handled by the game's choice system
        return ("CHOICE_NEEDED", enchantment_type)
    
    def can_enchant_weapon(self, player, enchantment_type):
        """Check if weapon can be enchanted."""
        return (player.weapon is not None and
                len(player.weapon.enchantments) < 2 and
                enchantment_type.can_enchant_weapon and
                not any(e.type == enchantment_type for e in player.weapon.enchantments))
    
    def can_enchant_armor(self, player, enchantment_type):
        """Check if armor can be enchanted."""
        return (player.armor is not None and
                len(player.armor.enchantments) < 2 and
                enchantment_type.can_enchant_armor and
                not any(e.type == enchantment_type for e in player.armor.enchantments))
    
    def apply_to_weapon(self, player, enchantment_type):
        """Apply enchantment to weapon."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} shines with new power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")
    
    def apply_to_armor(self, player, enchantment_type):
        """Apply enchantment to armor."""
        from enchantments import get_armor_enchantment_by_type
        enchantment = get_armor_enchantment_by_type(enchantment_type)
        if player.armor.add_enchantment(enchantment):
            return (True, f"Your {player.armor.name} gleams with new protection!")
        else:
            return (False, f"Your {player.armor.name} cannot be further enhanced!")