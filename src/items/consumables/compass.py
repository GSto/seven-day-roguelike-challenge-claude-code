"""
Makes all items visible on the map (3 charges).
"""

from constants import COLOR_WHITE
from ..consumable import Consumable


class Compass(Consumable):
    """Makes all items visible on the map (3 charges)"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Compass",
            char='c',
            color=COLOR_WHITE,
            description="Makes all items visible on the map",
            charges=3
        )
    
    def use(self, player):
        """Reveal all items on the current floor"""
        # This requires access to the current level's items
        if not hasattr(player, '_current_level') or player._current_level is None:
            self.use_charge()
            return (False, "Unable to detect items - no floor detected!")
        
        level = player._current_level
        
        # Mark all item positions as visible in FOV
        # This creates a temporary "sight" of all items
        items_revealed = 0
        for item in level.items:
            # Set FOV to true for item positions to make them visible
            level.fov[item.x, item.y] = True
            items_revealed += 1
        
        self.use_charge()
        
        if items_revealed == 0:
            return (True, "No items detected on this floor.")
        elif items_revealed == 1:
            return (True, "1 item is now visible on this floor!")
        else:
            return (True, f"{items_revealed} items are now visible on this floor!")