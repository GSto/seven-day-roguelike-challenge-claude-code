"""
Applies Rending enchantment to equipped weapon.
"""

from constants import COLOR_RED
from .boon import Boon
from enchantments import EnchantmentType, get_weapon_enchantment_by_type


class ReapersBoon(Boon):
    """Applies Rending enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Reaper's Boon",
            char='*',
            color=COLOR_RED,
            description="Applies Rending enchantment to equipped weapon (+10% crit)",
            effect_value=1,
            enchantment_type=EnchantmentType.RENDING
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Override to provide custom message for Reaper's Boon."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} is enchanted with Rending power (+10% crit chance)!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")