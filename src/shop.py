"""
Shop system for buying and selling items using XP as currency.
"""

import random
from typing import List, Optional, Tuple
from items.pool import ItemPool
from items.consumables.health_potion import HealthPotion


class Shop:
    """Shop for buying and selling items."""
    
    def __init__(self, floor_level: int):
        """Initialize a shop for a specific floor."""
        self.floor_level = floor_level
        self.inventory: List[Optional] = []  # List of items for sale (None = empty slot)
        self.x: Optional[int] = None  # Position in room
        self.y: Optional[int] = None
        self.symbol = '$'
        self.color = (255, 215, 0)  # Gold color for shop symbol
        
        # Generate initial inventory
        self.generate_inventory()
    
    def generate_inventory(self):
        """Generate level-appropriate items for shop."""
        # Clear existing inventory
        self.inventory = []
        
        # 1 guaranteed health potion
        health_potion = HealthPotion(0, 0)
        self.inventory.append(health_potion)
        
        # 2-3 level-appropriate consumables
        num_consumables = random.randint(2, 3)
        for _ in range(num_consumables):
            item = self._create_shop_item('consumable')
            if item and not self._is_duplicate(item):
                self.inventory.append(item)
        
        # 2-3 level-appropriate weapons
        num_weapons = random.randint(2, 3)
        for _ in range(num_weapons):
            item = self._create_shop_item('weapon')
            if item and not self._is_duplicate(item):
                self.inventory.append(item)
        
        # 2-3 level-appropriate armor pieces
        num_armor = random.randint(2, 3)
        for _ in range(num_armor):
            item = self._create_shop_item('armor')
            if item and not self._is_duplicate(item):
                self.inventory.append(item)
        
        # 2-3 level-appropriate accessories
        num_accessories = random.randint(2, 3)
        for _ in range(num_accessories):
            item = self._create_shop_item('accessory')
            if item and not self._is_duplicate(item):
                self.inventory.append(item)
        
        # Pad inventory to ensure consistent size (max 15 items)
        while len(self.inventory) < 15:
            self.inventory.append(None)  # Empty slots
    
    def _create_shop_item(self, item_type: str):
        """Create a shop item without affecting the main game's item pool."""
        from items.pool import ItemPool
        
        # Create a temporary pool that doesn't affect global state
        temp_pool = ItemPool()
        
        # Get appropriate specs for the item type
        if item_type == 'weapon':
            specs = temp_pool.weapon_specs
        elif item_type == 'armor':
            specs = temp_pool.armor_specs
        elif item_type == 'accessory':
            specs = temp_pool.accessory_specs
        elif item_type == 'consumable':
            specs = temp_pool.consumable_specs
        else:
            return None
        
        # Filter specs for current level
        level_appropriate_specs = []
        for spec in specs:
            if (spec.min_level <= self.floor_level and 
                (spec.max_level is None or spec.max_level >= self.floor_level)):
                level_appropriate_specs.append(spec)
        
        if not level_appropriate_specs:
            return None
        
        # Choose a random spec and create the item
        chosen_spec = random.choice(level_appropriate_specs)
        return chosen_spec.item_class(0, 0)
    
    def _is_duplicate(self, new_item) -> bool:
        """Check if item type already exists in inventory."""
        for item in self.inventory:
            if item and type(item).__name__ == type(new_item).__name__:
                return True
        return False
    
    def buy_item(self, item_index: int, player) -> Tuple[bool, str]:
        """
        Handle item purchase transaction.
        
        Returns:
            (success, message) tuple
        """
        # Validate index
        if item_index < 0 or item_index >= len(self.inventory):
            return False, "Invalid item selection."
        
        item = self.inventory[item_index]
        if item is None:
            return False, "That slot is empty."
        
        # Check if player has enough XP
        if player.xp < item.market_value:
            return False, f"Not enough XP! Need {item.market_value}, have {player.xp}."
        
        # Check if player has inventory space
        if len(player.inventory) >= player.inventory_size:
            return False, "Your inventory is full!"
        
        # Process transaction
        player.xp -= item.market_value
        player.inventory.append(item)
        self.inventory[item_index] = None  # Remove from shop
        
        return True, f"Purchased {item.name} for {item.market_value} XP."
    
    def sell_item(self, item, player) -> Tuple[bool, str]:
        """
        Handle item sale transaction.
        
        Returns:
            (success, message) tuple
        """
        if item not in player.inventory:
            return False, "You don't have that item."
        
        # Calculate sell price (50% of market value, rounded down)
        sell_price = item.market_value // 2
        
        # Process transaction
        player.inventory.remove(item)
        player.xp += sell_price
        
        # Don't add sold items back to shop inventory (they're gone)
        
        return True, f"Sold {item.name} for {sell_price} XP."
    
    def get_item_price(self, item) -> int:
        """Get the purchase price of an item."""
        return item.market_value
    
    def get_sell_price(self, item) -> int:
        """Get the sell price of an item (50% of market value)."""
        return item.market_value // 2
    
    def render(self, console, fov):
        """Render the shop symbol on the console."""
        if self.x is not None and self.y is not None:
            if fov[self.x, self.y]:
                console.print(self.x, self.y, self.symbol, fg=self.color)