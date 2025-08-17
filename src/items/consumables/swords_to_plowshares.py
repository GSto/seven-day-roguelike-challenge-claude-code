"""
Replace all unequipped weapons in inventory with health potions.
"""

from constants import COLOR_WHITE
from ..consumable import Consumable


class SwordsToPlowshares(Consumable):
    """Replace all unequipped weapons in inventory with health potions"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Swords to Plowshares",
            char='s',
            color=COLOR_WHITE,
            description="Replace all unequipped weapons in inventory with health potions"
        )
    
    def use(self, player):
        """Convert weapons to health potions"""
        from .health_potion import HealthPotion
        from ..weapons.base import Weapon
        
        # Find all unequipped weapons in inventory
        weapon_items = []
        for item in player.inventory:
            if isinstance(item, Weapon) and item != player.weapon:
                weapon_items.append(item)
        
        if not weapon_items:
            return (False, "You have no unequipped weapons to convert!")
        
        # Convert each weapon to a health potion
        for weapon in weapon_items:
            player.remove_item(weapon)
            health_potion = HealthPotion(0, 0)
            player.add_item(health_potion)
        
        count = len(weapon_items)
        if count == 1:
            return (True, f"Your {weapon_items[0].name} transforms into a healing potion!")
        else:
            return (True, f"{count} weapons transform into healing potions!")