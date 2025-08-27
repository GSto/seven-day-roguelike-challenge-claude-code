"""
Applies Holy enchantment to equipped weapon (attack trait) or armor (resistance).
"""

from constants import COLOR_YELLOW
from .boon import Boon
from enchantments import EnchantmentType, get_weapon_enchantment_by_type


class HolyBoon(Boon):
    """Applies Holy enchantment to equipped weapon (attack trait) or armor (resistance)"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Holy Boon",
            char='*',
            color=COLOR_YELLOW,
            description="Applies Holy enchantment to equipped weapon or armor",
            effect_value=1,
            enchantment_type=EnchantmentType.HOLY
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Apply Holy enchantment to weapon for attack trait."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} shines with divine light!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")
    
    def apply_to_armor(self, player, enchantment_type):
        """Apply Holy enchantment to armor for resistance."""
        from enchantments import get_armor_enchantment_by_type
        enchantment = get_armor_enchantment_by_type(enchantment_type)
        if player.armor.add_enchantment(enchantment):
            return (True, f"Your {player.armor.name} glows with blessed protection!")
        else:
            return (False, f"Your {player.armor.name} cannot be further enhanced!")