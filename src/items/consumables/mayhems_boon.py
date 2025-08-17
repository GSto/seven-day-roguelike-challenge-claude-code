"""
Grants a random elemental enchantment bonus.
"""

import random
from constants import COLOR_WHITE
from ..consumable import Consumable


class MayhemsBoon(Consumable):
    """Grants a random elemental enchantment bonus"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Mayhem's Boon",
            char='*',
            color=COLOR_WHITE,
            description="Grants a random elemental enchantment bonus"
        )
    
    def use(self, player):
        """Apply a random elemental enchantment to equipped weapon or armor"""
        from enchantments import EnchantmentType, get_weapon_enchantment_by_type, get_armor_enchantment_by_type
        
        # Get elemental enchantment types
        elemental_enchantments = [EnchantmentType.FIRE, EnchantmentType.ICE, EnchantmentType.HOLY, EnchantmentType.DARK]
        random_enchantment = random.choice(elemental_enchantments)
        
        # Check what can be enchanted
        weapon_eligible = (player.weapon is not None and
                          len(player.weapon.enchantments) < 2 and
                          not any(e.type == random_enchantment for e in player.weapon.enchantments))
        armor_eligible = (player.armor is not None and
                         len(player.armor.enchantments) < 2 and
                         not any(e.type == random_enchantment for e in player.armor.enchantments))
        
        if not weapon_eligible and not armor_eligible:
            return (False, "You need equipped items that can be further enhanced!")
        
        # Prefer weapon if both available
        if weapon_eligible:
            enchantment = get_weapon_enchantment_by_type(random_enchantment)
            if player.weapon.add_enchantment(enchantment):
                return (True, f"Your {player.weapon.name} is enchanted with {random_enchantment.value} power!")
        elif armor_eligible:
            enchantment = get_armor_enchantment_by_type(random_enchantment)
            if player.armor.add_enchantment(enchantment):
                return (True, f"Your {player.armor.name} is enchanted with {random_enchantment.value} protection!")
        
        return (False, "The enchantment failed to take hold!")