"""
Applies Dark enchantment to equipped weapon (attack trait) or armor (resistance).
"""

from constants import COLOR_SALMON
from .boon import Boon
from enchantments import EnchantmentType, get_weapon_enchantment_by_type


class DarkBoon(Boon):
    """Applies Dark enchantment to equipped weapon (attack trait) or armor (resistance)"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Dark Boon",
            char='*',
            color=COLOR_SALMON,
            description="Applies Dark enchantment to equipped weapon (Dark attacks) or armor (Dark resistance)",
            effect_value=1,
            enchantment_type=EnchantmentType.DARK
        )
    
    def apply_to_weapon(self, player, enchantment_type):
        """Apply Dark enchantment to weapon for attack trait."""
        enchantment = get_weapon_enchantment_by_type(enchantment_type)
        if player.weapon.add_enchantment(enchantment):
            return (True, f"Your {player.weapon.name} is shrouded in dark power!")
        else:
            return (False, f"Your {player.weapon.name} cannot be further enhanced!")
    
    def apply_to_armor(self, player, enchantment_type):
        """Apply Dark enchantment to armor for resistance."""
        from enchantments import get_armor_enchantment_by_type
        enchantment = get_armor_enchantment_by_type(enchantment_type)
        if player.armor.add_enchantment(enchantment):
            return (True, f"Your {player.armor.name} radiates an ominous aura!")
        else:
            return (False, f"Your {player.armor.name} cannot be further enhanced!")