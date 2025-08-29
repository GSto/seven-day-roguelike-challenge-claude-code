"""
MallNinja - +1 ATK for every weapon in your inventory.
"""
from .accessory import Accessory


class MallNinja(Accessory):
    """+1 ATK for every weapon in your inventory"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Mall Ninja", '=',
        description="+1 ATK for every weapon in your inventory")
        self.market_value = 38  # Uncommon accessory
    
    def get_attack_bonus(self, player):
        """Get attack bonus based on number of weapons in inventory."""
        base_bonus = super().get_attack_bonus(player)
        weapon_count = sum(1 for item in player.inventory if hasattr(item, 'equipment_slot') and item.equipment_slot == 'weapon')
        return base_bonus + weapon_count