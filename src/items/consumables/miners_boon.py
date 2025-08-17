"""
Applies Glowing enchantment to equipped weapon.
"""

from constants import COLOR_CYAN
from .boon import Boon
from enchantments import EnchantmentType, get_weapon_enchantment_by_type


class MinersBoon(Boon):
    """Applies Glowing enchantment to equipped weapon"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Miner's Boon",
            char='*',
            color=COLOR_CYAN,
            description="Applies Glowing enchantment to equipped weapon (+2 FOV)",
            effect_value=1,
            enchantment_type=EnchantmentType.GLOWING
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Override to provide custom message for Miner's Boon."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} begins to glow softly!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")