"""
Applies Fire enchantment to equipped weapon (attack trait) or armor (resistance).
"""

from constants import COLOR_RED
from .boon import Boon
from enchantments import EnchantmentType, get_weapon_enchantment_by_type


class FireBoon(Boon):
    """Applies Fire enchantment to equipped weapon (attack trait) or armor (resistance)"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Fire Boon",
            char='*',
            color=COLOR_RED,
            description="Applies Fire enchantment to equipped weapon (Fire attacks) or armor (Fire resistance)",
            effect_value=1,
            enchantment_type=EnchantmentType.FIRE
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Apply Fire enchantment to weapon for attack trait."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} ignites with flaming power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")
    
    def apply_to_armor(self, player, enchantment_type):
        """Apply Fire enchantment to armor for resistance."""
        from enchantments import get_armor_enchantment_by_type
        enchantment = get_armor_enchantment_by_type(enchantment_type)
        if player.armor.add_enchantment(enchantment):
            return (True, f"Your {player.armor.name} becomes fireproof!")
        else:
            return (False, f"Your {player.armor.name} cannot be further enhanced!")