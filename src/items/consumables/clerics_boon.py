"""
Applies Blessed enchantment to equipped weapon.
"""

from constants import COLOR_WHITE
from .boon import Boon
from enchantments import EnchantmentType, get_weapon_enchantment_by_type


class ClericsBoon(Boon):
    """Applies Blessed enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Cleric's Boon",
            char='*',
            color=COLOR_WHITE,
            description="Applies Blessed enchantment to equipped weapon (+5% healing)",
            effect_value=1,
            enchantment_type=EnchantmentType.BLESSED
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Override to provide custom message for Cleric's Boon."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} is blessed with divine power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")