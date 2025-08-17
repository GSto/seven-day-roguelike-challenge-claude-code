"""
Applies Gilded enchantment to equipped weapon.
"""

from constants import COLOR_WHITE
from .boon import Boon
from enchantments import EnchantmentType, get_weapon_enchantment_by_type


class JewelersBoon(Boon):
    """Applies Gilded enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Jeweler's Boon",
            char='*',
            color=COLOR_WHITE,
            description="Applies Gilded enchantment to equipped weapon (+5% XP)",
            effect_value=1,
            enchantment_type=EnchantmentType.GILDED
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Override to provide custom message for Jeweler's Boon."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} gleams with golden light!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")