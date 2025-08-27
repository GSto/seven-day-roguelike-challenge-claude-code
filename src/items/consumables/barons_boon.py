"""
Applies Shiny enchantment to equipped weapon or armor.
"""

from constants import COLOR_YELLOW
from .boon import Boon
from enchantments import EnchantmentType


class BaronsBoon(Boon):
    """Applies Shiny enchantment to equipped weapon or armor"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Baron's Boon",
            char='*',
            color=COLOR_YELLOW,
            description="Applies Shiny enchantment to weapon (1.25x ATK) or armor (1.25x DEF)",
            effect_value=1,
            enchantment_type=EnchantmentType.SHINY
        )