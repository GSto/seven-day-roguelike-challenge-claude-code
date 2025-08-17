"""
Cleric's Staff weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class ClericsStaff(Weapon):
    """Holy staff that enhances healing abilities."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Cleric's Staff", ')', 4, "A holy staff that enhances healing", health_aspect_bonus=0.2, attack_traits=[Trait.HOLY, Trait.MYSTIC])
    
    def get_enchantment_bonus(self, enchantment, bonus_type, player):
        """Override to give special bonuses for BLESSED and HOLY enchantments."""
        from enchantments import EnchantmentType
        
        # Get base bonus
        base_bonus = super().get_enchantment_bonus(enchantment, bonus_type, player)
        
        # Special bonuses for BLESSED and HOLY enchantments on Cleric's Staff
        if enchantment.type in [EnchantmentType.BLESSED, EnchantmentType.HOLY]:
            if bonus_type == "attack":
                base_bonus += 4  # Additional +4 ATK bonus
            elif bonus_type == "health_aspect":
                base_bonus += 0.10  # Additional +10% health aspect bonus
        
        return base_bonus