"""
Base pickup class for instant-effect items.
"""

from ..item import Item


class Pickup(Item):
    """Base class for pickup items that have instant effects when collected."""
    
    def __init__(self, x, y, name, char, color, description="", market_value=0):
        """Initialize a pickup item.
        
        Pickups typically have no market value since they're consumed instantly.
        """
        super().__init__(x, y, name, char, color, description, market_value)
    
    def on_pickup(self, player):
        """Apply instant effect when picked up.
        
        Returns:
            tuple: (success, message) - whether pickup was successful and message to display
        """
        # Default implementation - override in subclasses
        return False, "Nothing happens."