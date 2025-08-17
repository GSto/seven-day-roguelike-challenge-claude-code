"""
Replace all unequipped armor in inventory with shield potions.
"""

from constants import COLOR_WHITE
from ..consumable import Consumable


class Transmutation(Consumable):
    """Replace all unequipped armor in inventory with shield potions"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Transmutation",
            char='t',
            color=COLOR_WHITE,
            description="Replace all unequipped armor in inventory with shield potions"
        )
    
    def use(self, player):
        """Convert armor to shield potions"""
        from .shell_potion import ShellPotion
        from ..armor.base import Armor
        
        # Find all unequipped armor in inventory
        armor_items = []
        for item in player.inventory:
            if isinstance(item, Armor) and item != player.armor:
                armor_items.append(item)
        
        if not armor_items:
            return (False, "You have no unequipped armor to transmute!")
        
        # Convert each armor piece to a shield potion
        for armor in armor_items:
            player.remove_item(armor)
            shield_potion = ShellPotion(0, 0)
            player.add_item(shield_potion)
        
        count = len(armor_items)
        if count == 1:
            return (True, f"Your {armor_items[0].name} transforms into a protective potion!")
        else:
            return (True, f"{count} pieces of armor transform into protective potions!")