"""
Materia Staff weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class MateriaStaff(Weapon):
    """A staff that gets better with enchantments."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Materia Staff", ')', 2, "A staff that gets better with enchantments", attack_traits=[Trait.MYSTIC])
        self.market_value = 68  # Mid game uncommon weapon
        self.no_initial_enchantments = True

    def get_attack_bonus(self, player):
        base_attack = super().get_attack_bonus(player) 
        enchant_count = len(self.enchantments)
        if(player.armor is not None): 
            enchant_count += len(player.armor.enchantments)
        if enchant_count == 0:
            return base_attack
        elif enchant_count == 1:
            return base_attack + 3
        elif enchant_count == 2: 
            return base_attack + 6
        elif enchant_count == 3:
            return base_attack + 9 
        else:
            return base_attack + 12