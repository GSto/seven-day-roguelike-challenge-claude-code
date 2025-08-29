"""
Warden's Tome accessory - permanently increases defense when leveling up.
"""

from .accessory import Accessory
from constants import COLOR_BLUE
from event_type import EventType
from event_context import LevelUpContext

class WardensTome(Accessory):
    """An accessory that permanently increases defense when the player levels up."""
    
    def __init__(self, x, y):
        super().__init__(
            x, y,
            name="Warden's Tome",
            char="♦",
            description="Permanently gain +1 DEF when leveling up",
        )
        self.market_value = 38  # Uncommon accessory
        self.color = COLOR_BLUE
        # Subscribe to level up events
        self.event_subscriptions.add(EventType.LEVEL_UP)
    
    def on_event(self, event_type, context):
        """Handle level up events."""
        if event_type == EventType.LEVEL_UP and isinstance(context, LevelUpContext):
            # Permanently increase player defense
            context.player.defense += 1